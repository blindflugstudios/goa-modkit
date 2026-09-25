# An event script in a proper mod tree: handlers, no .json, no mission id.
#
# Missions/ is a mod's only script folder - there is no Events/ folder for mods - so this
# is where event scripts have to live. Reporting it as a mission missing its data would
# tell the author to delete a file that works.

from Blindflug.MinorEvents import MinorEvent


@event_handler(MinorEvent.AIRPLANE_ON_MISSION_SUCCEED)
def on_success(airplane_id, entity_id, mission_id, skill, as_planned, location, estimate):
    return False
