# Shared memory for the Kanalkampf campaign.
#
# This is the piece JSON cannot do at all. A mission's JSON declares four fixed
# outcomes and flat numbers; it cannot remember that the enemy has raided you
# four times, that Sergeant Clark has been shot down twice, or that the player
# chose to hunt the airfield instead of defending the coast. A campaign is made
# of exactly those things.
#
# game_api.GetScriptDataPath(id) hands out a folder of your own under the
# player's save directory. What you write there survives the flight, the day and
# the session. The shipped birthday_mission uses the same trick.
#
# That folder is per id and NOT per save game, so the file name carries the air
# base guid. Without that, starting a second campaign in a second save would
# continue - and overwrite - the first one.
#
# This file is loaded like any other script in the mod - it registers no
# handlers, it just defines functions the four mission scripts import by calling
# them. Keeping the state in one place means the missions cannot disagree about
# what has happened.

import json
import os

CAMPAIGN_ID = "kanalkampf"

# What a fresh campaign looks like. Every key the missions read has to be here,
# or a save made before that key existed will KeyError on load.
_DEFAULTS = {
	"raids_survived": 0,
	"raids_lost": 0,
	"pursuits_flown": 0,
	"airfield_found": False,
	"airfield_struck": False,
	"pilots_lost": 0,
	"first_blood": None,
}


def _path():
	"""One state file per save game.

	GetScriptDataPath is per id, not per save: two campaigns in two different
	saves would otherwise share - and overwrite - each other's progress. The air
	base guid identifies the save, so it goes in the file name.
	"""
	return os.path.join(
		game_api.GetScriptDataPath(CAMPAIGN_ID),
		"campaign_{}.json".format(game_api.GetAirBaseGuid())
	)


def load():
	"""The campaign so far. Missing keys fall back to their default, so an old
	save picks up new keys instead of crashing on them."""
	state = dict(_DEFAULTS)

	try:
		with open(_path(), "r") as handle:
			stored = json.load(handle)
	except (IOError, OSError, ValueError):
		# No file yet, or a half-written one. Either way: start clean rather than
		# take the whole mission down with an exception in a handler.
		return state

	if isinstance(stored, dict):
		state.update(stored)

	return state


def save(state):
	try:
		with open(_path(), "w") as handle:
			json.dump(state, handle)
	except (IOError, OSError):
		# A campaign that cannot write its state still has to fly.
		logger.LogWarning(CAMPAIGN_ID, "could not write campaign state")


def get(key):
	return load().get(key, _DEFAULTS.get(key))


def bump(key, amount=1):
	"""Increment a counter and return its new value."""
	state = load()
	state[key] = state.get(key, 0) + amount
	save(state)

	return state[key]


def set_value(key, value):
	state = load()
	state[key] = value
	save(state)


def reset():
	"""Start the campaign over. Worth exposing: without it a player who finishes
	the arc can never see it again on the same save."""
	save(dict(_DEFAULTS))
