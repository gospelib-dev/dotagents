# API maps (read-only)

## Proxmox VE API (`/api2/json`, role PVEAuditor)

Auth header: `Authorization: PVEAPIToken=<user>@<realm>!<tokenid>=<secret>` (keep it out of argv
where you can). All calls are GET.

| Path | Answers |
|---|---|
| `/cluster/resources` | every VM, container, storage and node with status, CPU, memory, disk — start here |
| `/nodes` | node list |
| `/nodes/<node>/status` | host CPU, memory, uptime, load |
| `/nodes/<node>/qemu`, `/nodes/<node>/lxc` | VMs and containers |
| `/nodes/<node>/lxc/<vmid>/status/current` (or `qemu/…`) | one guest's live status |
| `/nodes/<node>/storage` | storage pools and usage |
| `/nodes/<node>/disks/list` | physical disks and SMART health |
| `/cluster/tasks` | recent tasks (failed backups show here) |
| `/cluster/backup` | backup job definitions |
| `/nodes/<node>/tasks?limit=50&errors=1` | recent failed tasks |

## UniFi Site Manager API (cloud, read-only key)

Base `https://api.ui.com/ea/` (early-access path at time of writing). Headers:
`X-API-KEY: <key>` and `Accept: application/json`. GET only.

| Path | Answers |
|---|---|
| `hosts` | consoles: firmware, uptime, WAN/IP, update availability |
| `sites` | sites with statistics: client counts, ISP info, critical notifications, offline devices |
| `devices` | every device per host: model, online/offline, firmware, IP |
| `isp-metrics/5m`, `isp-metrics/1h` | internet latency, packet loss, download/upload, uptime |

Pagination: responses may include `nextToken`; pass `?nextToken=…` for the next page.
