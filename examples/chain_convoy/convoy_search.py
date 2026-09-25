# Step 2b - search again (after a FAILURE)
#
# Part of the convoy chain. See README.md in this folder for the branching structure.

from Blindflug.FlightMission import MissionEvent

MISSION_ID = "convoy_search"


def _term(slot, text):
    localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


_term("mission_name", "Renewed Search")
_term("mission_description", "The first sweep found nothing. Fly the strait again, further out.")
_term("intel_threat_report", "Low. Still no escort reported, but the weather is worsening.")

_term("ap_transmission", "Second sweep under way, further out to sea this time.")
_term("gw_transmission", "Weather closed in again. Visibility is poor.")
_term("ap_success_transmission", "Found them. The convoy had swung wide to avoid the earlier patrol.")
_term("ap_failure_transmission", "A second empty sweep. The trail has gone cold.")
_term("gw_success_transmission", "Flying almost on the water, the flight finally spotted the convoy.")
_term("gw_failure_transmission", "Two sweeps, nothing to show. The convoy has slipped through.")


@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
    return MISSION_ID


@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
    events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)

    if events_sent == 1:
        going_as_planned = missions_api.MakeAsPlannedRoll(mission_entity_id)
        slot = "ap_transmission" if going_as_planned else "gw_transmission"
        event_log.Create("missions/{}/{}".format(MISSION_ID, slot))

    elif events_sent == 2:
        going_as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
        skill_passed = missions_api.MakeSkillRoll(mission_entity_id)
        event_log.Create("missions/{}/{}".format(
            MISSION_ID, _result_slot(going_as_planned, skill_passed)))


@event_handler(MissionEvent.GET_MISSION_RESULT_TEXT)
def get_mission_result_text(mission_entity_id):
    going_as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
    skill_passed = missions_api.GetSkillRoll(mission_entity_id)

    return "missions/{}/{}".format(MISSION_ID, _result_slot(going_as_planned, skill_passed))


def _result_slot(going_as_planned, skill_passed):
    prefix = "ap" if going_as_planned else "gw"
    suffix = "success" if skill_passed else "failure"

    return "{}_{}_transmission".format(prefix, suffix)
