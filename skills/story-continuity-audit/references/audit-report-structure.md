# Canon assessment report structure

Use this skeleton when the task does not prescribe another format.

```markdown
# Canon structure assessment

Source commit: <short revision>

## Scope and method
<Assigned files, prose chapters, mirror checks, and count methods.>

## Executive verdict
<One paragraph on prose completeness and one on canon reliability.>

| Area | Verdict |
| --- | --- |
| Prose/chapter completeness | ... |
| Chapter packet agreement | ... |
| Canon internal consistency | ... |
| State tracking | ... |
| Documentation/navigation | ... |
| Mirror fidelity | ... |

## Findings ranked by publication impact

### Blocker 1 — <systemic problem>
<Every confirmed instance, grouped, with citations on both sides.>

### Major 2 — <problem>
...

## Prose agreement ledger

| Chapter | Material plot agreement | Exceptions found |
| --- | --- | --- |
| 1 | Pass/Fail | ... |

## Mirror assessment

| # | Fact queried | Pinned source | Mirror result | Verdict |
| --- | --- | --- | --- | --- |
| 1 | ... | `file:line` | ... | Match/Mismatch/Inconclusive |

## Recommended repair order
1. ...

## Coverage ledger
- `assigned/path.md` — reviewed (finding tag if applicable)

## Coverage totals and residual uncertainty
- Assigned canon files: N/N reviewed.
- Prose chapters: N/N compared.
- Mirror facts: N checked.
- Missing assigned files: N.
- Unknown: ... because ...
```

Validation expectations:

- The ledger contains every assigned path exactly once.
- Every citation resolves to an existing line at the pinned revision.
- The count in prose and mirror tables matches the declared total.
- `Pass` on plot agreement does not hide metadata or state-table exceptions.
