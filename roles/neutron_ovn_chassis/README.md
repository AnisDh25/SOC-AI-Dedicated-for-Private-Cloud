# Role `neutron_ovn_chassis`: OVN chassis

ovn-controller on every chassis; OVN metadata and DHCP agents on compute nodes.

| | |
|---|---|
| **Runs on** | compute + network |
| **Server World items** | 11, 24 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags neutron_ovn_chassis` |

## What it does

- Install ovn-host (+ Neutron agents on computes)
- Neutron config and the OVN metadata agent on computes
- Point ovn-controller at the southbound cluster, Geneve tunnels on the host IP, gateway option

## Key files

- `tasks/main.yml`
- `templates/neutron_ovn_metadata_agent.ini.j2`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `compute_is_gateway_chassis`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |

Back to the [role index](../README.md) · [project README](../../README.md)
