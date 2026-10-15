# Role `network_setup`: Provider bridge + networks

Attaches the provider NIC to an OVS bridge and creates the Neutron networks.

| | |
|---|---|
| **Runs on** | compute + network (API calls once on the first controller) |
| **Server World items** | 12, 25 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags network_setup` |

## What it does

- Assert the provider NIC isn't the default-route NIC
- Bring the NIC up without IP, OVS bridge, `ovn-bridge-mappings`
- `flat`: shared network `sharednet1`
- `geneve`: external `public` + `public-subnet`, tenant `private` + `private-subnet`, `router01`

## Key files

- `tasks/main.yml`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `network_mode`, `provider_interface`, `provider_bridge`, `physnet`, `provider_net`, `private_net`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
