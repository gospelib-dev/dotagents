---
name: test-lanes-and-coverage
description: Use when judging a test suite: lanes, branch-coverage ratchet, perf budgets.
metadata:
  version: "0.1.0"
  status: draft
  owner: maintainer
---

# Test lanes, coverage and performance evidence

How an engineer or code reviewer decides whether a change is *proven*, not merely tested: which
lane of tests must run, what coverage means and how to ratchet it, which minimum proof each risk
needs, and how to measure performance instead of intuiting it. Writing tests first is
`test-driven-development`; acceptance from the user's side is `qa-acceptance-evidence`.

## When to use

- Reviewing a change whose evidence is "N tests pass".
- Adding test infrastructure: markers/lanes, coverage, component or browser tests.
- Any change claiming a performance improvement or touching a hot path.

## Principles

- **A test count is not coverage.** Require executed behaviour at the changed boundary, and measured
  branch coverage where the harness exists. [2][3]
- **Coverage is a locator, not a quality score.** Use branch coverage: a line can run without both
  outcomes executing. [2]
- **Lanes are declared, never silently skipped.** A killed, dependency-blocked or deselected run is
  not a passing run. Report unsupported lanes as unsupported.
- **Measure before optimising**, on representative data, on one machine.
- **Thresholds are local policy.** Numbers below are reasonable starting budgets, not industry
  standards; adopt them deliberately and say so.

## Test lanes

Name lanes by *prerequisite*, not business importance, and register them so unknown names fail
(pytest strict markers, [1]):

1. **Contract / fast lane**: deterministic tests with fakes and small generated fixtures; no network,
   downloaded weights, GPU or external services. Aim for a couple of minutes on a dev host.
2. **Tool lane**: real external tools (encoders, aligners, CLIs); prerequisites marked, failing with
   a clear "missing tool" reason.
3. **Hardware / model lane**: real models or devices on the supported host.
4. **Full lane**: no deselection, bounded by per-test and session timeouts.

A change runs the narrow lane that proves it *plus* the broadest lane the worker supports. Record the
exact command, exit code, test count, duration, platform and any deselection.

UI suites have their own layers: pure unit (reducers, formatters, stores) → mounted component with
providers and user events, queried by role/label/name [5] → workspace integration with a controlled
backend (subscriptions, loading/error/empty, toggles, cleanup) → one real-browser smoke per critical
path (emulated DOMs can't reproduce all browser behaviour [4]) → accessibility (keyboard/focus
assertions plus axe; automation is incomplete [6]). Pure logic may stay in node-mode tests; every
changed user interaction needs a mounted test.

## Coverage policy

- Capture an honest line+branch baseline first, excluding only generated/vendor code. Don't pick a
  global percentage by taste.
- Then ratchet: no decrease in total line or branch coverage; ≥90% of changed branches; 100% of
  changed branches at trust boundaries (validation, path containment, upload/resource limits,
  cross-tenant identity, atomic persistence, cache-key generation).
- Every corrected bug has a regression test at the public boundary.
- Exclusions are narrow, justified inline, reviewed. Keep separate floors per language/suite.
- Coverage tools can fail the run below a floor (`coverage report --fail-under`, Vitest thresholds)
  [2][3]. Add coverage commands only after the repo declares the provider; never smuggle the
  dependency in through a review.

## Minimum proof per risk

| Risk | Minimum proof |
|---|---|
| Schema/input | valid, malformed, wrong type, lower/upper boundary, unknown field/coercion policy |
| Cross-tenant access | valid ID in the selected scope, valid ID in another scope, missing ID |
| Persistence | round trip, malformed existing file, concurrent writers, interrupted write, permission failure |
| Cache | same semantic input hits; every one-field change misses; unrelated field stays stable |
| Event subscription | receives relevant event, ignores foreign scope, unsubscribes on unmount/rebind |
| Async job | success, failure, cancellation, duplicate click/idempotency, stale completion |
| UI interaction | accessible control name, keyboard route, state transition, visible error/recovery |
| Media transform | finite data, rate/channels, duration/sample count, amplitude/true peak, deterministic metadata |

HTTP frameworks' official test clients (e.g. FastAPI's `TestClient` [16]) cover request/response
contracts; keep direct service tests for failure injection.

## Performance method

1. Name the user action and the acceptable output.
2. Freeze representative data (full-size, realistic), not a toy sample.
3. One cold run, then ≥20 warm repetitions; record median and p95 (and variance).
4. Profile before changing code. React `<Profiler>` reports render duration but adds overhead [11];
   browser latency also includes parsing, style, layout, paint and compositing [19].
5. Compare on the same machine and toolchain only. A reasonable default budget: reject a hot-path
   p95 regression greater than *both* 20% and 100 ms unless the task accepts it.
6. Retest resource growth (subscribers, retained objects, file descriptors) after ~20 repeated
   switches or renders; steady state must not grow unbounded. Bound list rendering, decoding, queues,
   scans and caches, and test cancellation and cleanup.

## Common failures and smallest fixes

| Failure | Smallest complete fix |
|---|---|
| Many tests, unknown blind spots | Branch coverage config and a ratcheted floor; inspect misses |
| Full suite needs special hardware, no fast lane | Register markers; isolate deterministic contract tests |
| Pure-function UI tests only | Mount the changed component; add one browser flow |
| Test asserts the echo of its own input | Re-measure the produced artifact |
| Performance claim from one timing | Cold + 20 warm runs; compare median/p95 |
| Reviewer finds one instance | Search the class; list every file:line in one finding |

## Verification

Commands and lanes recorded with counts and deselections; coverage reported as a delta against the
baseline; each risk touched has its minimum proof; perf numbers include hardware, data, cold/warm,
median and p95.

## Project specifics

The project's engineering skill or `AGENTS.md` supplies the actual lanes and markers, commands,
current baselines and floors, the supported hardware host, and any stricter budgets.

Sources: [references/sources.md](references/sources.md).
