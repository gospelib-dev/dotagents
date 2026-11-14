# GospeLib project rules mapped to engineering principles

GospeLib's integrity invariants and Golden Rules are *project rules*: binding in that repo, and
each an application of one or more `EP-nn` principles. This page maps them, so reviewers can cite
both ("EP-03, also INV-3") and so gaps and conflicts are visible. Sources: GospeLib `AGENTS.md`
and `apps/docs/docs/contributing/codebase-integrity-standard.md` (as of 2026-11-14).

## Integrity invariants and Boy-Scout rules

| Project rule | Principles | Fit and gaps |
| --- | --- | --- |
| **INV-1** No arbitrary literals ("named-or-nothing") | EP-01, EP-04 | Sound intent. Stated as an absolute, so read literally it forces names for `0`, `1`, empty strings and test data. Per D-004, restate it as the EP-01 judgment (name a value when the name carries knowledge; leave it inline when the literal is clearer), with lint as a prompt, not a verdict. No exception list. |
| **INV-2** Reuse over duplication; Reuse Decision Procedure | EP-01, EP-02, EP-10 | Strong; Q3 ("a wizard *is* a tabbed interface") is EP-02. Gaps: (a) no question for coincidental similarity; suggest a Q0, "do these encode the same knowledge: if one changes, must the other?"; (b) no exit when the shared thing has decayed into flags (inline and re-extract); (c) "generalise with a prop" can drive boolean-prop growth; point to composition. |
| **INV-3** Import through barrels; one-way dependencies; no cycles | EP-03 | Sound and mechanisable. Gap: barrels govern *where* you import from, not *how much* is exported; suggest "a barrel exports the minimal public API". |
| **INV-4** File-size and god-component caps | EP-03, EP-04, EP-06 | Caps are proxies. Gap: without framing, agents split files mechanically into shallow fragments. Suggest "exceeding a cap signals lost cohesion; decompose along concept boundaries". |
| **§3.1** Duplicate-value and workaround token detectors | EP-01, EP-02 | Good: "semantic distinctness, not value equality" is EP-01's coincidence test. |
| **§3.2** Closed, semantic variant API; layout is the caller's | EP-02, EP-03, EP-07 | Good. Could name composition as the route when callers need different structure. |
| **§3.3** No dead or drifting CSS variables | EP-01, EP-07 | Fine as a specific case. |
| **§0/§4** Mechanical enforcement; teaching errors; warn, clean, error | EP-12 | Tension with D-001: §0 says "every principle here must ultimately be a machine check". Reconciled reading: machines enforce detectable *signals*; judgment principles (EP-02, EP-09) stay with review; every check names its principle. Suggest rewording §0 to say so. |
| **BS-1** Scope-match the fix or defer with `@todo:` | EP-11 | Aligned with D-003 (structured `@todo` + PR list). Reword to the D-003 marker format. |
| **BS-2** Risky: comment, don't touch | EP-09, EP-11 | Sound core (don't trade a regression for a cosmetic win). Its `@todo:` part follows D-003. |
| **BS-3** Side-quest fixes in separate commits | EP-11 | Sound. |
| **BS-4** Only Boy-Scout actual violations | EP-11, EP-04 | Sound, but scoped to "named invariants in this standard" (four INVs). Suggest widening to "a principle in the shared engineering principles or a project rule", so testability or root-cause violations found in passing qualify. |

## Golden Rules

Most Golden Rules are repo facts and process, not principles; they stay in `AGENTS.md`. The ones
that apply a principle:

| Golden Rule | Principles | Notes |
| --- | --- | --- |
| **5** Graph writes are UPSERT in FK order, never TRUNCATE | EP-09, EP-06 (irreversible decisions) | A safety rule; correctly absolute, with its reason given. |
| **7** Gateway is the sole ingress; backends never parse JWTs | EP-03 | A boundary rule. |
| **8** Never bypass git hooks | EP-12 | Protects the machine checks. |
| **9** Use the plan that already exists | EP-01 (applied to plans and tooling), EP-12 | Fine. |
| **10** Done means complete and verified; safety outranks all | EP-08, EP-09, meta "safety outranks tidiness" | Source of the fleet's safety-first ordering. |
| **11** Not complete until merged to `stage` | (process) | Workflow rule, not a principle. |
| **12** No deferral or descoping without explicit owner sign-off | EP-10 reporting, fix protocol section 11 | Reword so a structured D-003 marker listed in the PR counts as an accepted hand-off. Rules 10 to 12 restate one idea three ways; consider consolidating. |
| **1-4, 6, 13-15** | (repo facts and process) | Branches, paths, ports, patterns, legal stance, polling, Markdown reading. Not principles; no mapping needed. |

## Principles with no GospeLib rule

These principles have no counterpart in GospeLib's written rules today. Reviewers can still cite
the `EP-nn` ID; the owner may want project rules or checks for some of them.

- **EP-04** readable in place (names and locality; only INV-1 touches naming)
- **EP-05** document the contract and the why
- **EP-06** least complexity / no speculative generality
- **EP-07** make wrong states hard to represent (TypeScript strictness and Pydantic `extra="forbid"` are partial)
- **EP-08** direct testability
- **EP-09** understand before changing (root cause, Chesterton's fence)
- **EP-10** findings are classes (in the integrity standard's thesis and the reviewer SOUL, but not as an agent rule)

## SOUL wording to align

- Reviewer SOULs, step 3, list specific rules ("no magic literals, barrel imports, file-size caps").
  Suggest "violations of the engineering principles (cite `EP-nn`) and project rules (cite the
  ID)", and point to the review protocol.
- Reviewer SOULs, step 4 ("Every finding is a class: name it, and list every other instance you
  found") already matches EP-10; point to the protocol for format and search.
- Engineer SOULs say "smallest correct change". Suggest "smallest sufficient change (EP-11): no
  one-off hacks, no fix-one-ignore-the-rest, no rewrite for a minor bug", and point step 5 to the
  fix protocol.

## Router line for GospeLib `AGENTS.md`

Rather than restating principles, the root `AGENTS.md` can carry one line, for example under
Codebase Integrity:

> The invariants below are project rules applying the shared `engineering-principles` skill
> (EP-01 to EP-12). Load that skill when writing, reviewing or fixing code; cite `EP-nn` and the
> invariant ID in reviews.
