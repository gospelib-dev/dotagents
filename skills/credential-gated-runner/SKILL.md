---
name: credential-gated-runner
description: Use when building a sudo-gated runner that keeps secrets away from agents.
metadata:
  version: "0.1.0"
  status: draft
  owner: Lance
---

# Credential-gated runner

A pattern for tools that let agents trigger privileged operations without ever holding the
credentials: a dedicated Unix service user owns the secrets, agents get exactly one sudo-allowed
runner, and an approval check decides what the runner may do. Examples: an infrastructure-apply
gate, a deploy runner, a secret-rotation runner, plus the root installer for such a runner.

## When to use

Designing, building, testing or reviewing such a runner or its installer.

## Principles

- **Threat-model every path from the agent user to the secret**, not only the obvious "run apply"
  path. Anything executed with credentials loaded is a read path.
- **Trust nothing the agent can write**: not its checkout, not its refs, not its cwd, not an
  approval store it can edit.
- **Bind approval to the exact artifact, once.** Approvals name a hash, postdate the artifact, and
  are consumed by use.
- **Fail closed and leave a trail.** Every invocation, including crashes, leaves exactly one audit
  line; an unwritable log stops the run.
- **Prove refusals refuse for the intended reason.**

## Procedure

1. **Threat model before coding.**
   - Code the runner executes with credentials loaded (sourced wrappers, IaC `external` data
     sources, providers, build hooks) is a read path. Restrict it to reviewed, merged code (for
     example require `git merge-base --is-ancestor <sha> origin/<integration-branch>`), never "any
     sha on origin", because any agent can push a branch.
   - The source of refs must not be agent-writable. The service user fetches from the forge with
     its own read-only token; never from the agent's checkout, where `refs/remotes/origin/*` can be
     forged.
   - The approval store must not be writable by the agent user. State this as a trust assumption.
   - The installer runs whatever runner is in its checkout: tell the owner to run it from the
     reviewed, merged commit.
2. **Write the runner** (root-owned, 0755, in a system bin dir; agents run it as the service user
   via one sudoers line `agent ALL=(svc) NOPASSWD: /path/to/runner`):
   - `set -euo pipefail; umask 077`. Validate every argument with a strict regex (task key, full
     40-hex SHA) before use.
   - Fixed paths and a fixed `PATH`/`HOME` when running as the service user. Honour test-only path
     overrides only when *not* the service user (sudo's `env_reset` strips them anyway; don't rely on
     that alone).
   - Keep secrets off argv (visible in `ps`). Pass git tokens via `GIT_CONFIG_COUNT/KEY_0/VALUE_0`
     (an `http.<url>.extraheader`), and HTTP bearer headers via stdin (`curl -H @-`).
   - Store the artifact with its sha256 and creation time; require the approval to name the hash and
     to postdate creation. Take the creation time *after* the artifact is durably stored, in ms, and
     compare in ms: a timestamp taken before a slow plan lets an approval granted mid-plan authorise
     the new plan. A re-plan replaces the artifact, so old approvals go stale automatically.
   - Single use: move the artifact to an `applied/<key>-<ts>/` dir before executing it.
   - `cd` into a directory the service user owns before any git or tool call. sudo keeps the
     caller's cwd, which is usually unreadable to the service user, and git then dies with exit 128
     before any decision. Put the `cd` after the "state dir exists" check so that refusal keeps its
     message.
   - Serialise runs with `flock` on a lock file in the state dir.
   - Audit-log every invocation (`$SUDO_USER`, args, decision). Sanitise caller-supplied fields
     (`${v//[^A-Za-z0-9._-]/?}`) so they cannot forge lines. Touch the log before any work so it
     fails closed early. In `refuse()`, print to stderr before logging so the reason shows even if
     the log write kills the run.
   - Exactly one audit line per exit: set a flag in `log()` and add an EXIT trap that logs
     `error: exit N` when nothing was logged, so `set -e` aborts are recorded.
   - Don't run approval checks inside `$(...)`: a refusal in the subshell never reaches the parent's
     trap. Write output to a file in the main shell.
3. **Write the installer** (run once with sudo, idempotent):
   - System user with no login shell. Dirs via `install -d -o -g -m` (config root:svc 0750, state
     svc 0700).
   - Move each credential in with `install -o svc -m 0600`, then `shred -u` the source; omitting a
     file on a re-run keeps the installed one.
   - Sudoers to a temp file, `visudo -cqf`, install at 0440, then a global `visudo -cq`.
   - Pin tool versions to the repo docs; verify downloads against the vendor checksum file, and mark
     it as a shortcut if not signature-verified.
   - End with a negative check: the agent user must not be able to read the secret
     (`sudo -u agent test -r …` → die).
4. **Test without root**, plus a CI job running shellcheck and the tests:
   - Fake binaries on `PATH` that log their argv; a local bare repo as origin with the protected
     branch and an unmerged branch.
   - Stub the approval HTTP API as a `file://` tree (curl reads `file://…/interactions` like the
     endpoint), so no server is needed.
   - One case per refusal path: missing, pending, rejected, wrong user, agent-resolved, wrong
     policy, approved before the artifact, stale hash, tampered artifact, API unreachable, unwritable
     log, unmerged SHA, bad args, replayed approval. For each, assert non-zero exit, that the
     privileged command did not run (count it in the fake's log), that no secret appears in output or
     log, and that exactly one audit line with the expected reason was added (a case can pass by
     tripping an earlier check).
   - Exercise the installer in a user+mount namespace
     ([references/namespace-install-test.md](references/namespace-install-test.md)). Reviewers will
     also want a real root install test: an `install-test.sh` that refuses unless `CI=true`, run on a
     disposable CI runner with sudo, installing twice, checking modes, checking the agent cannot read
     secrets or the clone, and driving the real service-user path up to tool init with fake keys.
     Start that sudo call from an agent-private dir and first assert the service user cannot read it,
     or the result depends on the runner's cwd rather than the real host's condition.
   - Confirm results from the job log (grep the `ok`/`FAIL`/decision lines), not just the check
     status, and paste the job URL and key lines on the task.
5. **PR**: each deviation from the requested design with its reason, the trust assumptions, what the
   install test did not cover, and the rollback (removing the sudoers file and the runner revokes all
   access).

## Pitfalls

- In an approval-gated session, never put unrelated or speculative commands in the same call as real
  work (e.g. a `chmod` on system paths "to test"). One flagged command blocks the whole call, and the
  block forbids retrying it.
- Protected files (a repo's `AGENTS.md`) may be write-blocked by the approval guard. Don't route
  around it; put the proposed text in the PR or task as an owed item.

## Verification

Every refusal case has its own test with the audit reason checked; the negative read check passes
after install; secrets never appear in argv, stdout or logs; the root install test ran on a
disposable runner and its log was read.

## Project specifics

The project's ops-tooling skill or `AGENTS.md` supplies the approval store and its API, the
integration branch, the service user and paths, the pinned tool versions, and which files are
protected.
