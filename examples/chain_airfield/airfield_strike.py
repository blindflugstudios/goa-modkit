# The Airfield Chain, part 4 of 4 - you finish it.
#
# Unlocked by airfield_search succeeding, through its JSON requirement
# ("_requirementType": 3, value "airfield_search,success"). The chain lives entirely in
# the JSON; this script only carries the text and the rolls.
#
# See airfield_raid.py for how the sequence fits together.

from Blindflug.FlightMission import MissionEvent

MISSION_ID = "airfield_strike"


def _define(slot, text):
	localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


def _term(slot):
	return "missions/{}/{}".format(MISSION_ID, slot)


_define("mission_name", "Return the Favour")
_define(
	"mission_description",
	"Everything that has happened this week ends here. The strip is photographed, the "
	"pens are marked, and the bowsers were still in the open when we last looked. Take "
	"everything that will fly and settle the account."
)
_define(
	"intel_threat_report",
	"They will be expecting this eventually - the question is whether eventually is "
	"today. Eight or more fighters on the field, and flak that was not there in the "
	"photographs."
)
_define(
	"ap_transmission",
	"On the run-in, target ahead exactly where the photographs put it. Bomb doors open."
)
_define(
	"gw_transmission",
	"Flak is heavier than briefed and we are scattered before the run-in. Reforming as "
	"best we can."
)
_define(
	"ap_success_transmission",
	"Pens burning, two bowsers gone up and taken the treeline with them, and the strip "
	"is cratered end to end. Nothing is flying out of there this week. The account is "
	"settled."
)
_define(
	"ap_failure_transmission",
	"A good run onto the wrong end of the field. Some damage, nothing decisive, and "
	"they will be operating again in a day or two."
)
_define(
	"gw_success_transmission",
	"Broken formation, half the bombs long, and one direct hit on the fuel dump that "
	"did the work of all the rest. We will take it."
)
_define(
	"gw_failure_transmission",
	"Scattered by the flak, bombed on guesswork, and came home lighter than we went "
	"out. They are still there and now they know we know."
)
_define("cancelled", "Strike scrubbed. The account stays open.")


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
