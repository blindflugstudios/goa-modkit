# Coastal Patrol - a minimal hybrid mission.
#
# The JSON file next to this script supplies stats, location, outcomes and timings.
# This script supplies the text: what the crew radios in during the flight, and what
# the result window says afterwards.
#
# File name, get_mission_id return value and the JSON file name must all match exactly.

from Blindflug.FlightMission import MissionEvent

MISSION_ID = "coastal_patrol"


# All nine loc keys this mission needs. Defining them here means no localisation pass
# is required - SetTerm writes into a separate language source at runtime.
def _term(slot, text):
    localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


_term("mission_name", "Coastal Patrol")
_term("mission_description",
      "Fly the shoreline between Dover and Eastbourne. Report anything that moves.")
_term("intel_threat_report", "Low. No enemy activity reported in the last week.")

_term("ap_transmission",
      "Patrol is airborne. Clear skies, good visibility along the coast.")
_term("gw_transmission",
      "Cloud came in thicker than forecast. The flight is feeling its way along the shore.")

_term("ap_success_transmission",
      "Patrol complete. Nothing to report, and the crew enjoyed the view.")
_term("ap_failure_transmission",
      "The patrol flew its route but came back with nothing usable. Wasted fuel.")
_term("gw_success_transmission",
      "Despite the weather the flight held its course and brought back a full report.")
_term("gw_failure_transmission",
      "The flight lost the coastline in the murk and turned back early.")


@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
    return MISSION_ID


@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
    # Fires three times per flight in JSON mode. The first call rolls whether the
    # mission goes as planned; later calls read that roll rather than re-rolling it.
    events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)

    if events_sent == 1:
        going_as_planned = missions_api.MakeAsPlannedRoll(mission_entity_id)
        slot = "ap_transmission" if going_as_planned else "gw_transmission"
        event_log.Create("missions/{}/{}".format(MISSION_ID, slot))

    elif events_sent == 2:
        going_as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
        skill_passed = missions_api.MakeSkillRoll(mission_entity_id)
        event_log.Create("missions/{}/{}".format(MISSION_ID,
                                                 _result_slot(going_as_planned, skill_passed)))


@event_handler(MissionEvent.GET_MISSION_RESULT_TEXT)
def get_mission_result_text(mission_entity_id):
    # Read the rolls, never re-roll here - this runs when the result window opens.
    going_as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
    skill_passed = missions_api.GetSkillRoll(mission_entity_id)

    return "missions/{}/{}".format(MISSION_ID, _result_slot(going_as_planned, skill_passed))


def _result_slot(going_as_planned, skill_passed):
    prefix = "ap" if going_as_planned else "gw"
    suffix = "success" if skill_passed else "failure"

    return "{}_{}_transmission".format(prefix, suffix)

def broken(:
    pass
