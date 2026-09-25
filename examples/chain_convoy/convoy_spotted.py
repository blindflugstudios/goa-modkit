# Step 1 - find the convoy
#
# Part of the convoy chain. See README.md in this folder for the branching structure.

from Blindflug.FlightMission import MissionEvent

MISSION_ID = "convoy_spotted"


def _term(slot, text):
    localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


_term("mission_name", "Convoy Sighting")
_term("mission_description", "Naval intelligence suspects a supply convoy crossing the strait. Find it.")
_term("intel_threat_report", "Low. No fighter escort expected on a reconnaissance run.")

_term("ap_transmission", "The flight is over open water, sweeping the strait in clear conditions.")
_term("gw_transmission", "Haze over the water. The flight is searching blind.")
_term("ap_success_transmission", "Convoy located and photographed. Six vessels, heading south-west.")
_term("ap_failure_transmission", "Nothing found. Either the intelligence was wrong or the convoy has passed.")
_term("gw_success_transmission", "Despite the haze the flight caught the wakes and brought back a position.")
_term("gw_failure_transmission", "The flight came home with nothing but grey photographs.")


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
