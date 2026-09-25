# Kanalkampf, part 4 - the account is settled.
#
# The finale, handed out by kanalkampf_search on success. Reads the whole
# campaign record for its closing line: a squadron that lost raids on the way
# here gets a different ending from one that never did.
#
# On success it marks the campaign finished, so the arc does not loop.

from Blindflug.FlightMission import MissionEvent

import campaign_state

MISSION_ID = "kanalkampf_strike"


def _define(slot, text):
	localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


def _term(slot):
	return "missions/{}/{}".format(MISSION_ID, slot)


_define("mission_name", "Return the Favour")
_define(
	"mission_description",
	"Everything this week has led here. The strip is photographed, the pens are marked, "
	"and the bowsers were in the open when we last looked. Take everything that will fly."
)
_define(
	"intel_threat_report",
	"Eight or more fighters on the field, and flak that was not in the photographs. They "
	"will be expecting this eventually - the question is whether eventually is today."
)
_define(
	"ap_transmission",
	"On the run-in, target exactly where the photographs put it. Bomb doors open."
)
_define(
	"gw_transmission",
	"Flak heavier than briefed and we are scattered before the run-in. Reforming as we "
	"can."
)
_define(
	"ap_success_transmission",
	"Pens burning, two bowsers gone up and taken the treeline with them, strip cratered "
	"end to end. Nothing flies out of there this week."
)
_define(
	"ap_failure_transmission",
	"A good run onto the wrong end of the field. Some damage, nothing decisive. They will "
	"be operating again in a day or two."
)
_define(
	"gw_success_transmission",
	"Broken formation, half the bombs long, and one direct hit on the fuel dump that did "
	"the work of all the rest."
)
_define(
	"gw_failure_transmission",
	"Scattered by flak, bombed on guesswork, and home lighter than we went out. They are "
	"still there, and now they know we know."
)
_define("cancelled", "Strike scrubbed. The account stays open.")
_define("hard_won", "It cost us more than it should have to get here. Nobody is cheering.")
_define(
	"clean_sweep",
	"Not one raid lost getting here. They will be a long time working out what happened."
)

@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
	events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)

	if events_sent == 1:
		as_planned = missions_api.MakeAsPlannedRoll(mission_entity_id)
		event_log.Create(_term("ap_transmission" if as_planned else "gw_transmission"))

	elif events_sent == 2:
		missions_api.MakeSkillRoll(mission_entity_id)


@event_handler(MissionEvent.SET_MISSION_IMPACT)
def set_mission_impact(mission_entity_id):
	"""The closing line depends on the whole week, not on this one flight."""
	if missions_api.IsMissionSuccessful(mission_entity_id) == False:
		return

	campaign_state.set_value("airfield_struck", True)

	if campaign_state.get("raids_lost") > 0:
		event_log.Create(_term("hard_won"))
	else:
		event_log.Create(_term("clean_sweep"))


@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
	return MISSION_ID


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
