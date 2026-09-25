"""Walk a mod folder and classify what is in it.

A path may be a mod root (containing Missions/, Events/, Quests/), a folder of
mods, or a single content folder. All three are accepted, because a modder
testing one mission should not have to build the whole tree first.
"""

import dataclasses
import pathlib

# MissionBase.py is a template that returns the literal "[MissionId]" and has no
# JSON. Treating it as a mission produces a bogus orphan finding and poisons the
# substring check for every real mission.
TEMPLATE_STEMS = {"MissionBase", "default_mission"}

CONTENT_FOLDERS = ("Missions", "Events", "Quests")

# config.json is the mod's own settings file at the mod root, never a mission. A CSV-only
# mod has a config.json and no Missions/ folder, which would otherwise make the root look
# like a folder of loose mission files.
NON_CONTENT_FILES = {"config.json"}


@dataclasses.dataclass
class MissionUnit:
	stem: str
	json_path: pathlib.Path = None
	py_path: pathlib.Path = None

	@property
	def paths(self):
		return [p for p in (self.json_path, self.py_path) if p]


@dataclasses.dataclass
class EventUnit:
	stem: str
	py_path: pathlib.Path


@dataclasses.dataclass
class QuestUnit:
	stem: str
	json_path: pathlib.Path


@dataclasses.dataclass
class Discovery:
	missions: list = dataclasses.field(default_factory=list)
	events: list = dataclasses.field(default_factory=list)
	quests: list = dataclasses.field(default_factory=list)

	@property
	def file_count(self):
		total = sum(len(m.paths) for m in self.missions)
		return total + len(self.events) + len(self.quests)


def _collect_missions(directory, discovery):
	units = {}

	for path in sorted(directory.iterdir()):
		if path.is_dir() or path.stem in TEMPLATE_STEMS or path.name.lower() in NON_CONTENT_FILES:
			continue

		suffix = path.suffix.lower()

		if suffix not in (".json", ".py"):
			continue

		unit = units.setdefault(path.stem, MissionUnit(stem=path.stem))

		if suffix == ".json":
			unit.json_path = path
		else:
			unit.py_path = path

	discovery.missions.extend(units[stem] for stem in sorted(units))


def _collect_events(directory, discovery):
	for path in sorted(directory.iterdir()):
		if path.is_file() and path.suffix.lower() == ".py" and path.stem not in TEMPLATE_STEMS:
			discovery.events.append(EventUnit(stem=path.stem, py_path=path))


def _collect_quests(directory, discovery):
	for path in sorted(directory.iterdir()):
		if path.is_file() and path.suffix.lower() == ".json":
			discovery.quests.append(QuestUnit(stem=path.stem, json_path=path))


_COLLECTORS = {
	"Missions": _collect_missions,
	"Events": _collect_events,
	"Quests": _collect_quests,
}

# The game ships its own content under singular folder names. Recognising them
# lets the shipped corpus be validated directly, which is how the regression
# suite works.
_FOLDER_ALIASES = {
	"Mission": "Missions",
	"OldMission": "Missions",
	"Quest": "Quests",
	"Default": "Events",
	"new_missions": "Missions",
	"new_events": "Events",
}


def discover(root):
	"""Return everything under `root` that the validator knows how to check."""

	root = pathlib.Path(root)
	discovery = Discovery()

	if root.is_file():
		parent_kind = _FOLDER_ALIASES.get(root.parent.name, root.parent.name)

		if parent_kind in _COLLECTORS:
			_COLLECTORS[parent_kind](root.parent, discovery)

		return discovery

	# A content folder passed directly, e.g. .../Missions
	folder_kind = _FOLDER_ALIASES.get(root.name, root.name)

	if folder_kind in _COLLECTORS:
		_COLLECTORS[folder_kind](root, discovery)
		return discovery

	found_any = False
	# Compare names exactly: on a case-insensitive file system (macOS, Windows) `root / "Quests"`
	# would also match a folder called "quests" that is not a content folder at all.
	children = {path.name for path in root.iterdir() if path.is_dir()}

	for name, collect in _COLLECTORS.items():
		directory = root / name

		if name in children:
			collect(directory, discovery)
			found_any = True

	if found_any:
		# Missions/ is a mod's only script folder, so it also holds event scripts and helper
		# modules - there is no Events/ folder for mods. A .py there with handlers but no
		# .json is an event script, not a mission missing its data.
		_collect_loose_event_scripts(root, discovery)
		return discovery

	# A mod root whose content the validator does not check (CSV, maps, art). Stop here
	# rather than walking into CSV/ and mistaking table files for missions.
	if _is_unchecked_mod_root(root):
		return discovery

	# A bare folder holding mission files directly, with no Missions/ subfolder.
	# This is what a modder gets when they copy one example, so accept it.
	if _holds_loose_content(root):
		_collect_missions(root, discovery)
		_collect_loose_event_scripts(root, discovery)
		return discovery

	# Not a mod root - try every immediate subdirectory as one.
	for child in sorted(root.iterdir()):
		if child.is_dir():
			child_discovery = discover(child)
			discovery.missions.extend(child_discovery.missions)
			discovery.events.extend(child_discovery.events)
			discovery.quests.extend(child_discovery.quests)

	return discovery


# Mod content folders the validator has no rules for yet.
UNCHECKED_FOLDERS = ("CSV", "Maps", "Objects", "TerrainObjects", "Biomes")


def _is_unchecked_mod_root(directory):
	return any((directory / name).is_dir() for name in UNCHECKED_FOLDERS)


def _holds_loose_content(directory):
	return any(
		path.is_file()
		and path.suffix.lower() in (".json", ".py")
		and path.stem not in TEMPLATE_STEMS
		and path.name.lower() not in NON_CONTENT_FILES
		for path in directory.iterdir()
	)


def _collect_loose_event_scripts(directory, discovery):
	"""Decide what a lone .py with no .json is.

	The folder name does not settle it, even in a proper mod tree: Missions/ is a mod's
	only script folder, so event scripts and helper modules live there too. Ask the script
	instead - one that registers GET_MISSION_ID is a mission missing its JSON, anything
	else is an event script.
	"""

	from .pyscript import analyse

	orphans = [unit for unit in discovery.missions if unit.json_path is None]

	for unit in orphans:
		facts = analyse(unit.py_path)

		if facts.handler_for("GET_MISSION_ID") is not None:
			continue

		discovery.missions.remove(unit)
		discovery.events.append(EventUnit(stem=unit.stem, py_path=unit.py_path))
