---
name: event-script
description: Write a Python event script that reacts to things happening in Ground of Aces (midnight, building finished, mission returned, plane landing). Use when the user says "when X happens, do Y", "react to", "random event", "event log message", "morale change after", "script that listens".
---

# Event script

Read `AGENTS.md` sections 8 and 11. Sources: `docs/en/scripting/events.md` (events and argument order), `docs/en/scripting/api.md` (what a script can do), `minor_events` in `generated/catalog.json`.

## 1. Understand the idea

Ask one at a time:

1. **Mod id**.
2. **Trigger** - which event. Pick from `minor_events` where `tutorial_only` is false. If nothing fits, say so.
3. **Reaction** - an event log message, a morale change, a mission handed out, ... Only use functions documented in `docs/en/scripting/api.md`.
4. **How often** - `chance` (0.0-1.0) and `max_occurrences` per save game. Default something modest so it does not become wallpaper.

## 2. Scaffold

New mod: copy `templates/event-script/` to `mods/<mod_id>/`. Existing mod: add a new `.py` to its `Missions/`. The file **must** be in `Missions/`; it is the only script folder. Also see `examples/event_script/`.

## 3. Write

- `from Blindflug.MinorEvents import MinorEvent`; decorate with `@event_handler(MinorEvent.NAME, chance=..., max_occurrences=...)`.
- Copy the argument list from the docs; arguments are positional.
- Return `False` early when the event is not the one you care about; it does not use up `max_occurrences`.
- Texts: `localization.SetTerm("en", "<mod_id>/<name>", text)` at top level; placeholders `{[NAME]}` filled by `event_log.Create(key, {"NAME": str(value)})`. Formatting tags: `docs/en/scripting/localization.md`.
- Handing out a mission: `missions_api.CreateMission("<mission_id>")`.
- No forbidden imports; nothing newer than Python 3.6; top-level code small and safe.

## 4. Validate

`python tools/validator/goa_validate.py mods/<mod_id>` until 0 errors (it warns about tutorial-only events), plus `AGENTS.md` section 13.

## 5. Install and hand over

Follow `install-mod`. Tell the user: save, Options -> Quit to main menu, open Mods (if the mod folder is new, press **Refresh** - opening the window alone does not rescan; check the mod is listed and on), load the save again. Explain how to trigger the event (and that `chance` may make it rare - suggest temporarily `chance=1.0` for testing, then set it back). Ask what they see; on trouble `read-log`.
