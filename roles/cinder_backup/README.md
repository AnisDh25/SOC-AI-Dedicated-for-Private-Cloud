# Role `cinder_backup`: Cinder backup

cinder-backup to the NFS backup share.

| | |
|---|---|
| **Runs on** | storage |
| **Server World items** | 32 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags cinder_backup` |

## What it does

- Install cinder-backup, NFS client
- `cinder.conf` backup settings

## Key files

- `tasks/main.yml`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `enable_cinder_backup`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
