# Reacting to the world, not to a mission you own.
#
# Minor events fire from base life and from every mission, including missions written by
# somebody else. A script like this needs no JSON and no mission of its own - drop it in
# a mod's Missions/ folder and it runs - that is a mod's only script folder, and the loader
# imports every module it finds, so a file with handlers but no JSON works fine there.

from Blindflug.MinorEvents import MinorEvent
from Blindflug.Game.Characters.Morale import MoraleCategory


localization.SetTerm(
    "en", "convoy_reactions/dover_relief",
    "Word comes back from the coast: the patrol over [location] returned without loss. "
    "The ground crews breathe easier.")

localization.SetTerm(
    "en", "convoy_reactions/hard_night",
    "[character:{[PILOT]}] sat up late after the failed sortie, going over the maps again.")

localization.SetTerm(
    "en", "convoy_reactions/quiet_midnight",
    "A still night over the airfield. Nothing but the sound of the sea.")


# Seven arguments arrive with this event, so a script can be very specific about which
# mission it reacts to - without owning that mission.
@event_handler(MinorEvent.AIRPLANE_ON_MISSION_SUCCEED)
def on_mission_success(airplane_id, entity_id, mission_id, skill_type,
                       going_as_planned, location_name, success_estimate):
    if location_name != "dover":
        return False   # not counted against max_occurrences

    event_log.Create("convoy_reactions/dover_relief")


@event_handler(MinorEvent.AIRPLANE_ON_MISSION_FAILED, chance=0.5, max_occurrences=3)
def on_mission_failure(airplane_id, entity_id, mission_id, skill_type,
                       going_as_planned, location_name, success_estimate):
    # A failure that was predicted to go well stings more.
    if success_estimate < 60:
        return False

    pilot = airplanes_api.GetPilot(entity_id)

    if pilot is None:
        return False

    characters_api.ModifyMorale(pilot, MoraleCategory.Confidence, -5)
    event_log.Create("convoy_reactions/hard_night", {"PILOT": str(pilot)})


@event_handler(MinorEvent.MIDNIGHT, chance=0.02, max_occurrences=2)
def quiet_night(year, month, day):
    event_log.Create("convoy_reactions/quiet_midnight")
