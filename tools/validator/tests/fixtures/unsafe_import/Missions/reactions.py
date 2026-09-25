# An event script that reaches the file system. The game has no sandbox, so the validator
# must warn - but still let it load, because it is valid Python.

import clr
from Blindflug.MinorEvents import MinorEvent


@event_handler(MinorEvent.AIRPLANE_ON_MISSION_SUCCEED)
def on_success(airplane_id, entity_id, mission_id, skill, as_planned, location, estimate):
    clr.AddReference("System")
    return False
