# Night Interception - a worked example of what a mission script is for.
#
# ---------------------------------------------------------------------------
# HOW THIS FILE RUNS
#
# This is not a program that runs top to bottom. It is a set of functions the
# game calls at fixed moments during a flight. You never call them yourself.
#
#   @event_handler(SOMETHING)     "call this function when SOMETHING happens"
#   def my_function(mission_entity_id):
#
# Everything OUTSIDE a handler - the constants and the SetTerm calls below -
# runs once, when the game loads this file at startup. Everything INSIDE a
# handler runs during a flight, possibly for several flights at once.
#
# For one flight the game calls, in this order:
#
#   INITIALIZE_MISSION        once, when the mission appears
#   SEND_MISSION_EVENT        three times, spread across the flight
#   SET_MISSION_IMPACT        once, after the outcome is decided
#   SEND_MISSION_RESULT_EVENT once, the closing line in the event log
#   GET_MISSION_RESULT_TEXT   when the player opens the result window
#
# ---------------------------------------------------------------------------
# WHAT THIS MISSION DOES THAT JSON CANNOT
#
# A night intercept is about the crew, not the aircraft. So this script:
#
#   1. remembers who flew, per flight, and how tired they already were
#   2. varies its radio traffic by how exhausted the crew is
#   3. after landing, hands out consequences per pilot rather than per mission -
#      the tired ones lose more than the fresh ones, and a first night kill is
#      worth more to a green pilot than to a veteran
#
# None of that is expressible in the JSON, which only knows flat numbers.
#
# ---------------------------------------------------------------------------

from Blindflug.FlightMission import MissionEvent
from Blindflug.Game.Characters.Morale import MoraleCategory

MISSION_ID = "night_interception"

# Below this energy a pilot counts as flying tired, and the mission says so.
TIRED_ENERGY = 40.0

# A pilot with fewer sorties than this has probably never flown at night.
FIRST_NIGHT_SORTIES = 5

# What a night flight costs everyone aboard, on top of the JSON's outcome effects.
NIGHT_FATIGUE = -8.0

# What it costs a pilot who was already tired before taking off.
EXHAUSTED_EXTRA_FATIGUE = -12.0

# Confidence a green pilot gains from surviving their first night interception.
FIRST_NIGHT_CONFIDENCE = 20.0


def _term(slot):
	return "missions/{}/{}".format(MISSION_ID, slot)


def _define(slot, text):
	localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


# --- Text -------------------------------------------------------------------
#
# Registered once at load. A mission's JSON has nine _raw* slots and no more; a
# script has no such limit, which is the whole reason this mission has a script.

_define("mission_name", "Night Interception")
_define(
	"mission_description",
	"Bombers are crossing the coast in the dark, and the sector controller has nothing but "
	"a plot on a table and a voice on the radio to put you near them. Whoever goes up will "
	"be flying on instruments, alone, with no horizon to speak of."
)
_define(
	"intel_threat_report",
	"Three aircraft, heading north-west, height uncertain. Finding them is most of the job. "
	"Landing afterwards is the rest of it."
)

_define("rested_departure", "Airborne and climbing. Cockpit dark, eyes adjusting. Standing by for a vector.")
_define("tired_departure", "Airborne. Some of us have been up since before dawn and it shows already.")
_define(
	"exhausted_departure",
	"Airborne, barely. Nobody in this flight has any business being in the air tonight."
)

_define("ap_transmission", "Vector was good - contact ahead and slightly below. Closing quietly.")
_define("gw_transmission", "Lost the vector in cloud. Searching blind and burning fuel doing it.")

_define(
	"ap_success_transmission",
	"One bomber down in the Channel, the rest turned back before they reached the coast. "
	"Everyone home and on the ground in one piece."
)
_define(
	"ap_failure_transmission",
	"Found them, closed on them, and could not hold the contact long enough to finish it. "
	"They went on inland."
)
_define(
	"gw_success_transmission",
	"Half the night spent chasing a plot that was never there - and then one of them flew "
	"straight across us on the way home. Nobody is more surprised than we are."
)
_define(
	"gw_failure_transmission",
	"Two hours in the dark for nothing at all. The bombers got through and the crews are "
	"finished."
)

_define("cancelled", "Interception scrubbed before take-off. Nobody is complaining.")


# --- Reading the crew -------------------------------------------------------
#
# Every handler is given mission_entity_id: the mission this call is about. The
# api answers questions about it. Nothing is stored between calls in a global -
# two flights of the same mission can be in the air at the same time.


def _pilots(mission_entity_id):
	"""Every pilot assigned to this flight, as character ids."""
	pilots = []

	for airplane_id in missions_api.GetMissionAirplaneFormation(mission_entity_id):
		pilot = airplanes_api.GetPilot(airplane_id)

		if pilot:
			pilots.append(pilot)

	return pilots


def _tired_pilots(mission_entity_id):
	"""Those already low on energy before the flight even started."""
	return [
		pilot for pilot in _pilots(mission_entity_id)
		if characters_api.GetMorale(pilot, MoraleCategory.Energy) < TIRED_ENERGY
	]


def _departure_slot(mission_entity_id):
	"""Which of the three departure lines fits this crew."""
	pilots = _pilots(mission_entity_id)
	tired = _tired_pilots(mission_entity_id)

	if not pilots or not tired:
		return "rested_departure"

	if len(tired) == len(pilots):
		return "exhausted_departure"

	return "tired_departure"


# --- Handlers ---------------------------------------------------------------


@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
	"""Required of every mission script. Must return exactly this file's name."""
	return MISSION_ID


@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
	"""Called once per progress step - three times over a JSON mission's flight.

	Nothing tells the handler which step this is, so it asks. Step 1 rolls
	whether the intercept develops as briefed, step 2 rolls whether the crew can
	convert it. Both rolls happen exactly once; everything later reads them back.
	"""
	events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)

	if events_sent == 1:
		missions_api.MakeAsPlannedRoll(mission_entity_id)
		event_log.Create(_term(_departure_slot(mission_entity_id)))

	elif events_sent == 2:
		as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
		event_log.Create(_term("ap_transmission" if as_planned else "gw_transmission"))
		missions_api.MakeSkillRoll(mission_entity_id)


@event_handler(MissionEvent.SET_MISSION_IMPACT)
def set_mission_impact(mission_entity_id):
	"""Called after the outcome is decided, before the result is shown.

	The JSON's outcome effects have already been applied to the whole squadron by
	this point. This is where a script adds what the JSON cannot express: effects
	that differ from one pilot to the next.
	"""
	successful = missions_api.IsMissionSuccessful(mission_entity_id)
	tired = _tired_pilots(mission_entity_id)

	for pilot in _pilots(mission_entity_id):
		# Flying at night costs everyone; it costs the already-tired far more.
		fatigue = EXHAUSTED_EXTRA_FATIGUE if pilot in tired else NIGHT_FATIGUE
		characters_api.ModifyMorale(pilot, MoraleCategory.Energy, fatigue)

		# Surviving a first night interception is worth more to someone who has
		# not done it before.
		is_green = characters_api.GetPilotMissionCount(pilot) < FIRST_NIGHT_SORTIES

		if successful and is_green:
			characters_api.ModifyMorale(pilot, MoraleCategory.Confidence, FIRST_NIGHT_CONFIDENCE)


@event_handler(MissionEvent.SEND_MISSION_RESULT_EVENT)
def send_mission_result_text(mission_entity_id):
	"""The closing line in the event log."""
	event_log.Create(_result_term(mission_entity_id))


@event_handler(MissionEvent.GET_MISSION_RESULT_TEXT)
def get_mission_result_text(mission_entity_id):
	"""Which text the result window shows. Returns a key, not a sentence."""
	return _result_term(mission_entity_id)


@event_handler(MissionEvent.SEND_MISSION_CANCELLED_EVENT)
def send_mission_cancelled_text(mission_entity_id):
	event_log.Create(_term("cancelled"))


def _result_term(mission_entity_id):
	"""The four endings, picked the same way the JSON's four outcomes are.

	Both handlers that report the result go through here, so the event log and
	the result window can never disagree with one another.
	"""
	as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
	successful = missions_api.IsMissionSuccessful(mission_entity_id)

	if as_planned:
		return _term("ap_success_transmission" if successful else "ap_failure_transmission")

	return _term("gw_success_transmission" if successful else "gw_failure_transmission")
