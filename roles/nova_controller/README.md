# Role `nova_controller`: Nova controller

Nova API (8774), metadata (8775), conductor, scheduler and noVNC (6080).

| | |
|---|---|
| **Runs on** | controller |
| **Server World items** | 07, 08 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags nova_controller` |

## What it does

- Keystone registration; databases `nova`, `nova_api`, `nova_cell0`
- Install, `nova.conf` (shared template), API + metadata vhosts
- DB syncs, `map_cell0`, create `cell1` once
- Publish 8774/8775/6080 (noVNC sticky in HA)

## Key files

- `tasks/main.yml`
- `../../templates/nova.conf.j2`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `vault_db_passwords.nova`, `vault_service_passwords.nova`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
