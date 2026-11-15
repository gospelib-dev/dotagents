---
name: smart-home-request-handling
description: Use when relaying or doing a request to read or change smart-home devices.
metadata:
  version: "0.1.0"
  status: draft
  owner: maintainer
---

# Smart-home request handling

## Purpose
Handle "is the door locked?", "turn the office lights on", "make the house warmer" safely when one
agent holds the home-automation tools and other agents (or the person) ask through it. The method
separates direct asks from proposals, gates security devices behind explicit naming, never reports
an action done until the new state is read back, and keeps answers complete even when the asker
only sees the first line.

## When to use
- **Requester role:** an assistant without device tools receives a house question or action from
  its person and must route it to the agent that has the tools.
- **Executor role:** the agent with home-automation tools receives a request (usually a task from
  another agent).

## Method

### 1. Classify the request
- **Direct ask** from the person (lights, switches, plugs, thermostat, fans, covers, media players,
  scenes, scripts): carry it out.
- **Security devices** (locks, alarm, garage doors): act only when the person named that device;
  quote their exact words in the request. Never infer from a vague ask ("lock up", "secure the
  house"): read the states, then ask which to change.
- **Anything nobody asked for, and any change to the automation platform itself** (automations,
  integrations, dashboards, settings, restarts, updates): proposal only, prefixed `Proposal:`. The
  person decides; the executor acts only after a later request carrying their yes in their words.

### 2. Requester: write the request
- Title: `House: <short question or action>`. One request per ask; independent asks in parallel.
- Body, in order: (1) who asked (`Requested by <person>: yes`) or `Proposal only: do not act`;
  (2) the ask in plain words with the device as the person named it (room + device) and values
  (temperature, brightness, until when); (3) for security devices, the person's exact words in
  quotes; (4) what to report back (state after the action, or the reading).
- Never put private details (health worries, gifts) in the body; health-device questions name only
  the metric wanted, and only the agent authorized for that person asks them.
- Never guess a device state and never tell the person something is done before the executor
  reports it. Send a holding line and wait to be woken.

### 3. Executor: find, act, read back
1. Find the entity first (by domain and/or area) and match the room + device named. If two entities
   could fit, act on neither; report both names and ask which.
2. Find the right service and its fields, then call it.
3. **Read the state back after every action.** Report done only if the new state shows it; if not,
   say so with the likely cause (device offline/unavailable, wrong entity, service rejected).
4. A device that isn't in the platform cannot be reached: say "not in <platform>" rather than
   guessing; the requester should not retry with other names more than once.
5. Health data from devices goes only to the authorized requester, only the metrics asked.

### 4. Executor: reply format
- **The first line is the complete short answer**, because the asker may be woken with only that
  line: `15 lights on: Kitchen, Kitchen Island, Dining Room, Entry, ... (full list below)` or
  `Office lights turned on -> on, 40%`.
- Count only real fixtures: leave out indicator LEDs (network gear, keypad/button LEDs) and
  segments of a light already listed; list a lamp once if it appears as both a light and a switch.
- One line per device: `<friendly name> (<entity id>): <what you did> -> <state read back>`.
- Questions: answer first, then each reading with its last-updated time.
- Errors: exact error text and whether anything changed. Proposals on their own lines with the
  reason in one clause. No preamble, no tips.

### 5. Requester: relay
- Open the full result before answering; never answer from the wake message's first line alone
  (a list answered from its first line can be badly wrong).
- Lists: count and rooms ("15 lights are on: kitchen, kitchen island, ..."); skip entity IDs and
  brightness unless asked. Actions: one short line ("Office lights are on, 40%."). Failures: say so
  plainly with cause and next step. Proposals: one line plus a yes/no question.

## Pitfalls
- Acting on a security device from a vague request.
- Reporting an action as done without a state read-back.
- Acting on an ambiguous entity match.
- Answering from a truncated first line; counting indicator LEDs as lights.
- The executor making unrequested changes instead of proposals.

## Verification
- Every action in the reply shows a state read back after the call.
- Security-device actions trace to the person's quoted words.
- The first line alone answers the question correctly.

## Household specifics
The agent's own local skill supplies the automation platform and tool names, which agent holds
device access, device and room names, which devices count as security devices, which health
devices exist and who may ask about them, what the executor's tools cannot do, and board
conventions for requests.
