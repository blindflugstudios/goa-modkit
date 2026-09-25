# The Airfield Chain, part 2 of 4 - you follow them home.
#
# Unlocked by airfield_raid succeeding, through its JSON requirement
# ("_requirementType": 3, value "airfield_raid,success"). The chain lives entirely in
# the JSON; this script only carries the text and the rolls.
#
# See airfield_raid.py for how the sequence fits together.

from Blindflug.FlightMission import MissionEvent

MISSION_ID = "airfield_pursuit"


def _define(slot, text):
	localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


def _term(slot):
	return "missions/{}/{}".format(MISSION_ID, slot)


_define("mission_name", "Follow Them Back")
_define(
	"mission_description",
	"They are running for France with empty racks and tired gunners, and for once we "
	"know exactly where they are going. Follow them across, stay with them as long as "
	"the fuel allows, and see how far they lead us."
)
_define(
	"intel_threat_report",
	"Six or more, low over the water and making for the French coast. Their escort "
	"broke off over the Strait. This is the only hour of the day they are weak."
)
_define(
	"ap_transmission",
	"Still with them, four thousand feet, coast ahead. They have not seen us."
)
_define(
	"gw_transmission",
	"Lost them in the haze over the water. Casting about on a guess and a compass "
	"heading."
)
_define(
	"ap_success_transmission",
	"Followed them all the way in and watched them go down onto a strip that is not on "
	"any of our maps. We have a heading and a rough position. That is more than we had "
	"this morning."
)
_define(
	"ap_failure_transmission",
	"Stayed with them until the fuel gauges made the decision for us. They went inland "
	"and we turned for home with nothing but a compass bearing."
)
_define(
	"gw_success_transmission",
	"Lost them, found them again by luck and the smoke of a bad engine, and saw where "
	"they put down. Not elegant, but we have a direction."
)
_define(
	"gw_failure_transmission",
	"Lost them over the water and never regained contact. Wherever they came from, it "
	"is still ours to find."
)
_define("cancelled", "Pursuit called off. They are long gone by now.")


@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
	return MISSION_ID


@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
	events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)

	if events_sent == 1:
		as_planned = missions_api.MakeAsPlannedRoll(mission_entity_id)
		event_log.Create(_term("ap_transmission" if as_planned else "gw_transmission"))

	elif events_sent == 2:
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
	as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
	successful = missions_api.IsMissionSuccessful(mission_entity_id)

	if as_planned:
		return _term("ap_success_transmission" if successful else "ap_failure_transmission")

	return _term("gw_success_transmission" if successful else "gw_failure_transmission")
