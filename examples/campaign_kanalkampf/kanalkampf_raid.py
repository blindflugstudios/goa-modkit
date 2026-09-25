# Kanalkampf, part 1 - the raid that keeps coming back.
#
# The same mission, flown repeatedly, that is not the same mission twice. What
# changes is what the campaign remembers:
#
#   * the briefing counts how many raids you have already survived
#   * the third raid onwards, the enemy has learned - the target gets harder
#   * losing three raids opens the fallback mission instead of the counterattack
#   * whoever is aboard the first time you win is remembered by name, and the
#     later missions refer to them
#
# None of that fits in a JSON file. The four fixed outcomes are still there, and
# still declared in the JSON; what the script adds is everything that depends on
# what came before.

from Blindflug.FlightMission import MissionEvent

import campaign_state

MISSION_ID = "kanalkampf_raid"

# From this many raids on, the enemy stops making mistakes.
ENEMY_ADAPTS_AFTER = 2

# Losing this many opens the regroup mission rather than the counterattack.
DEFEATS_BEFORE_REGROUP = 3


def _define(slot, text):
	localization.SetTerm("en", "missions/{}/{}".format(MISSION_ID, slot), text)


def _term(slot):
	return "missions/{}/{}".format(MISSION_ID, slot)


_define("mission_name", "Kanalkampf")
_define(
	"mission_description",
	"They come across the Strait every morning now, and they come for the airfield. There "
	"is nothing clever to be done about it: get everything airborne before they arrive, or "
	"lose it on the ground."
)
_define(
	"intel_threat_report",
	"The usual formation, the usual hour. Whether they have learned anything from last "
	"time is the only open question."
)

_define("first_raid", "First one. Nobody here has done this before - climbing and hoping.")
_define("another_raid", "Another morning, another plot on the table. We know the drill by now.")
_define(
	"they_learned",
	"They have changed their approach - higher, and with the sun behind them. Somebody over "
	"there has been paying attention to us."
)

_define("ap_transmission", "Airborne in time and above them. This is the position we want.")
_define("gw_transmission", "Late off the ground and they are already on the run-in.")

_define(
	"ap_success_transmission",
	"Broke them up before the field and sent them home light. That is one they will "
	"remember."
)
_define(
	"ap_failure_transmission",
	"Good position, poor shooting. They bombed and left and we have nothing to show for it."
)
_define(
	"gw_success_transmission",
	"Scrambled late, caught them anyway, and turned the second wave back over the coast."
)
_define(
	"gw_failure_transmission",
	"Too slow, too few, and the field has the craters to prove it."
)

_define("cancelled", "They turned back over the water. A morning off, for once.")


@event_handler(MissionEvent.GET_MISSION_ID)
def get_mission_id(mission_entity_id):
	return MISSION_ID


@event_handler(MissionEvent.INITIALIZE_MISSION)
def initialize_mission(mission_entity_id):
	"""Raise the bar once the enemy has seen this squadron a few times.

	The JSON declares the mission's baseline; this makes the campaign's third
	raid measurably harder than its first, which no amount of JSON could.
	"""
	state = campaign_state.load()
	raids = state["raids_survived"] + state["raids_lost"]

	if raids < ENEMY_ADAPTS_AFTER:
		return

	# Each raid after the second raises the skill target and lowers the chance of
	# a clean intercept, up to a floor that is still winnable.
	step = min(raids - ENEMY_ADAPTS_AFTER, 3)

	missions_api.SetMissionStat(mission_entity_id, "Fight", 60 + step * 8, 95 + step * 10)
	missions_api.SetAsPlannedChance(mission_entity_id, max(25, 45 - step * 5))


@event_handler(MissionEvent.SEND_MISSION_EVENT)
def send_mission_event(mission_entity_id):
	events_sent = missions_api.GetNumberOfEventsSent(mission_entity_id)

	if events_sent == 1:
		state = campaign_state.load()
		raids = state["raids_survived"] + state["raids_lost"]

		if raids == 0:
			event_log.Create(_term("first_raid"))
		elif raids >= ENEMY_ADAPTS_AFTER:
			event_log.Create(_term("they_learned"))
		else:
			event_log.Create(_term("another_raid"))

		as_planned = missions_api.MakeAsPlannedRoll(mission_entity_id)
		event_log.Create(_term("ap_transmission" if as_planned else "gw_transmission"))

	elif events_sent == 2:
		missions_api.MakeSkillRoll(mission_entity_id)


@event_handler(MissionEvent.SET_MISSION_IMPACT)
def set_mission_impact(mission_entity_id):
	"""Record what happened, then decide what the campaign offers next.

	This is the whole reason the campaign is in Python: the follow-up depends on
	the record, not on this one flight.
	"""
	successful = missions_api.IsMissionSuccessful(mission_entity_id)
	state = campaign_state.load()

	if successful:
		state["raids_survived"] = state["raids_survived"] + 1

		# Remember who was aboard the first time this squadron won one.
		if state["first_blood"] is None:
			formation = missions_api.GetMissionAirplaneFormation(mission_entity_id)

			if len(formation) > 0:
				state["first_blood"] = airplanes_api.GetPilot(formation[0])
	else:
		state["raids_lost"] = state["raids_lost"] + 1

	campaign_state.save(state)

	# A squadron that keeps losing needs to regroup before it can counterattack.
	if state["raids_lost"] >= DEFEATS_BEFORE_REGROUP:
		missions_api.CreateMission("kanalkampf_regroup")
	elif successful:
		missions_api.CreateMission("kanalkampf_pursuit")


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
