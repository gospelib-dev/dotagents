# Alert delivery wiring, test-fires and rule authoring

Use when creating or changing the triage contact point or notification policy, when asked to prove
"one alert = one triage item", or when authoring a rule. Examples use the Grafana provisioning API
(`/api/v1/provisioning/{contact-points,policies,alert-rules}`).

## Read live state before editing code

1. Contact points: note `uid`, `name`, webhook URL and `disableResolveMessage` for each.
2. Policies: the route tree (receiver, matchers, `group_by`, timings, `continue`).
3. Alertmanager alerts (`/api/alertmanager/grafana/api/v2/alerts`): what is firing now and which
   receivers get it.
4. Diff the repo's constants (contact point name, timings) against live. If they differ, the repo
   adopts the live name, not the other way round.

## Contact point upsert rule

- Match the existing contact point by **name**, then PUT to its real `uid`; live uids are usually
  generated, not the name. A POST with an existing name adds a *second integration* to the same
  receiver, so every alert is delivered twice.
- Renaming the contact point in code without migrating live leaves the old route in place, so both
  routes fire: same double delivery.
- Regression-test the upsert with a mocked request function and a live-shaped
  `[{uid: <generated>, name: <name>}]` list; assert one PUT to that uid and no POST. Confirm the test
  fails on the old code.

## Test-fire recipe (one alert → one item)

1. Create an always-true rule (`vector(1) > 0`, `for: 0s`) with the label your routing matches and a
   **fresh** service label (`service=<triage-test>-<suffix>`): a new label set gives a new
   fingerprint and group, so old group state cannot interfere. Annotate it to tell triage to note
   receipt and close. (Grafana: header `X-Disable-Provenance: true` keeps it editable.)
2. Wait about `group_wait` + one evaluation (~90 s), then list triage runs triggered after the rule's
   creation. Expect exactly one whose group key contains the test service.
3. **Delete the test rule immediately** after delivery. A forgotten always-true rule re-fires every
   repeat interval and spawns a new triage item each time.
4. Wait another ~60 s, re-list, and show no duplicate. Report the run.

## Diagnosing duplicate deliveries

Compare duplicated runs' group key, alert fingerprint and trigger time:

| Pattern | Cause | Action |
|---|---|---|
| Same group key, ~12 h apart | repeat interval on a still-firing alert | By design: dedup comment. If a test rule, delete it. |
| Same group key, ~15–20 s apart, one contact point | HA alertmanager peer-timeout resend | Not configurable in Grafana Cloud; rare; fingerprint dedupe absorbs it. |
| Same group key, near-simultaneous, two receivers on the alert | two webhook routes/integrations | Fix the contact point / route (upsert rule). |
| Different group keys, same second | distinct alerts batched together | Correct: separate runs. |

## Routine concurrency

Keep the triage routine on "always enqueue". "Coalesce/skip if active" policies drop a *different*
alert that arrives while a run is active (distinct alerts often arrive in the same second), delaying
it until the next repeat. Let the fingerprint dedupe handle duplicates.

## Authoring a rule

- Choose the no-data state on purpose. `OK` makes the rule blind when the pipeline dies, so a dark
  cluster reads healthy everywhere. Keep one namespace-wide dead-man's switch
  (`count(up{namespace="<ns>"}) < 1`, no-data → Alerting, `for` ≥ 10 m). `count()` over zero series
  returns empty, so the no-data path is what fires. Scope it to the whole namespace so it fires only
  on total silence and doesn't overlap per-service "down" rules.
- If the expression has no `by (job)` (or similar), a builder that sets `service` from a static
  component yields one fingerprint for everything. Test that the built rule has the intended no-data
  state, service label and unique uid; confirm the test fails on the base branch.
- A new absence rule fires as soon as it syncs if an outage is ongoing; say so in the PR so the first
  triage run isn't read as a regression.

## Applying rule changes

- Merging may not sync. If nothing in CI applies alert config, someone with write credentials must
  run the sync after merge; list it in the PR and the remaining done-when items. An upsert-only sync
  does not delete reverted rules: rollback also needs a DELETE by uid.
- Changing a rule's labels changes the fingerprint of alerts already firing: each sends one fresh
  notification and the fingerprint title search misses the old tracker. Say so in the PR and expect
  one extra triage run per firing alert.
