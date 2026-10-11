"""The checks themselves.

Every rule is a function taking a context and yielding Findings. Rule ids are
stable strings - tests and JSON consumers depend on them, so rename with care.

The three rules in this file that matter most (outcomes, stats, substring) need
no catalogue data beyond a list of known ids, so they stay correct however old
the shipped catalogue is.
"""

import json

from .findings import Finding, Severity

# Constants that exist in MissionEvent but have no call site anywhere in the
# game. Implementing them is harmless but wasted effort.
DEAD_HANDLERS = {
	"GET_MISSION_ICON": "get_mission_icon",
	"CALCULATE_MISSION_MODIFIERS": "calculate_mission_modifiers",
	"CALCULATE_AIRPLANE_MODIFIERS": "calculate_airplane_modifiers",
	"CALCULATE_PILOT_MODIFIERS": "calculate_pilot_modifiers",
}

MANDATORY_SLOTS = ("mission_name", "mission_description", "intel_threat_report")

TRANSMISSION_SLOTS = (
	"ap_transmission",
	"gw_transmission",
	"ap_success_transmission",
	"ap_failure_transmission",
	"gw_success_transmission",
	"gw_failure_transmission",
)

OUTCOME_ORDER_HINT = (
	"Order is mandatory - the game picks with (skillPassed ? 1 : 0) | (asPlanned ? 2 : 0):\n"
	"  [0] gone wrong + skill failed\n"
	"  [1] gone wrong + skill passed\n"
	"  [2] as planned + skill failed\n"
	"  [3] as planned + skill passed"
)


def load_json(path):
	"""Return (data, error_message). Never raises."""

	try:
		return json.loads(path.read_text(encoding="utf-8-sig")), None
	except json.JSONDecodeError as error:
		return None, f"{error.msg} (line {error.lineno}, column {error.colno})"
	except OSError as error:
		return None, f"cannot read file: {error}"


def check_mission_json(unit, data, positions):
	"""Structural rules on the mission JSON."""

	path = unit.json_path

	outcomes = data.get("_missionOutcomes")

	if not isinstance(outcomes, list) or len(outcomes) != 4:
		count = len(outcomes) if isinstance(outcomes, list) else "no"

		yield Finding(
			rule="mission.outcomes.count",
			severity=Severity.ERROR,
			path=path,
			line=positions.get("_missionOutcomes"),
			message=f"{count} entries in _missionOutcomes, expected exactly 4",
			hint=OUTCOME_ORDER_HINT + "\nFewer or more throws ArgumentOutOfRangeException when the mission completes.",
			unit=unit.stem,
		)

	stats = data.get("_missionStats")

	if not isinstance(stats, list) or len(stats) < 2:
		count = len(stats) if isinstance(stats, list) else "no"

		yield Finding(
			rule="mission.stats.count",
			severity=Severity.ERROR,
			path=path,
			line=positions.get("_missionStats"),
			message=f"{count} entries in _missionStats, expected at least 2",
			hint=(
				"[0] is rolled when the mission goes as planned, [1] when it goes wrong.\n"
				"Fewer throws IndexOutOfRangeException on the skill roll."
			),
			unit=unit.stem,
		)

	locations = data.get("_potentialLocations")

	for index, entry in enumerate(locations if isinstance(locations, list) else []):
		location_id = entry.get("_locationId") if isinstance(entry, dict) else None

		if not isinstance(location_id, str) or not location_id.strip():
			yield Finding(
				rule="mission.location.id",
				severity=Severity.ERROR,
				path=path,
				line=positions.get("_potentialLocations"),
				message=f"entry {index} of _potentialLocations has no _locationId",
				hint=(
					"The game finds a location by its _locationId alone; _locationName and coordinates "
					"in a mission are ignored.\n"
					"Without an ID the entry is never found, and the mission "
					"is placed at a random location."
				),
				unit=unit.stem,
			)

	enemies = data.get("_enemyPlaneReport")

	if isinstance(enemies, int) and enemies > 18:
		yield Finding(
			rule="mission.enemyreport.high",
			severity=Severity.WARNING,
			path=path,
			line=positions.get("_enemyPlaneReport"),
			message=f"_enemyPlaneReport is {enemies}; the UI breaks above 18",
			hint="Nothing in the game enforces this limit.",
			unit=unit.stem,
		)

	if data.get("_historicDay") and not data.get("_isHistoric"):
		historic_day = data.get("_historicDay") or {}

		if isinstance(historic_day, dict) and historic_day.get("Year", 1) > 1:
			yield Finding(
				rule="mission.historic.dayunused",
				severity=Severity.NOTE,
				path=path,
				line=positions.get("_historicDay"),
				message="_historicDay is set but _isHistoric is false, so the date is ignored",
				unit=unit.stem,
			)


def is_helper_module(unit, facts):
	"""
	True for a script that registers no handlers and has no mission data beside it.

	Missions/ is not only for missions. The loader imports every .py it finds, which runs the
	module top level, so a file that registers nothing is still executed - that is how a mod
	registers quest localisation terms or shares constants between missions. Such a file has no
	.json and no get_mission_id by design, and flagging it drives modders to delete working code.

	Both halves matter. A .py beside a .json is a mission whatever it contains, and a mission
	that registers no handler is broken in the way this tool exists to catch - so the absence of
	handlers alone must not excuse it.

	facts is None when the script could not be parsed; that is reported separately, so treat an
	unparseable file as a mission rather than silently excusing it.
	"""

	return unit.json_path is None and facts is not None and not facts.handlers


def check_pairing(unit, facts=None):
	"""Both files must exist and agree on the id."""

	if unit.json_path is None:
		if is_helper_module(unit, facts):
			return

		# A script that registers initialize_mission authors its own data - gates, stats,
		# location, outcomes - so it needs no .json. Without that handler there is nothing to
		# set the mission up and SetupFromScript produces a mission of pure defaults.
		if facts is not None and facts.handler_for("INITIALIZE_MISSION") is not None:
			return

		yield Finding(
			rule="mission.pair.missing",
			severity=Severity.ERROR,
			path=unit.py_path,
			message=f"{unit.stem}.py has no matching {unit.stem}.json",
			hint=(
				"A mission script needs its .json, or must author its own data in "
				"initialize_mission, or register no handlers at all and act as a helper module."
			),
			unit=unit.stem,
		)
		return

	# A mission without its own script is the normal case: it runs on the shared
	# default_mission module. Only a script without data is broken.


def check_mission_script(unit, facts):
	"""Rules that read the script's syntax tree."""

	path = unit.py_path

	if facts.mission_id_dynamic:
		yield Finding(
			rule="mission.id.undetermined",
			severity=Severity.NOTE,
			path=path,
			line=facts.mission_id_line,
			message="get_mission_id does not return a statically known string; id checks skipped",
			hint="Return a literal or a module-level constant so tooling can read it.",
			unit=unit.stem,
		)
	elif facts.mission_id is None:
		if is_helper_module(unit, facts):
			return

		yield Finding(
			rule="mission.handler.missing",
			severity=Severity.ERROR,
			path=path,
			message="no get_mission_id handler found",
			hint="@event_handler(MissionEvent.GET_MISSION_ID) is the one required handler.",
			unit=unit.stem,
		)
	elif facts.mission_id != unit.stem:
		yield Finding(
			rule="mission.id.mismatch",
			severity=Severity.ERROR,
			path=path,
			line=facts.mission_id_line,
			message=f'get_mission_id returns "{facts.mission_id}" but the file is named "{unit.stem}"',
			hint="The file name, the JSON name and this return value must be identical.",
			unit=unit.stem,
		)

	for handler in facts.handlers:
		dead = DEAD_HANDLERS.get(handler.constant)

		if dead:
			yield Finding(
				rule="mission.handler.dead",
				severity=Severity.WARNING,
				path=path,
				line=handler.line,
				message=f"implements {dead}, which the game never calls",
				hint=(
					"The constant exists but has no call site. Older example scripts "
					"implement it too; that code does nothing.\n"
					"The mission icon comes from _missionIcon in the JSON."
				),
				unit=unit.stem,
			)


def check_id_collisions(units, known_ids):
	"""Two missions in the same run must not share an id.

	Handler resolution matches module names exactly, so a substring is no longer
	a trap - but two files claiming the same id still mean one silently replaces
	the other.
	"""

	seen = {}

	for unit in units:
		path = unit.json_path or unit.py_path

		if path is None:
			continue

		# Ids are compared case-insensitively: two files differing only in case
		# collide on Windows and macOS but not on Linux.
		key = unit.stem.lower()

		if key in seen:
			yield Finding(
				rule="mission.id.duplicate",
				severity=Severity.ERROR,
				path=path,
				message=f'mission id "{unit.stem}" is already defined by {seen[key]}',
				hint=(
					"Two files claiming the same id means one silently replaces the other, "
					"decided by load order. Rename one, or prefix both with their mod name."
				),
				unit=unit.stem,
			)
			continue

		seen[key] = path.name


def check_mission_catalog(unit, data, positions, catalog, local_ids=()):
	"""Rules that compare against the shipped catalogue.

	All warnings by design: an unknown value may simply be newer than the
	catalogue, and erroring on that would make the tool wrong every time the
	game gains content.
	"""

	if catalog.is_empty:
		return

	path = unit.json_path
	icon = data.get("_missionIcon")

	if isinstance(icon, str) and icon:
		if icon not in catalog.icons:
			known = ", ".join(sorted(name for name, marker in catalog.icons.items() if not marker))

			yield Finding(
				rule="mission.icon.unknown",
				severity=Severity.WARNING,
				path=path,
				line=positions.get("_missionIcon"),
				message=f'_missionIcon "{icon}" is not a known icon; the mission will show none',
				hint=f"Known mission icons: {known}",
				unit=unit.stem,
			)
		elif catalog.icons[icon]:
			yield Finding(
				rule="mission.icon.resultmarker",
				severity=Severity.WARNING,
				path=path,
				line=positions.get("_missionIcon"),
				message=f'_missionIcon "{icon}" is a result marker, not a mission type',
				hint="Success and Failure mark outcomes in the result window.",
				unit=unit.stem,
			)

	for entry in data.get("_potentialLocations") or []:
		if not isinstance(entry, dict):
			continue

		location_id = entry.get("_locationId")

		if isinstance(location_id, str) and location_id and location_id not in catalog.locations:
			yield Finding(
				rule="mission.location.unknown",
				severity=Severity.WARNING,
				path=path,
				line=positions.get("_potentialLocations"),
				message=f'_locationId "{location_id}" is not one of the predefined places',
				hint=(
					"Unless a mod defines it in Missions/Locations/, the game does not find it and "
					"places the mission at a random location."
				),
				unit=unit.stem,
			)

	# Validating the game's own content would otherwise report every mission as
	# overriding itself.
	if unit.stem in catalog.mission_ids and not _is_shipped_content(path):
		yield Finding(
			rule="mission.id.overrides",
			severity=Severity.WARNING,
			path=path,
			message=f'"{unit.stem}" replaces a mission that ships with the game',
			hint="Intentional overrides are fine; an accidental name clash is not.",
			unit=unit.stem,
		)

	# 0 RunwayTier, 1 EarliestAppearanceDay, 2 LatestAppearanceDay - all three parse their
	# value as an int with no guard, so a blank or non-numeric one throws inside the eligibility
	# check and takes the whole mission draw with it, not just this mission.
	NUMERIC_REQUIREMENT_TYPES = {0: "RunwayTier", 1: "EarliestAppearanceDay", 2: "LatestAppearanceDay"}

	for requirement in data.get("_missionRequirements") or []:
		if not isinstance(requirement, dict):
			continue

		requirement_type = requirement.get("_requirementType")

		if requirement_type in NUMERIC_REQUIREMENT_TYPES:
			raw_value = str(requirement.get("_value") or "").strip()

			if raw_value.lstrip("-").isdigit() is False:
				yield Finding(
					rule="mission.requirement.value",
					severity=Severity.ERROR,
					path=path,
					line=positions.get("_missionRequirements"),
					message=(
						f"{NUMERIC_REQUIREMENT_TYPES[requirement_type]} requirement has a"
						f' non-numeric _value ("{raw_value}")'
					),
					hint="It is parsed with int.Parse and throws, which aborts the mission draw.",
					unit=unit.stem,
				)

	for requirement in data.get("_missionRequirements") or []:
		if not isinstance(requirement, dict) or requirement.get("_requirementType") != 3:
			continue

		value = str(requirement.get("_value") or "")
		referenced = value.split(",")[0].strip()

		if referenced and referenced not in catalog.mission_ids and referenced not in local_ids:
			yield Finding(
				rule="mission.chain.unknown",
				severity=Severity.NOTE,
				path=path,
				line=positions.get("_missionRequirements"),
				message=f'chain requirement refers to "{referenced}", which is not a known mission',
				hint="Fine if that mission is part of this mod; otherwise the chain never unlocks.",
				unit=unit.stem,
			)


SHIPPED_MARKERS = ("StreamingAssets", "_DLC")


def _is_shipped_content(path):
	"""Whether this file is the game's own content rather than a mod."""

	return any(marker in path.parts for marker in SHIPPED_MARKERS)


# A mission may carry its own text in the JSON instead of a loc term. The game reads these
# through MissionData.TryGetRawText, keyed by the slot name without the leading underscore.
RAW_TEXT_FIELDS = {
	"mission_name": "_rawMissionName",
	"mission_description": "_rawMissionDescription",
	"intel_threat_report": "_rawIntelThreatReport",
	"ap_transmission": "_rawApTransmission",
	"gw_transmission": "_rawGwTransmission",
	"ap_success_transmission": "_rawApSuccessTransmission",
	"ap_failure_transmission": "_rawApFailureTransmission",
	"gw_success_transmission": "_rawGwSuccessTransmission",
	"gw_failure_transmission": "_rawGwFailureTransmission",
}


def _raw_text_slots(data):
	"""Slots the JSON answers itself, so no loc term is needed for them."""

	if not isinstance(data, dict):
		return set()

	return {slot for slot, field in RAW_TEXT_FIELDS.items() if str(data.get(field) or "").strip()}


def check_localization(unit, facts, catalog, extra_terms=frozenset(), data=None):
	"""Every mission needs nine pieces of text, whoever supplies them.

	Four sources count: raw text authored in the mission's own JSON, terms the
	mission's own script defines with SetTerm, terms already in the game's
	localisation asset, and - for a mission with no script of its own - a companion
	script elsewhere in the mod. Shipped missions define none in Python at all, so
	without the catalogue this would fire on every one of them.
	"""

	if facts is not None and (facts.mission_id_dynamic or not unit.stem):
		return

	if not unit.stem:
		return

	own_terms = {key for key, _ in facts.set_terms} if facts is not None else set()
	defined = own_terms | catalog.loc_terms | extra_terms
	defined |= {f"missions/{unit.stem}/{slot}" for slot in _raw_text_slots(data)}

	missing_mandatory = [slot for slot in MANDATORY_SLOTS if f"missions/{unit.stem}/{slot}" not in defined]
	missing_optional = [slot for slot in TRANSMISSION_SLOTS if f"missions/{unit.stem}/{slot}" not in defined]

	# Without a script of its own the JSON is the only file to point at.
	path = unit.py_path or unit.json_path

	if missing_mandatory:
		yield Finding(
			rule="mission.loc.mandatory",
			severity=Severity.ERROR,
			path=path,
			message="missing required loc key(s): " + ", ".join(missing_mandatory),
			hint=(
				f"The game builds missions/{unit.stem}/<slot> itself and shows the raw key when it "
				"is absent.\nDefine them with localization.SetTerm, either in this mission's own "
				"script or in any script the mod loads."
			),
			unit=unit.stem,
		)

	if missing_optional:
		yield Finding(
			rule="mission.loc.transmission",
			severity=Severity.WARNING,
			path=path,
			message="missing transmission loc key(s): " + ", ".join(missing_optional),
			hint="These appear in the event log during and after the flight; a missing one is a blank line.",
			unit=unit.stem,
		)


def check_event_script(unit, facts, catalog):
	"""Minor event subscriptions in an event script."""

	if catalog.is_empty:
		return

	for handler in facts.handlers:
		if handler.constant not in catalog.minor_events:
			continue

		if catalog.minor_events[handler.constant]:
			yield Finding(
				rule="event.tutorialonly",
				severity=Severity.WARNING,
				path=unit.py_path,
				line=handler.line,
				message=f"{handler.constant} only fires during the tutorial",
				hint="Tutorial-only events never fire in normal play, so this handler will not run.",
				unit=unit.stem,
			)


def check_quest(unit, data, positions, catalog):
	"""Quest JSON rules."""

	path = unit.json_path
	sub_quests = data.get("_subQuests")

	if not isinstance(sub_quests, list) or not sub_quests:
		yield Finding(
			rule="quest.subquests.missing",
			severity=Severity.ERROR,
			path=path,
			message="quest has no _subQuests, so it can never complete",
			unit=unit.stem,
		)
		sub_quests = []

	quest_id = data.get("_questId")

	if quest_id and quest_id != unit.stem:
		yield Finding(
			rule="quest.id.mismatch",
			severity=Severity.WARNING,
			path=path,
			line=positions.get("_questId"),
			message=f'_questId is "{quest_id}" but the file is named "{unit.stem}"',
			hint="The file name is what identifies the quest; _questId should match it.",
			unit=unit.stem,
		)

	# Tutorial quests legitimately use cheats; a mod quest must not.
	if data.get("_cheatsOnStart") or data.get("_completionCheats"):
		if data.get("_questType") != 2:
			yield Finding(
				rule="quest.cheats",
				severity=Severity.WARNING,
				path=path,
				line=positions.get("_cheatsOnStart") or positions.get("_completionCheats"),
				message="quest runs developer console commands",
				hint=(
					"Cheat fields are a tutorial mechanism. A quest distributed to other players "
					"should never carry them."
				),
				unit=unit.stem,
			)

	for index, sub_quest in enumerate(sub_quests):
		if not isinstance(sub_quest, dict):
			continue

		requirement = sub_quest.get("_subQuestRequirement") or {}
		requirement_type = requirement.get("_type")

		if requirement_type in catalog.unbound_quest_types:
			name = catalog.unbound_quest_types[requirement_type]

			yield Finding(
				rule="quest.requirement.novalidator",
				severity=Severity.ERROR,
				path=path,
				line=positions.get("_subQuests"),
				message=f"sub-quest {index} uses type {requirement_type} ({name}), which has no validator",
				hint="Nothing in the game evaluates it, so this sub-quest can never progress.",
				unit=unit.stem,
			)

		elif catalog.quest_types and requirement_type not in catalog.quest_types:
			# The game loads an unknown type number without complaint and then never
			# evaluates it. No error, no log, no progress - the quietest failure in the
			# quest system, so the tool has to be the one that speaks up.
			yield Finding(
				rule="quest.requirement.unknowntype",
				severity=Severity.ERROR,
				path=path,
				line=positions.get("_subQuests"),
				message=f"sub-quest {index} uses type {requirement_type}, which is not a known requirement type",
				hint="Nothing evaluates it and nothing is logged; the sub-quest stays at zero forever.",
				unit=unit.stem,
			)

		amount = requirement.get("_amount")

		if isinstance(amount, int) and amount < 0:
			yield Finding(
				rule="quest.requirement.amount",
				severity=Severity.WARNING,
				path=path,
				line=positions.get("_subQuests"),
				message=f"sub-quest {index} has a negative _amount",
				unit=unit.stem,
			)


def check_script_safety(unit, facts, path):
	"""Rules for what any mod script may contain, mission or event script alike."""

	for feature, line in facts.too_new_syntax:
		yield Finding(
			rule="script.syntax.too_new",
			severity=Severity.ERROR,
			path=path,
			line=line,
			message=f"uses {feature}, which the game's Python (IronPython 3.4) cannot read",
			hint="The whole file is skipped by the game. Use syntax from Python 3.6 or older; f-strings are fine.",
			unit=unit.stem,
		)

	for what, line in facts.risky_uses:
		yield Finding(
			rule="script.unsafe",
			severity=Severity.WARNING,
			path=path,
			line=line,
			message=f"uses {what}, which reaches outside the game",
			hint=(
				"Mod scripts run without a sandbox, so this could touch files, processes or the "
				"network on the player's computer. A mod never needs it, and players are told to "
				"distrust scripts that do this. Use the game's scripting API instead."
			),
			unit=unit.stem,
		)

	if facts.uses_script_data_path:
		return

	for what, line in facts.file_uses:
		yield Finding(
			rule="script.file_access",
			severity=Severity.NOTE,
			path=path,
			line=line,
			message=f"uses {what} without game_api.GetScriptDataPath",
			hint=(
				"The one legitimate reason for file access is keeping your mod's own state in the "
				"folder game_api.GetScriptDataPath(\"<your id>\") returns. Anything else touches the "
				"player's computer outside the game."
			),
			unit=unit.stem,
		)
