# Role `octavia_ovn`: Octavia (load balancer, OVN provider)

Load balancer API (9876) with the OVN provider driver: no amphora VMs, L4 only.

| | |
|---|---|
| **Runs on** | network |
| **Server World items** | 48-51 (OVN provider instead of amphora) |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags octavia` |

## What it does

- Keystone registration, database
- Install API, driver agent, `ovn-octavia-provider`
- `octavia.conf`, `policy.yaml`
- DB upgrade, stop amphora-only services, publish 9876

## Key files

- `tasks/main.yml`
- `templates/octavia.conf.j2`
- `templates/policy.yaml.j2`

## HA notes

Pools must use `SOURCE_IP_PORT` (the OVN provider doesn't support ROUND_ROBIN).

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |

Back to the [role index](../README.md) · [project README](../../README.md)
