# Role `nova_compute`: Nova compute

Hypervisor nodes (KVM, or QEMU when `/dev/kvm` is missing).

| | |
|---|---|
| **Runs on** | compute |
| **Server World items** | 09, 17 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags nova_compute` |

## What it does

- Install nova-compute, open-iscsi (LVM volumes) and nfs-common (NFS volumes)
- `nova.conf`, libvirt `virt_type`
- Wait until the host registers, then `nova-manage cell_v2 discover_hosts`

## Key files

- `tasks/main.yml`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `nova_allow_qemu_fallback`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
