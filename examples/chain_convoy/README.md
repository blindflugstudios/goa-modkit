# Example: Convoy Chain

Three missions that branch on the outcome of the first. Chains need no script: a requirement of type 3 (`CompletedMission`) in the JSON does it.

## The structure

```text
convoy_spotted            available from day 10, runway tier 2
   |
   +-- success --> convoy_strike     "convoy_spotted,success"
   |
   +-- failure --> convoy_search     "convoy_spotted,failure"
```

The gate lives in each follow-up mission's JSON:

```json
{ "Name": "CompletedMission", "_requirementType": 3, "_value": "convoy_spotted,success" }
```

The value is `"<missionId>"` on its own, or `"<missionId>,<outcome>"` where outcome is `success`, `failure` or `cancelled`. Without an outcome, any finish counts.

## Why the follow-ups are historic

Both `convoy_strike` and `convoy_search` set `"_isHistoric": true`. This matters for chains: a historic mission never enters the random weekly draw and is **guaranteed** to appear once its gate passes. With a `_historicDay` it appears on that date; without one (as here) it takes the next mission slot, so it arrives with a normal mission's lead time. It never expires. Without the flag the follow-up would sit in the random pool and might not appear for weeks, or at all.

A historic mission is also one-shot on success: once won it never appears again, so the branch cannot repeat. A failed or cancelled attempt comes back at the next slot.

## Files

| File | Role |
|---|---|
| `convoy_spotted.json` / `.py` | step 1, plain gates |
| `convoy_strike.json` / `.py` | step 2a, requires success |
| `convoy_search.json` / `.py` | step 2b, requires failure |

## Watch out

- **Ids must be unique.** A second mission with the same id replaces this one. When you prefix the ids with your mod name, update the `_value` of both requirements as well.
- A mission the player called off counts as `cancelled`, not as a failure.

## Tested

Loaded and created in the game. All three missions registered, and the game read both chain requirements exactly as written. The `create_mission` cheat used for this skips requirements, so the branch itself (`convoy_strike` appearing only after a successful `convoy_spotted`) has not yet been flown end to end.
