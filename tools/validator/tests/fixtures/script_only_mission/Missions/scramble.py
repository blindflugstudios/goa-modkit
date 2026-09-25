# A script-only mission: get_mission_id plus initialize_mission, no .json.
#
# It authors its own gates and data, so there is nothing for a file to carry. Distinct from
# orphan_py, which registers get_mission_id but never sets the mission up - that one really
# is a mission missing its data.

from Blindflug.FlightMission import MissionEvent

MISSION_ID = "scramble"


@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
    return MISSION_ID


@event_handler(MissionEvent.INITIALIZE_MISSION)
def initialize_mission(mission_entity_id):
    missions_api.AddMissionRequirement(mission_entity_id, "RunwayTier", "1")
    missions_api.SetMissionStat(mission_entity_id, "Fight", 55, 75)
    missions_api.SetOutcome(mission_entity_id, 3, True)


@event_handler(MissionEvent.GET_MISSION_RESULT)
def get_mission_result(mission_entity_id):
    return missions_api.GetSkillRoll(mission_entity_id)
