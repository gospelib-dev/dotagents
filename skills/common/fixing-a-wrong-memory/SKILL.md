---
name: fixing-a-wrong-memory
description: Use when you are corrected or find a stored memory is wrong. Delete every copy, save once.
metadata:
  version: "0.1.0"
  status: draft
  owner: Lance
---

# Fixing a wrong memory

A wrong fact in long-term memory keeps coming back: every later recall surfaces it again, and an
added "correction" just sits next to it, so the agent now holds two contradicting facts and may pick
either. The fix is to remove every stored copy of the wrong fact and then store the right one once.

## When to use
- Someone corrects you ("that's not right", "I changed that", "we stopped doing X").
- You notice that something you recalled conflicts with live data or with what the person just said.
- A recall returns two versions of the same fact.

## Procedure
1. **Find every stored version.** Search the memory store for the fact, using two or three different
   wordings (names, synonyms, the old value, the new value). Copies are often phrased differently.
2. **Delete each wrong version** by its id. Leave unrelated facts alone, even if they share words.
3. **Save the correct fact once**, in one clear sentence that stands on its own (who, what, since when).
4. **Confirm** by searching once more: only the corrected fact should come back.
5. **Repeat in every other store you keep** (notes files, local memory files, profile docs): the same wrong
   fact usually lives in more than one place.

## Rules
- Never add a correction on top of a wrong memory without deleting the wrong one.
- Never claim you could not remove it. If a delete really fails, say exactly which tool or call failed
  and what it returned, so a human can fix it.
- Correct only what was wrong. Don't take the chance to rewrite or prune other memories.
- Private facts stay where they were stored; fixing a memory never moves it to a more shared place.

## Tool examples
- Hermes with Honcho: `honcho_conclude` with `list=true` and a `query` finds stored conclusions and
  their ids; `honcho_conclude` with `delete_id` removes one; `honcho_conclude` with `conclusion` saves the
  corrected fact.
- Other memory tools: use their search, delete-by-id and add operations in the same order.
