"""Reference data about the game, generated from its sources.

The validator never reads game files - this is its only knowledge of them. That
is what lets the tool ship to modders who do not have the game's source.

Catalogue-derived checks are warnings, never errors: an unknown icon means "not
in the catalogue I shipped with", which is also what a legitimately new value
looks like. The rules that can crash the game need nothing from here beyond the
id list, so they stay correct however old this file is.
"""

import dataclasses
import json
import pathlib
import sys

if getattr(sys, "frozen", False):
	# The prebuilt program (PyInstaller) unpacks its bundled catalog next to itself.
	DEFAULT_PATH = pathlib.Path(sys._MEIPASS) / "generated" / "catalog.json"
else:
	DEFAULT_PATH = pathlib.Path(__file__).resolve().parents[3] / "generated" / "catalog.json"

SUPPORTED_SCHEMA = 1


@dataclasses.dataclass
class Catalog:
	game_version: str = None
	generated_at: str = None
	mission_ids: tuple = ()
	quest_ids: tuple = ()
	icons: dict = dataclasses.field(default_factory=dict)      # name -> is result marker
	locations: set = dataclasses.field(default_factory=set)  # location IDs
	minor_events: dict = dataclasses.field(default_factory=dict)  # constant -> tutorial_only
	dead_handlers: dict = dataclasses.field(default_factory=dict)  # constant -> event name
	unbound_quest_types: dict = dataclasses.field(default_factory=dict)  # value -> name
	quest_types: frozenset = frozenset()  # every value the enum declares
	loc_terms: set = dataclasses.field(default_factory=set)

	@property
	def is_empty(self):
		return not self.mission_ids and not self.icons


def load(path=None):
	"""Read the catalogue. A missing or unreadable file yields an empty one, so
	the crash-checks still run with --no-catalog or a broken install."""

	path = pathlib.Path(path) if path else DEFAULT_PATH

	try:
		data = json.loads(path.read_text(encoding="utf-8"))
	except (OSError, json.JSONDecodeError):
		return Catalog()

	if data.get("schema_version") != SUPPORTED_SCHEMA:
		return Catalog()

	subquest = data.get("enums", {}).get("SubQuestRequirementType", [])

	return Catalog(
		game_version=data.get("game_version"),
		generated_at=data.get("generated_at"),
		mission_ids=tuple(data.get("mission_ids", ())),
		quest_ids=tuple(data.get("quest_ids", ())),
		icons={entry["name"]: entry.get("result_marker", False) for entry in data.get("icons", [])},
		locations={entry["id"] for entry in data.get("locations", []) if not entry.get("test_data")},
		minor_events={entry["constant"]: entry.get("tutorial_only", False) for entry in data.get("minor_events", [])},
		dead_handlers={entry["constant"]: entry["event"] for entry in data.get("mission_handlers", []) if entry.get("dead")},
		unbound_quest_types={entry["value"]: entry["name"] for entry in subquest if not entry.get("has_validator")},
		quest_types=frozenset(entry["value"] for entry in subquest),
		loc_terms=set(data.get("loc_terms", ())),
	)
