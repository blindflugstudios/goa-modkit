# my_mod_patrol - mission template.
#
# The JSON file next to this script holds the numbers: stats, location, the four
# outcomes and the timings. This script holds the text and what the crew radios in.
#
# Rename checklist when you copy this template:
#   1. Rename both files (my_mod_patrol.json and my_mod_patrol.py) to your mission id.
#   2. Change MISSION_ID below to exactly the same id.
#   3. Replace "my_mod" with your own mod id everywhere.

from Blindflug.FlightMission import MissionEvent

MISSION_ID = "my_mod_patrol"


def _term(slot, text):
    localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


# The first three are shown in the mission window and must always exist.
_term("mission_name", "Coastal Patrol")
_term("mission_description",
      "Fly the shoreline near Dover. Report anything that moves on the water.")
_term("intel_threat_report", "Low. No enemy activity reported this week.")

# Sent while the flight is in the air.
_term("ap_transmission", "Patrol airborne. Visibility good along the coast.")
_term("gw_transmission", "Cloud thicker than forecast. Flight feeling its way along the shore.")

# The four endings.
_term("ap_success_transmission", "Patrol complete. Nothing to report.")
_term("ap_failure_transmission", "Route flown, nothing useful observed. Fuel spent for little.")
_term("gw_success_transmission", "Despite the weather the flight held course and brought back a full report.")
_term("gw_failure_transmission", "Flight lost the coastline in the murk and turned back early.")


@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
    return MISSION_ID


@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
    # Called three times per flight. Roll once, then only read the stored roll.
    events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)

    if events_sent == 1:
        going_as_planned = missions_api.MakeAsPlannedRoll(mission_entity_id)
        slot = "ap_transmission" if going_as_planned else "gw_transmission"
        event_log.Create("missions/{}/{}".format(MISSION_ID, slot))

    elif events_sent == 2:
        going_as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
        skill_passed = missions_api.MakeSkillRoll(mission_entity_id)
        event_log.Create("missions/{}/{}".format(MISSION_ID, _result_slot(going_as_planned, skill_passed)))


@event_handler(MissionEvent.GET_MISSION_RESULT_TEXT)
def get_mission_result_text(mission_entity_id):
    # Read the rolls here, never roll again.
    going_as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
    skill_passed = missions_api.GetSkillRoll(mission_entity_id)

    return "missions/{}/{}".format(MISSION_ID, _result_slot(going_as_planned, skill_passed))


def _result_slot(going_as_planned, skill_passed):
    prefix = "ap" if going_as_planned else "gw"
    suffix = "success" if skill_passed else "failure"

    return "{}_{}_transmission".format(prefix, suffix)
