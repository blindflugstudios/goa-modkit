# Writing a file without GetScriptDataPath - legal, but worth a note: the only reason a mod
# needs file access is its own state folder.

from Blindflug.MinorEvents import MinorEvent


@event_handler(MinorEvent.AIRPLANE_ON_MISSION_SUCCEED)
def on_success(airplane_id, entity_id, mission_id, skill, as_planned, location, estimate):
    with open("notes.txt", "w") as handle:
        handle.write(mission_id)
    return False
