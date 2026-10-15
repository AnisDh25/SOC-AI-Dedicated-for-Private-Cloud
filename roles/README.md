# Roles

One role per service or step. `site.yml` runs them in the order below, each on its inventory group.
Every role depends on [`os_common`](os_common/README.md), which provides the shared helper tasks and all handlers.

| # | Role | What it sets up | Runs on | Server World |
|---|---|---|---|---|
| 1 | [`common`](common/README.md) | Base system | all hosts | 02 |
| 2 | [`tls`](tls/README.md) | Self-signed TLS | all hosts | replaces Let's Encrypt in 03 |
| 3 | [`nginx`](nginx/README.md) | Nginx TLS stream proxy | controller, network, swift_proxy (single-controller layouts only) | 05+ |
| 4 | [`haproxy_keepalived`](haproxy_keepalived/README.md) | VIP: HAProxy + keepalived (HA) | controller (HA only) | — |
| 5 | [`mariadb`](mariadb/README.md) | MariaDB / Galera | controller | 02 |
| 6 | [`rabbitmq`](rabbitmq/README.md) | RabbitMQ | controller | 02 |
| 7 | [`memcached`](memcached/README.md) | Memcached | controller | 02 |
| 8 | [`keystone`](keystone/README.md) | Keystone (identity) | controller | 03, 04 |
| 9 | [`nfs_server`](nfs_server/README.md) | NFS server | nfs | 30, 32 |
| 10 | [`glance`](glance/README.md) | Glance (images) | controller | 05, 06 |
| 11 | [`placement`](placement/README.md) | Placement | controller | 07, 08 |
| 12 | [`nova_controller`](nova_controller/README.md) | Nova controller | controller | 07, 08 |
| 13 | [`nova_compute`](nova_compute/README.md) | Nova compute | compute | 09, 17 |
| 14 | [`neutron_server`](neutron_server/README.md) | Neutron server + OVN central | network | 10, 11, 23 |
| 15 | [`neutron_ovn_chassis`](neutron_ovn_chassis/README.md) | OVN chassis | compute + network | 11, 24 |
| 16 | [`bootstrap`](bootstrap/README.md) | Users and flavors | first controller | 13, 14 |
| 17 | [`network_setup`](network_setup/README.md) | Provider bridge + networks | compute + network (API calls once on the first controller) | 12, 25 |
| 18 | [`cinder_controller`](cinder_controller/README.md) | Cinder API | controller | 27, 31 |
| 19 | [`cinder_volume`](cinder_volume/README.md) | Cinder volume | storage | 28, 29, 30, 31 |
| 20 | [`cinder_backup`](cinder_backup/README.md) | Cinder backup | storage | 32 |
| 21 | [`barbican`](barbican/README.md) | Barbican (key manager) | controller | 36, 37 |
| 22 | [`manila_controller`](manila_controller/README.md) | Manila API | controller | 42, 44 |
| 23 | [`manila_share`](manila_share/README.md) | Manila share | storage | 43, 44 |
| 24 | [`heat`](heat/README.md) | Heat (orchestration) | network | 33, 34, 35 |
| 25 | [`designate`](designate/README.md) | Designate (DNS) | network | 45, 46, 47 |
| 26 | [`octavia_ovn`](octavia_ovn/README.md) | Octavia (load balancer, OVN provider) | network | 48-51 (OVN provider instead of amphora) |
| 27 | [`swift_proxy`](swift_proxy/README.md) | Swift proxy + rings | swift_proxy | 38, 39, 41 |
| 28 | [`swift_storage`](swift_storage/README.md) | Swift storage | swift_storage | 40 |
| 29 | [`gnocchi`](gnocchi/README.md) | Gnocchi (metrics) | network | 52 |
| 30 | [`ceilometer_central`](ceilometer_central/README.md) | Ceilometer central | network | 53, 55-57 |
| 31 | [`ceilometer_compute`](ceilometer_compute/README.md) | Ceilometer compute | compute | 54 |
| 32 | [`cloudkitty`](cloudkitty/README.md) | CloudKitty (rating) | network | 58, 59 |
| 33 | [`horizon`](horizon/README.md) | Horizon (dashboard) | controller | — (not in the series) |
| 34 | [`smoke_test`](smoke_test/README.md) | End-to-end tests | first controller (only with `create_test_resources=true`) | 15, 29-32, 35, 37, 41, 44, 47, 51 |

Helper role: [`os_common`](os_common/README.md).

## Role layout

Each role follows Ansible's standard structure:

| Folder | Content |
|---|---|
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `handlers/` | Handlers |
| `defaults/` | Default variables |
| `files/` | Static files |

Back to the [project README](../README.md)
