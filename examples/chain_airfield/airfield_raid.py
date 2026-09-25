# The Airfield Chain, part 1 of 4 - the enemy comes to you.
#
# Four missions, each unlocked by the one before it succeeding:
#
#   airfield_raid     bombers hit this airfield          you are defending
#   airfield_pursuit  chase them back across the Channel you are reacting
#   airfield_search   find where they came from          you are hunting
#   airfield_strike   destroy it                         you are attacking
#
# The chaining itself is pure JSON - "_requirementType": 3 with a value of
# "<mission_id>,success". No script is needed for it, and none of these four
# scripts touches the chain. What the scripts do is carry the story: each one
# knows where it sits in the sequence and says so.
#
# Every mission in the chain keeps its text in its own script rather than in the
# JSON's _raw* fields, because the four of them share a voice - the same
# squadron, over four days - and keeping the lines together makes that easier to
# write and to read.

from Blindflug.FlightMission import MissionEvent

MISSION_ID = "airfield_raid"


def _define(slot, text):
	localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


def _term(slot):
	return "missions/{}/{}".format(MISSION_ID, slot)


_define("mission_name", "They Came at Dawn")
_define(
	"mission_description",
	"Bombers over the field, and no warning worth the name. Everything that can fly gets "
	"airborne now - anything still on the ground when they arrive is a target. This is not "
	"a patrol you chose. It is one that chose you."
)
_define(
	"intel_threat_report",
	"Nine or more aircraft, low and fast, already inside the coast. Their escort is above "
	"them and they will be over the field in minutes."
)

_define(
	"ap_transmission",
	"Wheels up with seconds to spare. Climbing hard - they are right on top of us."
)
_define(
	"gw_transmission",
	"Caught on the ground. Two never got airborne and the first bombs are already falling."
)
_define(
	"ap_success_transmission",
	"They turned for home early and left two of their own in the fields south of the "
	"perimeter. The airfield is intact. Get the fires out and count the holes."
)
_define(
	"ap_failure_transmission",
	"We were up in time and it made no difference. They dropped where they meant to and "
	"went home unhurried. There is a great deal to repair."
)
_define(
	"gw_success_transmission",
	"A shambles of a scramble and we still broke up the second wave. Half of what they "
	"carried went into the fields instead of the hangars."
)
_define(
	"gw_failure_transmission",
	"They caught us flat-footed and made us pay for it. Whoever planned this knew exactly "
	"where we were and when we would be slowest."
)
_define("cancelled", "Stood down. They turned away before they reached us - this time.")


@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
	return MISSION_ID


@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
	events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)

	if events_sent == 1:
		as_planned = missions_api.MakeAsPlannedRoll(mission_entity_id)
		event_log.Create(_term("ap_transmission" if as_planned else "gw_transmission"))

	elif events_sent == 2:
		missions_api.MakeSkillRoll(mission_entity_id)


@event_handler(MissionEvent.SEND_MISSION_RESULT_EVENT)
def send_mission_result_text(mission_entity_id):
	event_log.Create(_result_term(mission_entity_id))


@event_handler(MissionEvent.GET_MISSION_RESULT_TEXT)
def get_mission_result_text(mission_entity_id):
	return _result_term(mission_entity_id)


@event_handler(MissionEvent.SEND_MISSION_CANCELLED_EVENT)
def send_mission_cancelled_text(mission_entity_id):
	event_log.Create(_term("cancelled"))


def _result_term(mission_entity_id):
	as_planned = missions_api.GetAsPlannedRoll(mission_entity_id)
	successful = missions_api.IsMissionSuccessful(mission_entity_id)

	if as_planned:
		return _term("ap_success_transmission" if successful else "ap_failure_transmission")

	return _term("gw_success_transmission" if successful else "gw_failure_transmission")
