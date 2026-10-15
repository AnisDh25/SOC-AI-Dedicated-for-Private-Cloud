# Role `manila_controller`: Manila API

Shared filesystem API (8786) and scheduler, plus the default share type.

| | |
|---|---|
| **Runs on** | controller |
| **Server World items** | 42, 44 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags manila_controller` |

## What it does

- Keystone registration, database
- Install, `manila.conf` (shared)
- DB sync, publish 8786, share type `default_share_type`

## Key files

- `tasks/main.yml`
- `../../templates/manila.conf.j2`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
