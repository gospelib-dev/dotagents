# Risk-based regression strategy

## Build the impact map

Start with the user-visible change and map:

- entry points: navigation, menu, shortcut, command palette, deep link, empty state;
- state: in-memory, local storage, database, filesystem, cache, queue, job, event;
- dependent outputs: editor, issue count, artifact, export, audio, notifications;
- inverse operations: cancel, undo/redo, unlock, retry, delete, reset;
- compatibility: existing data, URLs, preferences, seeds, feature toggles;
- cross-cutting surfaces: accessibility, privacy, security, performance, concurrency;
- historical defects in the same behavior or dependency.

## Select and prioritize

1. **Confirmation test:** reproduce the original failure, apply the fix build, and prove the failure no longer occurs.
2. **Targeted tests:** affected customer behaviors and every changed contract/entry point.
3. **Safety tests:** high-impact risks adjacent to the change even when not directly modified.
4. **Historical pack:** every prior defect whose trigger or dependency overlaps.
5. **Broad suite:** run all cheap deterministic checks; broaden manual/E2E coverage when impact is uncertain, architecture changed, or shared state is touched.
6. **Exploratory regression charter:** test around the fix because bug clusters and compensating changes often create nearby failures.

IBM's current regression overview likewise sequences change-impact analysis, case selection, prioritization, execution, reporting, fixing, and retesting. [RG3]

Kung, Gao, Hsia, Toyoshima, and Chen separate specification-based regression selection into targeted customer-feature tests and risk-directed safety tests. [RG1] Rothermel and Harrold show that safe selection can be cost-effective but its benefit varies with program, change, and suite design; do not claim a selected subset is “safe” without the technique’s stated conditions. [RG2]

## Risk rubric

| Impact | Example | Minimum response |
|---|---|---|
| Critical | user content data loss, secret exposure, wrong published artifact | Confirm + full affected workflow + recovery + persistence + concurrency + accessibility + broad automation |
| High | dead primary action, wrong item or media, lock bypass, destructive duplication | Confirm + targeted + safety + prior-bug pack + exploratory charter |
| Medium | secondary workflow or recoverable state mismatch | Targeted partitions/boundaries + adjacent smoke + keyboard |
| Low | cosmetic defect with no meaning/action loss | Focused check + visual/a11y guard |

Likelihood increases with shared mutable state, asynchronous ordering, persistence migration, prior defects, untested browser wiring, device/media APIs, and broad reusable components. Re-score after findings.

## Stop and release rules

- Stop acceptance on any must-pass failure, data corruption, uncontained privacy/security issue, or inaccessible primary action.
- Continue only to characterize blast radius and gather evidence, not to manufacture a partial pass.
- A selected regression set is complete only when every identified impact/risk has a test or an explicit Blocked/N/A rationale.
- Retrying a flaky check does not pass it; retain first-failure evidence and investigate.

## Sources

- **[RG1]** David C. Kung, Jerry Gao, Pei Hsia, Yasufumi Toyoshima, and Cris Chen, *Specification-based regression test selection with risk analysis*, CASCON 2002, ACM Digital Library. https://dl.acm.org/doi/10.5555/782115.782116
- **[RG2]** Gregg Rothermel and Mary Jean Harrold, *Empirical Studies of a Safe Regression Test Selection Technique*, IEEE Transactions on Software Engineering 24(6), 1998. https://digitalcommons.unl.edu/cgi/viewcontent.cgi?article=1015&context=csearticles
- **[RG3]** IBM, *What is Regression Testing?* (updated 2026), change-impact, selection, prioritization, execution, and retest overview. https://www.ibm.com/think/topics/regression-testing
