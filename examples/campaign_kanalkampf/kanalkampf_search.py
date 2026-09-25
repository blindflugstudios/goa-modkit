# Kanalkampf, part 3 - you go looking for the field.
#
# Handed out by kanalkampf_pursuit once two crossings have succeeded. Records
# the find in the campaign state, which is what makes the strike possible - and
# what stops the search being offered again once it has worked.

from Blindflug.FlightMission import MissionEvent

import campaign_state

MISSION_ID = "kanalkampf_search"


def _define(slot, text):
	localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


def _term(slot):
	return "missions/{}/{}".format(MISSION_ID, slot)


_define("mission_name", "Somewhere South of Amiens")
_define(
	"mission_description",
	"Two crossings have given us a direction and a rough area. Two aircraft, cameras, and "
	"as much daylight as we can use. Find the strip, photograph it, and bring the film "
	"home."
)
_define(
	"intel_threat_report",
	"Deep over occupied country in daylight, and the whole job is to loiter somewhere "
	"long enough to look at it properly."
)
_define("ap_transmission", "Feet dry, cameras running, working the search pattern west to east.")
_define(
	"gw_transmission",
	"Cloud lower than briefed. Down to two thousand to see anything, and everyone below "
	"can see us."
)
_define(
	"ap_success_transmission",
	"Found it. Grass strip, dispersal pens under the treeline, bowsers in the open. The "
	"film is home and the interpreters have it."
)
_define(
	"ap_failure_transmission",
	"Flew the whole pattern and photographed a great deal of farmland. Whatever is down "
	"there was under cover when we passed."
)
_define(
	"gw_success_transmission",
	"Half blind in cloud, one camera jammed, and we still came back with the strip on "
	"film."
)
_define(
	"gw_failure_transmission",
	"Cloud and flak and nothing to show. We are no closer than we were this morning."
)
_define("cancelled", "Reconnaissance scrubbed. The weather decided.")

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
	if missions_api.IsMissionSuccessful(mission_entity_id) == False:
		return

	campaign_state.set_value("airfield_found", True)
	missions_api.CreateMission("kanalkampf_strike")


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
