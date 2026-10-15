# Role `cloudkitty`: CloudKitty (rating)

Rating API (8889, plain HTTP as in the guide) and processor.

| | |
|---|---|
| **Runs on** | network |
| **Server World items** | 58, 59 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags cloudkitty` |

## What it does

- Keystone registration, role `rating`
- Database, install, `cloudkitty.conf`, `metrics.yml`
- DB sync, storage init
- HA: publish 8889 on the VIP
- Enable the hashmap module

## Key files

- `tasks/main.yml`
- `templates/cloudkitty.conf.j2`
- `templates/metrics.yml.j2`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |

Back to the [role index](../README.md) · [project README](../../README.md)
