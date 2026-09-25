# The Airfield Chain, part 3 of 4 - you go looking.
#
# Unlocked by airfield_pursuit succeeding, through its JSON requirement
# ("_requirementType": 3, value "airfield_pursuit,success"). The chain lives entirely in
# the JSON; this script only carries the text and the rolls.
#
# See airfield_raid.py for how the sequence fits together.

from Blindflug.FlightMission import MissionEvent

MISSION_ID = "airfield_search"


def _define(slot, text):
	localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


def _term(slot):
	return "missions/{}/{}".format(MISSION_ID, slot)


_define("mission_name", "Somewhere Near Amiens")
_define(
	"mission_description",
	"A heading and a rough position are not a target. Two aircraft, cameras, and as "
	"much of the countryside as the light allows. Find the strip they are flying from, "
	"photograph it, and get the film home."
)
_define(
	"intel_threat_report",
	"Deep over occupied territory in daylight, alone, and the whole point is to be "
	"somewhere long enough to look at it. There will be fighters."
)
_define(
	"ap_transmission",
	"Feet dry over the coast, cameras running. Nothing below but fields and hedgerows "
	"so far."
)
_define(
	"gw_transmission",
	"Cloud is lower than briefed and we are down to two thousand to see anything at "
	"all. Every gun in France can see us too."
)
_define(
	"ap_success_transmission",
	"Found it. A grass strip with dispersal pens under the treeline, thirty-odd "
	"aircraft, fuel bowsers in the open. The film is home and the interpreters have it "
	"now."
)
_define(
	"ap_failure_transmission",
	"Flew the whole search pattern and photographed a great deal of farmland. Whatever "
	"is down there, it was under something when we passed over it."
)
_define(
	"gw_success_transmission",
	"Half blind in the cloud and one camera jammed, and we still came back with the "
	"strip on film. Somebody was owed some luck."
)
_define(
	"gw_failure_transmission",
	"Nothing but cloud and flak. The film is worthless and we are no closer than we "
	"were."
)
_define("cancelled", "Reconnaissance scrubbed. The weather made the decision.")


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
