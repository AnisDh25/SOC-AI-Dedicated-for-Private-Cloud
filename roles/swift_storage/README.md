# Role `swift_storage`: Swift storage

Account, container and object servers on XFS devices (disk or loop file).

| | |
|---|---|
| **Runs on** | swift_storage |
| **Server World items** | 40 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags swift_storage` |

## What it does

- Install, format and mount devices under `/srv/node`
- Server configs, rsync
- Copy the rings, start the services

## Key files

- `tasks/main.yml`
- `templates/*-server.conf.j2`
- `templates/rsyncd.conf.j2`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `swift_devices`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |

Back to the [role index](../README.md) · [project README](../../README.md)
