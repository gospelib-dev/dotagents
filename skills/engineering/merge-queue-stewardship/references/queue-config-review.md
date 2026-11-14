# Reviewing CI-gate and merge-queue configuration

Applies to PRs that add or change an aggregate required check (a final job with `needs:` + `if:`),
merge-queue rules, or anything that decides what may merge into the integration branch. Examples use
GitHub Actions and Mergify because those are common; the questions carry over to other tools.

## Checklist (in order)

1. **Read the owner's original request.** Map each bullet (queue entry, batching, splitting,
   priority, bot auto-labels, merge method, "required checks green") to a config line.
2. **The aggregate covers its own workflow.** List the workflow's jobs and diff them against the
   aggregate's `needs:`. Test the result predicate with fixtures: success+skipped → pass;
   failure → fail; cancelled → fail.
3. **The aggregate covers every *other* gate.** List every PR-triggered workflow and its job names.
   Any gate outside the aggregate (provenance, licence/rights, migration lint, docs build,
   PR-title/commit checks) stops blocking merges unless the queue conditions require it. This is
   the most likely blocker: an aggregate of one workflow is not "required CI green". Workflows whose
   header comment calls them "blocking" or "only effective as a required check" make the severity
   obvious.
4. **Check what else enforces merges.** Branch protection and rulesets (a 404 means none; rulesets
   may be plan-gated). With neither, the queue tool injects no protection conditions and its own
   conditions are the entire gate.
5. **Path-filtered workflows never report when not triggered**, so requiring their success hangs the
   queue. Correct shapes: "no failed checks" (`#check-failure = 0`) for path-filtered gates on the
   source PR; explicit success (or success-or-skipped for jobs that skip on some events) for
   always-on gates.
6. **Source-PR gates vs batch gates.** Queue tools that test batches on a bot-authored draft PR
   cannot pass PR-title, commit-message or provenance checks there. Require those in the source-PR
   (queue) conditions and set the batch (merge) conditions explicitly to the CI aggregate. Empty
   merge conditions usually mean "reuse queue conditions" — ambiguous; prefer explicit.
7. **Cancellation semantics.** An aggregate with `if: always()` runs after a workflow cancel and
   reports failure, so the queue dequeues as "checks failed" (needs a fix) instead of "interrupted"
   (requeue as is). Recommend `if: ${{ !cancelled() }}`. Step-level `if: always()` on artifact
   uploads is fine; do not list those as instances.
8. **Default-branch activation.** Some queue tools read their config from the forge's *default*
   branch. If that is a frozen branch, the queue is inert until the owner acts. Verify the PR
   documents it; it is an owner decision, not an author defect.
9. **Plan features.** Batching, two-step CI and priorities may be plan-gated; on an unsupported plan
   the tool dequeues with a billing error. If the pricing page does not show it, say "unverified"
   and ask for a dashboard confirmation rather than guessing.
10. **Draft-skip vs queue drafts.** A PR that skips workflows on draft PRs also skips the queue's
    batch PRs (draft, special head prefix). The batch is then never tested, and an `always()`
    aggregate passes with every job skipped. Require an exception for the queue's head prefix.
11. **Integration-branch regressions.** For a long-lived CI PR, list integration commits to CI files
    since the old merge base and confirm each (runner labels, setup actions, aggregate jobs)
    survived the merge resolution.

## Mergify facts worth not re-researching (public docs)

- Validate: `uvx --from mergify-cli mergify config validate --config-file .mergify.yml` (fetches the
  live schema). `mergify config simulate <PR-URL>` exercises conditions against a real PR.
- `merge_queue.dequeued_label` defaults to `dequeued` (also `queued_label: queued`), so a
  `label != dequeued` queue condition really does block automatic re-entry.
- `batch_max_failure_resolution_attempts: null` (default) bisects until the culprit is isolated and
  the others merge; `0` dequeues the whole batch.
- `merge_method: merge` merges each source PR with its own merge commit (individually revertable);
  `merge-batch` / `fast-forward` land the batch as one unit.
- A GitHub check-run name is the job's `name:` without the workflow prefix.
- Docs: rules `docs.mergify.com/merge-queue/rules/`, lifecycle and dequeue reasons
  `.../merge-queue/lifecycle/`, batches `.../merge-queue/batches/`.
