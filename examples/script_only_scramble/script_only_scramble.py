# A mission with no JSON at all.
#
# Everything a .json would declare - gates, stats, location, slots, difficulty, outcomes and
# their effects - is written from here during initialize_mission. The eight getters below
# supply the base values the game reads just before that.
#
# Why bother, when JSON is simpler? Because these values can be computed. What the player has
# already flown cannot be expressed in a file. This example keeps the arithmetic obvious
# rather than clever: the enemy count and the skill target both grow with the number of
# scrambles already flown, counted in the mission's own data folder.
#
# The two things this file must get right, and which cost the most time to discover:
#
#   1. It has to gate itself. A script-authored mission starts with no requirements and no
#      map tags. Once it has been created the first time the game *does* know its data, so
#      the weekly draw stops skipping it - and with no gates it passes every check.
#      Without AddMissionRequirement this mission would start turning up in the weekly draw
#      on any map and any date.
#
#   2. It has to define get_mission_result. The authored data lives in memory only, so a
#      save loaded with this mission in flight has no authored outcomes; the game then asks
#      this handler for the result and fails with an error if it is missing.

import json
import os

from Blindflug.FlightMission import MissionEvent

MISSION_ID = "script_only_scramble"

# Gates. Without these the mission is drawable everywhere once created - see note 1 above.
REQUIRED_RUNWAY_TIER = "2"
EARLIEST_DAY = "10"

# The mission grows with use. Kept linear and clamped so the numbers stay readable in the
# mission window.
BASE_ENEMY_COUNT = 3
MAX_ENEMY_COUNT = 9
BASE_SKILL_TARGET = 55
MAX_SKILL_TARGET = 85


def _term(slot, text):
    localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


_term("mission_name", "Scramble")
_term("mission_description",
      "Radar has something crossing the coast and no patrol close enough to meet it. "
      "Everything that can start, starts now.")
_term("intel_threat_report", "Unknown. Whatever it is, it is already inbound.")
_term("mission_threat_level", "Rising")

_term("ap_transmission", "Flight is up and climbing on the vector. Contact expected shortly.")
_term("gw_transmission", "They came in lower than the plot suggested. The flight is turning hard to catch up.")

_term("ap_success_transmission", "Interception clean. They turned for home short of the coast.")
_term("ap_failure_transmission", "The flight made contact and lost it again in the haze. No claim.")
_term("gw_success_transmission", "Caught them late and low, but caught them. Two turned back trailing smoke.")
_term("gw_failure_transmission", "The flight never got above them. They went through and away.")


def _state_path():
    """A file of our own, per save game.

    GetScriptDataPath is per mission id and NOT per save, so the air base guid goes in the
    file name - otherwise a second campaign in a second save would continue the first one.
    """
    folder = game_api.GetScriptDataPath(MISSION_ID)

    return os.path.join(folder, "scrambles_{}.json".format(game_api.GetAirBaseGuid()))


def _scrambles_flown():
    """How many times this mission has been handed out. Missing or unreadable reads as 0."""
    try:
        with open(_state_path(), "r") as handle:
            return int(json.load(handle).get("flown", 0))
    except Exception:
        return 0


def _record_scramble():
    try:
        with open(_state_path(), "w") as handle:
            json.dump({"flown": _scrambles_flown() + 1}, handle)
    except Exception as error:
        print("{}: could not record scramble count: {}".format(MISSION_ID, error))


def _scaled(base, top, per_scramble=1):
    """Base value grown with how many scrambles have been flown, clamped to top."""
    return min(base + _scrambles_flown() * per_scramble, top)


@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
    return MISSION_ID


@event_handler(MissionEvent.INITIALIZE_MISSION)
def initialize_mission(mission_entity_id):
    # Gates first. Everything else is cosmetic if the mission appears where it should not.
    missions_api.AddMissionRequirement(mission_entity_id, "RunwayTier", REQUIRED_RUNWAY_TIER)
    missions_api.AddMissionRequirement(mission_entity_id, "EarliestAppearanceDay", EARLIEST_DAY)

    # No tags means "default", which every map declares - right for a mission that suits any
    # airfield. A campaign mission would name its own tag here instead.
    missions_api.SetTags(mission_entity_id, "default")

    missions_api.SetMissionLocation(mission_entity_id, "dover")
    missions_api.SetMaxAirplaneSlots(mission_entity_id, 3)
    missions_api.SetDifficulty(mission_entity_id, 2)
    missions_api.SetAsPlannedChance(mission_entity_id, 55)

    # Two stats: the first is rolled when the mission goes to plan, the second when it does
    # not. Both scale, so the mission stays a threat as the squadron improves.
    target = _scaled(BASE_SKILL_TARGET, MAX_SKILL_TARGET)

    missions_api.SetMissionStat(mission_entity_id, "Fight", target, target + 20)
    missions_api.SetMissionStat(mission_entity_id, "Maneuverability", target + 5, target + 25)

    # Four outcomes in the mandatory order: gone wrong + skill failed, gone wrong + passed,
    # as planned + failed, as planned + passed. Only the last two count as a success here.
    missions_api.SetOutcome(mission_entity_id, 0, False)
    missions_api.SetOutcome(mission_entity_id, 1, False)
    missions_api.SetOutcome(mission_entity_id, 2, False)
    missions_api.SetOutcome(mission_entity_id, 3, True)

    missions_api.AddOutcomeEffect(mission_entity_id, 0, "Damage", "80-160")
    missions_api.AddOutcomeEffect(mission_entity_id, 0, "CrewMood", "-25")
    missions_api.AddOutcomeEffect(mission_entity_id, 1, "Damage", "40-90")
    missions_api.AddOutcomeEffect(mission_entity_id, 2, "CrewMood", "-10")
    missions_api.AddOutcomeEffect(mission_entity_id, 3, "CrewConfidence", "20")
    missions_api.AddOutcomeEffect(mission_entity_id, 3, "VictoryPoints", "6")

    # Counted last, so the numbers above describe this flight rather than the next one.
    _record_scramble()


@event_handler(MissionEvent.GET_MISSION_NAME)
def get_mission_name(mission_entity_id):
    return "missions/{}/mission_name".format(MISSION_ID)


@event_handler(MissionEvent.GET_MISSION_DESCRIPTION_TEXT)
def get_mission_description_text(mission_entity_id):
    return "missions/{}/mission_description".format(MISSION_ID)


@event_handler(MissionEvent.GET_THREAT_LEVEL)
def get_threat_level(mission_entity_id):
    return "missions/{}/mission_threat_level".format(MISSION_ID)


@event_handler(MissionEvent.GET_TIME_TO_START)
def get_time_to_start(mission_entity_id):
    # A scramble is the one mission type where a short window is the point.
    return 25


@event_handler(MissionEvent.GET_COMPLETION_TIME)
def get_completion_time(mission_entity_id):
    return 70


@event_handler(MissionEvent.GET_ENEMY_COUNT)
def get_enemy_count(mission_entity_id):
    return _scaled(BASE_ENEMY_COUNT, MAX_ENEMY_COUNT)


@event_handler(MissionEvent.GET_MISSION_EVENTS_COUNT)
def get_mission_events_count(mission_entity_id):
    return 3


@event_handler(MissionEvent.GET_FUEL_LEVEL)
def get_fuel_level(mission_entity_id):
    return 100


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
        event_log.Create("missions/{}/{}".format(MISSION_ID,
                                                 _result_slot(going_as_planned, skill_passed)))


@event_handler(MissionEvent.GET_MISSION_RESULT)
def get_mission_result(mission_entity_id):
    # Required, not optional - see note 2 in the header. Without this a save loaded with the
    # mission in flight throws when it resolves.
    return missions_api.GetAsPlannedRoll(mission_entity_id) and missions_api.GetSkillRoll(mission_entity_id)


@event_handler(MissionEvent.GET_MISSION_RESULT_TEXT)
def get_mission_result_text(mission_entity_id):
    going_as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
    skill_passed = missions_api.GetSkillRoll(mission_entity_id)

    return "missions/{}/{}".format(MISSION_ID, _result_slot(going_as_planned, skill_passed))


def _result_slot(going_as_planned, skill_passed):
    prefix = "ap" if going_as_planned else "gw"
    suffix = "success" if skill_passed else "failure"

    return "{}_{}_transmission".format(prefix, suffix)
