# host_vars

One file per host, named after the inventory hostname (an FQDN). A file only takes effect for hosts that appear in the inventory you use.

| Variable | Meaning |
|---|---|
| `ansible_host` | Address Ansible connects to |
| `ansible_user` | SSH user (needs sudo) |
| `mgmt_ip` | Management IP: services, certificates, `/etc/hosts` |
| `provider_interface` | NIC without IP for the provider/external network (controllers in HA, computes) |
| `cinder_lvm_device`, `manila_lvm_device`, `swift_devices` | Storage node disks |

## Files

| File | Used by |
|---|---|
| `dlp.tekup.world.yml` | all-in-one, multi-node (ctl1) |
| `network.tekup.world.yml` | multi-node (ctl2) |
| `controller01/02/03.tekup.world.yml` | HA controllers |
| `node01.tekup.world.yml`, `node02.tekup.world.yml` | compute nodes |
| `storage.tekup.world.yml` | storage node (disks) |
| `workstation.tekup.world.yml` | Ansible control node (bootstrap only) |

Back to the [inventory README](../README.md)
