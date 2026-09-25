# Greenhorn Watch - the ace is in hospital and the new intake has to fly.
#
# The JSON next to this file carries the stats, outcomes and timings. This script does the
# two things JSON cannot: it looks at who actually climbed into the cockpit, and it writes
# its own text for what it finds there.
#
# On text. A mission's JSON has nine _raw* slots and no more, so a mission without a script
# is limited to those nine lines. A script is not: localization.SetTerm registers any term
# at load time, into a separate store the game keeps for script text - the game's own
# translation files are never touched. That is how the game's own event scripts supply
# their text, and it is how a mod ships text without shipping localisation files.
#
# Terms are registered at module level, once when the script loads, not per flight.

from Blindflug.FlightMission import MissionEvent

MISSION_ID = "greenhorn_watch"

# A pilot with fewer sorties than this behind them is still learning.
GREENHORN_SORTIES = 3

# How many green pilots it takes before the flight reads as inexperienced.
GREEN_FLIGHT_THRESHOLD = 2


def _term(suffix):
	return "missions/{}/{}".format(MISSION_ID, suffix)


# Text of this mission's own, beyond the nine slots the JSON can hold. Prefixed with the
# mission id so it cannot collide with another mod's terms.
localization.SetTerm("en", _term("green_departure"),
	"Formation is all over the sky. Half of them have never done this without an instructor on the wing.")
localization.SetTerm("en", _term("veteran_departure"),
	"Angels one-five, formation tight, sector quiet so far. Continuing the sweep.")
localization.SetTerm("en", _term("green_contact"),
	"Contact - and someone has already broken formation. Close up, close up!")
localization.SetTerm("en", _term("veteran_contact"),
	"Contact, three o'clock low. Breaking to engage.")
localization.SetTerm("en", _term("green_success"),
	"It was a shambles from start to finish, and they still came back. Every one of them.")
localization.SetTerm("en", _term("green_failure"),
	"We sent boys up against professionals. That is on us, not on them.")
localization.SetTerm("en", _term("veteran_success"),
	"Patrol flown, sector clear, all aircraft accounted for.")
localization.SetTerm("en", _term("veteran_failure"),
	"We held formation and still came off worse. A bad day - it happens to good pilots too.")
localization.SetTerm("en", _term("cancelled"),
	"Patrol scrubbed. Small mercies - they were not ready anyway.")


def _count_greenhorns(mission_entity_id):
	"""How many assigned pilots are still on their first few sorties."""
	green = 0

	for airplane_id in missions_api.GetMissionAirplaneFormation(mission_entity_id):
		pilot = airplanes_api.GetPilot(airplane_id)

		if pilot and characters_api.GetPilotMissionCount(pilot) < GREENHORN_SORTIES:
			green += 1

	return green


def _is_green_flight(mission_entity_id):
	return _count_greenhorns(mission_entity_id) >= GREEN_FLIGHT_THRESHOLD


def _prefix(mission_entity_id):
	return "green" if _is_green_flight(mission_entity_id) else "veteran"


@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
	return MISSION_ID


@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
	events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)
	prefix = _prefix(mission_entity_id)

	# Roll in the first in-flight event only; everything after this reads the stored roll.
	if events_sent == 1:
		missions_api.MakeAsPlannedRoll(mission_entity_id)
		event_log.Create(_term(prefix + "_departure"))

	elif events_sent == 2:
		event_log.Create(_term(prefix + "_contact"))
		missions_api.MakeSkillRoll(mission_entity_id)


@event_handler(MissionEvent.SEND_MISSION_RESULT_EVENT)
def send_mission_result_text(mission_entity_id):
	event_log.Create(_result_term(mission_entity_id))


@event_handler(MissionEvent.GET_MISSION_RESULT_TEXT)
def get_mission_result_text(mission_entity_id):
	return _result_term(mission_entity_id)


@event_handler(MissionEvent.SEND_MISSION_CANCELLED_EVENT)
def send_mission_cancelled_text(mission_entity_id):
	event_log.Create(_term("cancelled"))


def _result_term(mission_entity_id):
	outcome = "success" if missions_api.IsMissionSuccessful(mission_entity_id) else "failure"

	return _term("{}_{}".format(_prefix(mission_entity_id), outcome))
