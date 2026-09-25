# Kanalkampf, part 2b - picking the squadron up off the floor.
#
# Handed out by kanalkampf_raid after three lost raids. Not a counterattack -
# a quiet flight for a squadron that has stopped believing it can win.
#
# The one thing it does that JSON cannot: it reads the campaign's record of
# defeats and says the number out loud, and on success it forgives one of them,
# so the squadron can climb back out of the hole rather than being stuck in it.

from Blindflug.FlightMission import MissionEvent

import campaign_state

MISSION_ID = "kanalkampf_regroup"


def _define(slot, text):
	localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


def _term(slot):
	return "missions/{}/{}".format(MISSION_ID, slot)


_define("mission_name", "Regroup")
_define(
	"mission_description",
	"Three mornings in a row we have come off worse, and it shows in every face on this "
	"field. A short flight, close to home, nothing to prove. Get them back in the air "
	"before they forget how."
)
_define("intel_threat_report", "Nothing expected. That is rather the point.")
_define("ap_transmission", "Formation tight over the Downs. Quiet up here for once.")
_define(
	"gw_transmission",
	"Even this is going badly. Somebody is flying like they would rather be anywhere "
	"else."
)
_define(
	"ap_success_transmission",
	"A clean flight, a clean landing, and the first laughter in the mess for three days. "
	"It counts for more than the flying did."
)
_define("ap_failure_transmission", "Uneventful, and nobody came back looking any better than they went out.")
_define(
	"gw_success_transmission",
	"It started badly and they pulled it round themselves. That is worth more than if it "
	"had gone smoothly."
)
_define(
	"gw_failure_transmission",
	"A shambles even with nobody shooting at us. This will take longer than one flight."
)
_define("cancelled", "Stood down. Perhaps that is what they needed anyway.")
_define("morale_bad", "Three raids lost this week. Nobody says it, but everybody is counting.")

@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
	events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)

	if events_sent == 1:
		# Say the number out loud. The JSON has no idea there is a number.
		if campaign_state.get("raids_lost") >= 3:
			event_log.Create(_term("morale_bad"))

		as_planned = missions_api.MakeAsPlannedRoll(mission_entity_id)
		event_log.Create(_term("ap_transmission" if as_planned else "gw_transmission"))

	elif events_sent == 2:
		missions_api.MakeSkillRoll(mission_entity_id)


@event_handler(MissionEvent.SET_MISSION_IMPACT)
def set_mission_impact(mission_entity_id):
	"""A squadron that pulls itself together gets one defeat back.

	Without this the campaign is a trap: three losses open the regroup, and nothing
	ever closes it again."""
	if missions_api.IsMissionSuccessful(mission_entity_id) == False:
		return

	state = campaign_state.load()
	state["raids_lost"] = max(0, state["raids_lost"] - 1)
	campaign_state.save(state)


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
