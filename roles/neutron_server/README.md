# Role `neutron_server`: Neutron server + OVN central

Neutron API (9696), ML2/OVN, DHCP agent and the OVN northbound/southbound databases.

| | |
|---|---|
| **Runs on** | network |
| **Server World items** | 10, 11, 23 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags neutron_server` |

## What it does

- Keystone registration, database `neutron_ml2`
- Install, `neutron.conf`/`ml2_conf.ini`, bind Apache to `api_bind_host`
- DB migration (retried)
- HA: OVN NB/SB as a RAFT cluster (`/etc/default/ovn-central`), wait for all members
- Gateway chassis option, publish 9696

## Key files

- `tasks/main.yml`
- `templates/ovn-central.default.j2`
- `../../templates/neutron.conf.j2`, `../../templates/ml2_conf.ini.j2`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `ovn_nb_connection`, `ovn_sb_connection`

## HA notes

The first network node creates the OVN cluster; the others join one at a time.

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |

Back to the [role index](../README.md) · [project README](../../README.md)
