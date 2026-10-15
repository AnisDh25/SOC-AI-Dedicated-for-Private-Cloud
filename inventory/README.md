# Inventory

Hosts, groups and variables. Pick the inventory with `-i`; `ansible.cfg` defaults to `hosts.yml`.

| File | Layout |
|---|---|
| `hosts.yml` | All-in-one: every group is `dlp.tekup.world` |
| `hosts-multinode.yml` | 5 nodes: 2 controllers (controller + network node), 2 computes, 1 storage. No HA |
| `hosts-ha.yml` | HA: 3 controllers (also network nodes) behind the VIP `openstack.tekup.world`, 2 computes, 1 storage |
| `lab-bootstrap.yml` | Every lab VM including the workstation; only for `bootstrap-hosts.yml` (hostnames, `/etc/hosts`) |

## Groups

| Group | Runs |
|---|---|
| `controller` | MariaDB/Galera, RabbitMQ, Memcached, Keystone, Glance, Nova API, Placement, Cinder API, Barbican, Manila API, Horizon (+ HAProxy/keepalived in HA) |
| `network` | neutron-server, OVN central, Heat, Designate + BIND 9, Octavia, Gnocchi, Ceilometer central, CloudKitty |
| `compute` | nova-compute, OVN chassis, OVN metadata agent, ceilometer-compute |
| `storage` | cinder-volume, cinder-backup, manila-share |
| `swift_proxy` / `swift_storage` | Swift proxy and rings / Swift storage servers |
| `nfs` | NFS exports (Cinder; Glance and Gnocchi stores in HA) |

Inventory hostnames must be FQDNs. HA turns on automatically when `controller` has more than one host.

| Folder | Content |
|---|---|
| [`group_vars/`](group_vars/README.md) | Variables for all hosts, and secrets |
| [`host_vars/`](host_vars/README.md) | One file per host: IP, NIC, disks |

Back to the [project README](../README.md)
