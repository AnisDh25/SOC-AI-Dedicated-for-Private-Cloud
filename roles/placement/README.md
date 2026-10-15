# Role `placement`: Placement

Resource tracking for Nova, under Apache on 8778.

| | |
|---|---|
| **Runs on** | controller |
| **Server World items** | 07, 08 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags placement` |

## What it does

- Keystone registration, database
- Install, `placement.conf`, bind Apache to `api_bind_host`
- DB sync, publish 8778

## Key files

- `tasks/main.yml`
- `templates/placement.conf.j2`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `vault_db_passwords.placement`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |

Back to the [role index](../README.md) · [project README](../../README.md)
