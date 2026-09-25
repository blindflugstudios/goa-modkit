# The walrus operator is Python 3.8; the game's IronPython 3.4 cannot parse it and skips
# the whole file. f-strings, on the other hand, are fine.

from Blindflug.MinorEvents import MinorEvent


@event_handler(MinorEvent.AIRPLANE_ON_MISSION_SUCCEED)
def on_success(airplane_id, entity_id, mission_id, skill, as_planned, location, estimate):
    if (name := f"{mission_id}"):
        return False
    return False
