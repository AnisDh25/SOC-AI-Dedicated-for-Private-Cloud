# Role `barbican`: Barbican (key manager)

Key manager API (9311/9312) with the simple_crypto plugin.

| | |
|---|---|
| **Runs on** | controller |
| **Server World items** | 36, 37 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags barbican` |

## What it does

- Keystone registration, database
- Install, `barbican.conf` (KEK from the vault)
- DB upgrade, publish 9311/9312

## Key files

- `tasks/main.yml`
- `templates/barbican.conf.j2`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `vault_barbican_kek`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |

Back to the [role index](../README.md) · [project README](../../README.md)
