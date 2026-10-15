# Role `manila_share`: Manila share

manila-share with the LVM driver exporting NFS shares.

| | |
|---|---|
| **Runs on** | storage |
| **Server World items** | 43, 44 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags manila_share` |

## What it does

- Check the disk, install manila-share + nfs-kernel-server
- `manila.conf` with the `[lvm]` backend, sudoers for privsep
- Volume group `manila-volumes`

## Key files

- `tasks/main.yml`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `manila_lvm_device`, `manila_vg`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
