# Mapping a project's rules to the principles

A repository's own rules (invariants, golden rules, integrity standards, lint policies) are
*project rules*: binding in that repo, and usually each an application of one or more `EP-nn`
principles. A mapping lets reviewers cite both ("EP-03, also INV-3") and makes gaps and conflicts
visible. The mapping lives in the project's repo (its docs or its agent instructions), not in this
shared skill, because it describes that project's rules as they stand on the date it was written.

## How to build one

1. **Collect the sources.** Read the repo's `AGENTS.md` (or equivalent) and any standards it points
   to. Note the commit or date you read, so the next reader knows how fresh the mapping is.
2. **Separate rules from facts.** Branch names, paths, ports, tooling commands and workflow steps
   are repo facts and process; they stay in `AGENTS.md` and need no mapping. Map only the rules that
   express a judgment about code.
3. **Map each rule.** One table row per rule:

   | Project rule | Principles | Fit and gaps |
   | --- | --- | --- |
   | `<ID>` one-line summary | EP-nn, EP-nn | Sound / tension / gap, and the suggested rewording |

   Look in particular for:
   - **Absolutes that a principle treats as judgment.** A rule that, read literally, forces a bad
     result in ordinary cases (for example naming every literal) should be restated as the
     principle with its value, not patched with an exception list (D-001, D-004).
   - **Proxies without their reason.** Size caps, counts and thresholds are signals; say what they
     protect so agents don't satisfy them mechanically.
   - **Hand-off rules.** Deferral and out-of-scope rules should accept the structured `@todo(EP-nn)`
     marker listed in the PR (D-003).
   - **Mechanical-enforcement claims.** Machines enforce detectable signals; judgment principles stay
     with review, and every check names the principle it serves.
4. **List uncovered principles.** Principles with no project counterpart can still be cited by
   ID; the owner may want project rules or checks for some.
5. **Align agent instructions.** Where reviewer or engineer instructions in that project list
   specific rules, suggest pointing them at the principles and the review/fix protocols instead.
6. **Propose, don't edit silently.** Suggested rewordings of project rules go to the project's
   owner as a PR or decision in that repo.

## Router line for a project's `AGENTS.md`

Rather than restating principles, the root `AGENTS.md` can carry one line, for example under its
code-quality section:

> The rules below are project rules applying the shared `engineering-principles` skill
> (EP-01 to EP-12). Load that skill when writing, reviewing or fixing code; cite `EP-nn` and the
> rule ID in reviews.
