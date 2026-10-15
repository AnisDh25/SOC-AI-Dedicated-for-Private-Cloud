# Role `gnocchi`: Gnocchi (metrics)

Time-series metric store (8041).

| | |
|---|---|
| **Runs on** | network |
| **Server World items** | 52 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags gnocchi` |

## What it does

- Keystone registration, database
- HA: `gnocchi` user with fixed UID and the NFS metric store
- Install, `gnocchi.conf` (HA: coordination through MariaDB)
- `gnocchi-upgrade`, publish 8041

## Key files

- `tasks/main.yml`
- `templates/gnocchi.conf.j2`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `gnocchi_uid`, `nfs_gnocchi_path`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |

Back to the [role index](../README.md) · [project README](../../README.md)
