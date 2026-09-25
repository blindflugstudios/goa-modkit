# Step 2a - strike the convoy (after a SUCCESS)
#
# Part of the convoy chain. See README.md in this folder for the branching structure.

from Blindflug.FlightMission import MissionEvent

MISSION_ID = "convoy_strike"


def _term(slot, text):
    localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


_term("mission_name", "Convoy Strike")
_term("mission_description", "The convoy has been located. Hit it before it reaches port.")
_term("intel_threat_report", "High. Expect flak and a fighter escort over the target.")

_term("ap_transmission", "The flight is running in on the convoy at low level.")
_term("gw_transmission", "Flak found the formation early. The run is going badly.")
_term("ap_success_transmission", "Two vessels burning, one dead in the water. A clean strike.")
_term("ap_failure_transmission", "Bombs fell wide. The convoy sails on untouched.")
_term("gw_success_transmission", "Battered on the approach, the flight still put a bomb into the lead ship.")
_term("gw_failure_transmission", "The formation broke under fire and jettisoned its load into open water.")


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
