# Role `cinder_volume`: Cinder volume

cinder-volume with an LVM backend (iSCSI/LIO) and an NFS backend.

| | |
|---|---|
| **Runs on** | storage |
| **Server World items** | 28, 29, 30, 31 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags cinder_volume` |

## What it does

- Check the disk, install cinder-volume + targetcli
- Volume group `vg_volume01`
- `cinder.conf`, `nfs_shares`, wait for the NFS mount

## Key files

- `tasks/main.yml`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `cinder_lvm_device`, `cinder_vg`, `cinder_backends`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
