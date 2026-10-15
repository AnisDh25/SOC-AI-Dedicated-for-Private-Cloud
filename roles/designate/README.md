# Role `designate`: Designate (DNS)

DNS as a service with BIND 9 as the backend.

| | |
|---|---|
| **Runs on** | network |
| **Server World items** | 45, 46, 47 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags designate` |

## What it does

- Keystone registration, database (utf8mb3)
- BIND 9: RNDC key (same on every network node), `named.conf.options`
- `designate.conf`, DB sync, `pools.yaml` (one target per network node), pool update once
- Publish 9001

## Key files

- `tasks/main.yml`
- `templates/designate.conf.j2`
- `templates/named.conf.options.j2`
- `templates/pools.yaml.j2`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `mgmt_network`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |

Back to the [role index](../README.md) · [project README](../../README.md)
