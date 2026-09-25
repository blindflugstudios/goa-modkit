# my_mod_reactions - event script template.
#
# An event script owns no mission. It reacts to things that happen at the base.
# It lives in Missions/ because that is the only folder the game loads scripts from.
# Replace "my_mod" with your own mod id everywhere.

from Blindflug.MinorEvents import MinorEvent

localization.SetTerm("en", "my_mod/quiet_night",
                     "A still night over the airfield. Nothing but the wind in the wires.")
localization.SetTerm("en", "my_mod/aircraft_home",
                     "Mission {[MISSION]} is home. The ground crew wave the aircraft in.")


# 5 % of midnights, at most 3 times per save game.
@event_handler(MinorEvent.MIDNIGHT, chance=0.05, max_occurrences=3)
def on_midnight(year, month, day):
    event_log.Create("my_mod/quiet_night")


# Seven arguments arrive with this event, in this order.
@event_handler(MinorEvent.AIRPLANE_ON_MISSION_SUCCEED, chance=0.25, max_occurrences=5)
def on_mission_success(airplane_id, entity_id, mission_id, skill_type,
                       going_as_planned, location_name, success_estimate):
    if going_as_planned:
        return False   # returning False does not count against max_occurrences

    event_log.Create("my_mod/aircraft_home", {"MISSION": str(mission_id)})
