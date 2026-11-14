# Read-only bank data for an agent (choosing and configuring)

Researched 2026-11-11 (US household). Re-verify vendor terms before relying on them.

## Principles
- **Order of preference:** an official read-only API or MCP server from the provider the household
  already uses > community open source, self-hosted > forks > a custom build on a developer
  aggregator.
- **Scope to read only.** Use a dedicated viewer-role member or an API key granted only read
  scopes. Owner-level OAuth often still exposes transfer or rule-trigger tools that create
  approval-pending proposals; even a proposal violates "never moves money".
- **Secrets:** setup tokens and access URLs that embed credentials are bearer secrets; store them in
  the vault, never in config files or chat.
- **Data gaps to expect:** linked external accounts lag the bank sync; history windows can be
  ~90 days; most providers have no native "bill" object, so infer due dates from recurring
  transactions or keep a bill list.
- **Avoid** unofficial, credential-based APIs (email + password + MFA secret through a
  reverse-engineered API) and stale forks superseded by an official server.

## Options seen (2026-11)
| Option | Type | Read-only? | Notes |
|---|---|---|---|
| A budgeting/banking provider's official API + remote MCP | official | yes, with viewer role or read scopes | best when the household already uses it |
| SimpleFIN Bridge (~$15/yr) | official protocol | read-only by design | daily updates via an aggregator, ~90 days history, no bills object; community MCP/CLI wrappers immature |
| Actual Budget + actual-mcp | community OSS, self-hosted | read-only unless started with a write flag | "schedules" model recurring bills; needs hosting |
| Firefly III + MCP | community OSS | not read-only by default; token gives full API | MCP server stale at research time |
| YNAB API + community MCP | official API | token is unscoped (read/write) | requires adopting YNAB |
| Monarch Money unofficial API | unofficial | write tools exposed | credential-based, breaks on API changes; not recommended |
| Plaid / Teller | official developer APIs | read products exist | custom build: own app, link flow, token storage, mTLS (Teller) |

Sources: https://www.simplefin.org/protocol.html ; https://actualbudget.org/docs/advanced/bank-sync/simplefin ;
https://github.com/actualbudget/actual ; https://github.com/s-stefanov/actual-mcp ;
https://docs.firefly-iii.org/how-to/data-importer/import/simplefin/ ; https://api.ynab.com/ ;
https://github.com/calebl/ynab-mcp-server ; https://github.com/hammem/monarchmoney ;
https://plaid.com/docs/account/billing/ ; https://teller.io/docs/guides/environments/
