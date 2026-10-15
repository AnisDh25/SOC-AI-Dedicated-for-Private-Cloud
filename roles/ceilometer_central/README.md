# Role `ceilometer_central`: Ceilometer central

Central and notification agents.

| | |
|---|---|
| **Runs on** | network |
| **Server World items** | 53, 55-57 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags ceilometer` |

## What it does

- Keystone registration
- HA: coordination database `tooz`
- Install, `ceilometer.conf` (shared), `ceilometer-upgrade`

## Key files

- `tasks/main.yml`
- `../../templates/ceilometer.conf.j2`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `vault_db_passwords.tooz`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
