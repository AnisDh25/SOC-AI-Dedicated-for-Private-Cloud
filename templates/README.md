# templates

Config templates shared by several roles. Each one renders different sections depending on the host's groups,
so a node in several groups gets one combined file.

| Template | Rendered to | Used by roles |
|---|---|---|
| `nova.conf.j2` | `/etc/nova/nova.conf` | `nova_controller`, `nova_compute` |
| `neutron.conf.j2` | `/etc/neutron/neutron.conf` | `neutron_server`, `neutron_ovn_chassis` |
| `ml2_conf.ini.j2` | `/etc/neutron/plugins/ml2/ml2_conf.ini` | `neutron_server`, `neutron_ovn_chassis` |
| `cinder.conf.j2` | `/etc/cinder/cinder.conf` | `cinder_controller`, `cinder_volume`, `cinder_backup` |
| `manila.conf.j2` | `/etc/manila/manila.conf` | `manila_controller`, `manila_share` |
| `ceilometer.conf.j2` | `/etc/ceilometer/ceilometer.conf` | `ceilometer_central`, `ceilometer_compute` |
| `swift.conf.j2` | `/etc/swift/swift.conf` | `swift_proxy`, `swift_storage` |
| `keystonerc.j2` | `/root/keystonerc*` | `keystone`, `bootstrap`, `swift_proxy` |

Role-specific templates live in each role's own `templates/` folder.

Back to the [project README](../README.md)
