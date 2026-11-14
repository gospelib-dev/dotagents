# Query recipes for read-only triage (Grafana / Prometheus / Mimir / Loki)

Calls use a bearer token against the Grafana base URL, going through the datasource proxy. Never
echo the token.

## Endpoints

- Datasource list (uids): `GET /api/datasources`. Grafana Cloud stacks typically name them like
  `grafanacloud-prom`, `grafanacloud-logs`, `grafanacloud-traces`, `grafanacloud-usage`; confirm.
- PromQL instant: `GET /api/datasources/proxy/uid/<prom-uid>/api/v1/query --data-urlencode query=… [time=<unix>]`
- PromQL range: `…/api/v1/query_range` with `start`, `end`, `step`.
- Label values survive data gaps, so they list jobs that *ever* reported: `…/api/v1/label/job/values`.
- LogQL: `GET /api/datasources/proxy/uid/<loki-uid>/loki/api/v1/query` with
  `query=sum(count_over_time({namespace=~".+"}[7d]))`. Empty result = zero log lines.
- Ruler state (which rules sit Normal/NoData): `/api/prometheus/grafana/api/v1/alerts`.

## Is the whole pipeline dark?

1. `count(up)` now. Empty means no scrape target reports at all.
2. Log line counts over 1 d, 7 d and 30 d.
3. A public health URL probed from outside. Cloudflare `530` with body `error code: 1033` means the
   tunnel has no connected connector.

If all three are empty or failing, the runtime host or collector is down, and single-exporter alerts
are symptoms.

## When did a series last exist?

- `query_range` with `step=1h` over ≤32 days; read the first and last returned timestamps; slide the
  window back to bisect.
- Do **not** use `timestamp(last_over_time(x[30d]))`: it returns the evaluation time, not the time of
  the last sample, so every window looks live.
- Mimir rejects ranges over 768 h (`err-mimir-max-query-length`). Keep lookbacks ≤30 d and step the
  evaluation `time` back instead.
- Compare the exporter's own target (`up{job="<exporter>"}`) with the metric it exports. If the
  target drops before all telemetry stops, the exporter has a separate fault to re-check after
  restore.
