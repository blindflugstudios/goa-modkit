# Kanalkampf, part 2 - the counterattack.
#
# Handed out by kanalkampf_raid after a raid you won. Two things it does that
# the raid does not:
#
#   * it names the pilot who won the first raid, if there was one, so the
#     campaign refers back to something the player actually did
#   * it counts itself, and the second successful pursuit is what opens the
#     search - two crossings are what it takes to be sure where they come from
#
# The second point is the shape of a campaign rather than a chain: the condition
# is "twice", and no JSON requirement can count.

from Blindflug.FlightMission import MissionEvent

import campaign_state

MISSION_ID = "kanalkampf_pursuit"

# How many successful crossings it takes before the airfield can be searched for.
PURSUITS_BEFORE_SEARCH = 2


def _define(slot, text):
	localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


def _term(slot):
	return "missions/{}/{}".format(MISSION_ID, slot)


_define("mission_name", "Across the Strait")
_define(
	"mission_description",
	"They are going home light and slow, and for the first time this week we have the fuel "
	"and the daylight to follow. Cross with them, stay high, and see how far south they go."
)
_define(
	"intel_threat_report",
	"Six or so, low over the water, escort already turned back. This is the one hour of the "
	"day they cannot fight properly."
)

_define("first_pursuit", "First time we have gone after them. Crossing the coast now.")
_define("second_pursuit", "Second crossing this week. We are starting to know this water.")
# [character:{[PILOT]}] is how a script names a person: the game resolves the id
# into the name the player knows, and links it in the event log.
_define(
	"led_by_veteran",
	"[character:{[PILOT]}] is leading - the one who broke up the first raid. The others are "
	"following closely."
)

_define("ap_transmission", "Still with them, four thousand feet, French coast ahead.")
_define("gw_transmission", "Lost them in the haze. Casting about on a compass heading and a guess.")

_define(
	"ap_success_transmission",
	"Followed them all the way in and watched them descend somewhere south of Amiens. Not a "
	"position yet - but a direction, and that is new."
)
_define(
	"ap_failure_transmission",
	"Stayed with them until the fuel decided for us. They went inland and we turned back."
)
_define(
	"gw_success_transmission",
	"Lost them, found them again by the smoke of a bad engine, and saw roughly where they "
	"put down."
)
_define(
	"gw_failure_transmission",
	"Never regained contact. Wherever they fly from, it is still ours to find."
)

_define("cancelled", "Pursuit called off. They are long gone.")


@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
	return MISSION_ID


@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
	events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)

	if events_sent == 1:
		state = campaign_state.load()

		if state["pursuits_flown"] == 0:
			event_log.Create(_term("first_pursuit"))
		else:
			event_log.Create(_term("second_pursuit"))

		# Name the pilot who won the first raid, if they are aboard this one.
		veteran = state["first_blood"]

		if veteran is not None and _is_aboard(mission_entity_id, veteran):
			event_log.Create(_term("led_by_veteran"), {"PILOT": str(veteran)})

		as_planned = missions_api.MakeAsPlannedRoll(mission_entity_id)
		event_log.Create(_term("ap_transmission" if as_planned else "gw_transmission"))

	elif events_sent == 2:
		missions_api.MakeSkillRoll(mission_entity_id)


@event_handler(MissionEvent.SET_MISSION_IMPACT)
def set_mission_impact(mission_entity_id):
	if missions_api.IsMissionSuccessful(mission_entity_id) == False:
		return

	pursuits = campaign_state.bump("pursuits_flown")

	# Two crossings are what it takes to be sure. A JSON requirement can ask
	# whether a mission succeeded; it cannot ask whether it succeeded twice.
	if pursuits >= PURSUITS_BEFORE_SEARCH and campaign_state.get("airfield_found") == False:
		missions_api.CreateMission("kanalkampf_search")


@event_handler(MissionEvent.SEND_MISSION_RESULT_EVENT)
def send_mission_result_text(mission_entity_id):
	event_log.Create(_result_term(mission_entity_id))


@event_handler(MissionEvent.GET_MISSION_RESULT_TEXT)
def get_mission_result_text(mission_entity_id):
	return _result_term(mission_entity_id)


@event_handler(MissionEvent.SEND_MISSION_CANCELLED_EVENT)
def send_mission_cancelled_text(mission_entity_id):
	event_log.Create(_term("cancelled"))


def _is_aboard(mission_entity_id, character_id):
	for airplane_id in missions_api.GetMissionAirplaneFormation(mission_entity_id):
		if airplanes_api.GetPilot(airplane_id) == character_id:
			return True

	return False


def _result_term(mission_entity_id):
	as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
	successful = missions_api.IsMissionSuccessful(mission_entity_id)

	if as_planned:
		return _term("ap_success_transmission" if successful else "ap_failure_transmission")

	return _term("gw_success_transmission" if successful else "gw_failure_transmission")
