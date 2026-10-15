# Role `common`: Base system

Prepares every node: checks, hostname, `/etc/hosts`, time, Ubuntu Cloud Archive, upgrade, base packages, KVM.

| | |
|---|---|
| **Runs on** | all hosts |
| **Server World items** | 02 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags common` |

## What it does

- Assert the inventory layout (and the HA rules: odd controllers, network = swift_proxy = controllers)
- Hostname, `/etc/hosts` with every node (and the VIP in HA)
- Pre-seed Apache `ports.conf` on controllers in HA so Apache never binds the VIP
- apt cache auto-detect (apt-cacher-ng on the workstation)
- Stop automatic apt runs, wait for the dpkg lock
- Timezone, chrony, `cloud-archive:flamingo`, `apt upgrade`, base packages
- KVM packages on compute nodes; choose `virt_type` kvm/qemu

## Key files

- `tasks/main.yml`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `timezone`, `ntp_servers`, `apt_cache_host`, `apt_cache_port`, `nova_allow_qemu_fallback`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
