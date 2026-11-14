---
name: local-web-app-hardening
description: Use when building or reviewing a loopback/local web app. Boundaries, limits.
metadata:
  version: "0.1.0"
  status: draft
  owner: Lance
---

# Local web app hardening

"Local" narrows exposure; it does not erase trust boundaries. A desktop-style app that serves an
HTTP API to a browser on the same machine reads user content, writes project files, launches
expensive jobs, and is reachable by any page the user visits. This skill is the boundary review for
such apps (and a good baseline for any small web service).

## When to use

Building or reviewing routes, uploads, file paths, persistence, job queues or event streams in an
app that binds to loopback or a LAN; any request to expose such an app beyond loopback.

## Principles

- **Loopback is exposure reduction, not authentication.** Keep the default server on loopback
  (Uvicorn documents `127.0.0.1` as its default host [10]). Any non-loopback mode needs an explicit
  threat model and access control: authentication, origin policy, TLS and discovery. Stop and ask
  rather than silently binding `0.0.0.0`.
- **Validate before mutation, at the boundary.** Parse untrusted input once into a trusted type;
  prefer strict validation where coercion would hide an error (e.g. Pydantic strict mode [17]).
- **Cap work before doing it.** Bytes, item counts, durations and concurrency are limited *before*
  the full read or the expensive job.
- **Ownership is checked at the service boundary**, not only filtered in the UI.

## Boundary inventory

| Boundary | Abuse/failure to test | Required control |
|---|---|---|
| CLI host/port | accidental LAN exposure | loopback default; explicit warning/auth decision for non-loopback |
| HTTP body/upload | memory/disk/CPU exhaustion | total-body/file/count/time limits before full read; boundary tests |
| Path or filename | traversal, absolute path, symlink escape | normalise/resolve, then verify containment under the intended root |
| Tenant/project/item IDs | cross-scope read/write | ownership lookup at the service boundary |
| YAML/JSON/cache files | corruption, lost update | strict schema, locks, atomic replace, backup/recovery policy |
| SSE/websocket stream | leak, dead subscriber, foreign-scope event | disconnect handling, bounded queues, scope filtering, cleanup |
| Background/render job | queue/VRAM/CPU exhaustion | bounded concurrency, cancellation, timeout, dedupe, status |
| Static UI + API | CSRF/origin confusion | explicit origin policy; protect state-changing routes |
| Logs/errors | content/path/token disclosure | structured redaction, user-safe errors |

## Uploads

Framework upload objects often wrap a spooled temp file (FastAPI's `UploadFile` [7]); spooling
avoids holding every byte during parsing, but `file.file.read()` with no size still materialises the
whole upload. OWASP API4 lists maximum upload size, memory, execution time, process/descriptor counts
and per-request operation counts as resource controls [8]. For every upload:

1. An application/router body cap before route logic.
2. Check the measured size; don't trust only `Content-Length`.
3. Stream/decode with maximums (for media: duration, sample rate, channels, sample count).
4. Reject unsupported, corrupt or polyglot content based on the decoder result, not the filename.
5. Write only beneath a generated, app-owned path; never use the client filename.
6. Close temporary resources on every error path.
7. Test: zero bytes, malformed bytes, exactly-at-limit, one byte over, decompression/duration bomb,
   duplicate concurrent upload, cancelled client.

## CSRF and origin

"Simple" form content types can be sent cross-site without a CORS preflight; OWASP recommends CSRF
defences or custom-header patterns for state-changing requests [9]. So:

- Never claim CORS proves a mutating localhost API safe.
- Inventory every POST/PATCH/DELETE and whether a foreign page could issue it.
- If the service stays unauthenticated, use a per-launch secret or custom header and narrow allowed
  origins, or document and test an equivalent design.
- Keep GET/HEAD side-effect free.

Product-level auth UX for external access is an owner decision.

## Paths and persistence

Path containment:

```python
candidate = (root / user_relative).resolve()
candidate.relative_to(root.resolve())  # raises ValueError → reject
```

Then handle symlinks and time-of-check/time-of-use for the actual operation. Never use string-prefix
comparison.

For every read-modify-write resource: one shared lock; parse/validate before mutation; write a
sibling temp file, flush and close, then atomic replace; preserve the old file on failure; test
concurrent writers and injected failures. Never widen a critical section casually. Reading
historical data needs fixtures for every supported version.

Cache keys include every input that can change the output bytes; a cache hit is an assertion that
two results are semantically identical. Test each key field: same input hits, a change to only that
field misses.

## UI correctness at the boundary

Status and errors not conveyed only by colour or animation; focus restored after dialogs; honest
disabled/loading states; cancellation and recovery for long operations; no destructive action hidden
behind a mock success message. Full method: `web-accessibility-check`.

## Never log

Uploaded user content, tokens, absolute private paths, or model/service secrets.

## Verification

Each boundary in the inventory touched by the change has its control and a boundary test
(at-limit and one-over for limits; traversal/symlink/cross-scope for paths and IDs; concurrent and
interrupted writes for persistence); every mutating route has a documented origin decision.

## Project specifics

The project's engineering skill or `AGENTS.md` supplies the actual limits (product-approved upload
size, durations), the data root, the ID scheme, the job scheduler and model residency caps, and
whether any non-loopback mode is sanctioned.

Sources: numbered as in `test-lanes-and-coverage` → `references/sources.md` ([7] FastAPI Request
Files, [8] OWASP API4:2023, [9] OWASP CSRF Cheat Sheet, [10] Uvicorn Settings, [17] Pydantic Strict
Mode).
