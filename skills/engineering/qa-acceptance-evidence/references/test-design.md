# Test design and exploratory practice

## Technique selection

| Question | Technique | Coverage obligation |
|---|---|---|
| Which inputs/contexts should behave alike? | Equivalence partitioning | One representative from every valid and invalid partition; repartition on differing behavior. |
| Where can an ordered rule flip? | Boundary value analysis | Each boundary and closest adjacent value; add both neighbors for high risk. |
| Does history or mode change the outcome? | State-transition testing | Every required valid transition plus critical invalid transitions. |
| Do conditions combine? | Decision table | Every non-collapsible rule, including else/error rules. |
| Is the workflow a user goal? | Scenario testing | End-to-end path, side effects, persistence, recovery. |
| Is the product poorly understood or changing? | Chartered exploration | Reviewable session, notes, bugs, issues, data, follow-up charters. |

ISTQB defines equivalence partitioning, boundary analysis, decision tables, and state transitions as black-box techniques; ISO/IEC/IEEE 29119-4 standardizes test-design techniques. [TD1][TD2]

## Worked model

For an operation with states `draft`, `saving`, `saved`, and `failed`:

1. Enumerate valid transitions: draft→saving, saving→saved, saving→failed, failed→saving.
2. Enumerate critical invalid transitions: saved→saving without a new change; failed→saved without retry.
3. Assert each source state, action, destination, visible status, persisted record, emitted job/event, and duplicate count.
4. Add refresh/cancel during `saving`, double activation, late response ordering, and reload of `saved`/`failed`.
5. Use a decision table if role, lock, or feature toggle changes any transition.

## Behavioral oracle hierarchy

1. Binding acceptance criterion or owner ruling.
2. Current user-facing specification and contract.
3. Existing persisted behavior that compatibility promises preserve.
4. Observable product consistency and domain rules.
5. Heuristics and comparable products, clearly labeled.

Implementation details can explain a failure but cannot substitute for the user-visible oracle. Testing Library and Playwright both recommend user-centric behavior and avoiding internals. [BV1][BV2]

## Exploratory session sheet

- **Charter:** target, risk, and stopping condition.
- **Environment:** build/commit, browser, viewport, seed, toggles, data.
- **Coverage:** functions, data, platform, operations, time, accessibility.
- **Notes:** actions and observations in order.
- **Bugs:** reproducible product threats with evidence.
- **Issues:** questions or test obstacles.
- **Data files:** screenshots, clips, traces, exports, logs.
- **Follow-ups:** new charters, not hidden TODOs in an approval.

Jonathan Bach defines a session as an uninterrupted, reviewable, chartered block and uses a session sheet containing charter, tester, time, task breakdown, data, notes, issues, and bugs. [ET2] Kaner defines exploratory testing as parallel learning, design, execution, and interpretation. [ET1] Bach, Bach, and Bolton add explicit cycles of learning, testing, collaboration, self-management, and evolving work products. [ET3]

## Evidence discipline

- Record the starting state before the action.
- Capture the action and immediate response.
- Read the authoritative target again after navigation/reload.
- Capture error text, focus, console/network/log output, and timing where relevant.
- Preserve the first failure before retrying.
- Distinguish `Pass`, `Fail`, `Blocked`, and `Not applicable` with rationale.

## Sources

- **[TD1]** International Software Testing Qualifications Board, *Certified Tester Foundation Level Syllabus v4.0.1* (2024), §§2.2.3, 4.2.1–4.2.4, 4.4.2, 5.1.5, 5.2. https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf
- **[TD2]** ISO/IEC/IEEE, *29119-4:2021 Software and systems engineering — Software testing — Part 4: Test techniques* (2021). https://www.iso.org/standard/79430.html
- **[ET1]** Cem Kaner, *Defining Exploratory Testing* (2008). https://kaner.com/?p=46
- **[ET2]** Jonathan Bach, *Session-Based Test Management*, Software Testing and Quality Engineering (2000). https://www.satisfice.us/articles/sbtm.pdf
- **[ET3]** James Bach, Jonathan Bach, and Michael Bolton, *Exploratory Testing Dynamics v3.0* (2011). https://www.developsense.com/resource/et-dynamics3.pdf
- **[BV1]** Testing Library maintainers, *Introduction / Guiding Principles* (updated 2026). https://testing-library.com/docs/
- **[BV2]** Microsoft Playwright team, *Best Practices: Test user-visible behavior* (living documentation). https://playwright.dev/docs/best-practices
