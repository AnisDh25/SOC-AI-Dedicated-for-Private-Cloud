# Role `nfs_server`: NFS server

Exports for the Cinder NFS backend and backups, plus (HA) the Glance image and Gnocchi metric stores.

| | |
|---|---|
| **Runs on** | nfs |
| **Server World items** | 30, 32 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags nfs_server` |

## What it does

- Install nfs-kernel-server, idmapd domain
- Create and export the directories (fixed owners for Glance/Gnocchi)

## Key files

- `tasks/main.yml`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `nfs_share_path`, `nfs_backup_path`, `nfs_glance_path`, `nfs_gnocchi_path`, `nfs_allowed_network`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
