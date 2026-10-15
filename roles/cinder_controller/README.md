# Role `cinder_controller`: Cinder API

Block storage API (8776) and scheduler, plus the volume types.

| | |
|---|---|
| **Runs on** | controller |
| **Server World items** | 27, 31 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags cinder_controller` |

## What it does

- Keystone registration, database
- Install, `cinder.conf` (shared), bind Apache
- DB sync, publish 8776
- Volume types `lvm` and `nfs` (once)

## Key files

- `tasks/main.yml`
- `../../templates/cinder.conf.j2`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `enable_cinder_nfs`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
