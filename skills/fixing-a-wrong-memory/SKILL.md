---
name: fixing-a-wrong-memory
description: Use when you are corrected or find a stored memory is wrong. Remove or supersede every copy.
metadata:
  version: "0.2.0"
  status: draft
  owner: maintainer
---

# Fixing a wrong memory

A wrong fact in long-term memory keeps coming back: every later recall surfaces it again, and an
added "correction" that does not say what it replaces just sits next to it, so the agent now holds two
contradicting facts and may pick either. The fix is to remove every stored copy of the wrong fact and store
the right one once, or, where your memory tools cannot remove anything, to store a correction that
explicitly supersedes the old fact so the store can tell which one is current.

## When to use
- Someone corrects you ("that's not right", "I changed that", "we stopped doing X").
- You notice that something you recalled conflicts with live data or with what the person just said.
- A recall returns two versions of the same fact.

## Procedure
1. **Find every stored version.** Search the memory store for the fact, using two or three different
   wordings (names, synonyms, the old value, the new value). Copies are often phrased differently.
2. **Remove each wrong version**, if your tools can: delete or invalidate it by its id. Leave unrelated facts
   alone, even if they share words.
3. **Save the correct fact once**, in one clear sentence that stands on its own (who, what, since when). If you
   could not remove the old version, make the sentence say what it replaces and from when
   ("Since <date>, X is Y; this replaces the earlier X is Z"), so recall and consolidation favour it.
4. **Confirm** by searching once more: only the corrected fact should come back, or the corrected fact should
   come back first and clearly marked as current. If the wrong version still wins, report it (see Rules).
5. **Repeat in every other store you keep** (notes files, local memory files, profile docs): the same wrong
   fact usually lives in more than one place.

## Rules
- Never add a bare correction on top of a wrong memory: delete the wrong one, or say exactly what the new
  fact replaces.
- Never claim a wrong fact is gone when it is not. If a delete fails, or your tools cannot remove memories
  and the wrong version still comes back, say exactly which fact, its id if you saw one, and what the tool
  returned, so whoever administers the store can remove it.
- Correct only what was wrong. Don't take the chance to rewrite or prune other memories.
- Private facts stay where they were stored; fixing a memory never moves it to a more shared place.

## Tool examples
- Hermes with Honcho: `honcho_conclude` with `list=true` and a `query` finds stored conclusions and
  their ids; `honcho_conclude` with `delete_id` removes one; `honcho_conclude` with `conclusion` saves the
  corrected fact.
- Hindsight (Hermes plugin tools `hindsight_recall` / `hindsight_retain`, or MCP `recall` / `retain`): agent
  tools usually cannot delete. Recall with several wordings, retain one dated fact that names what it
  replaces, recall again to confirm. Removing the stale unit (`invalidate_memory` with a reason) is an
  administrator operation; report the unit's id if it keeps winning.
- Other memory tools: use their search, delete-or-invalidate-by-id and add operations in the same order; if
  they are append-only, follow the supersede path above.
