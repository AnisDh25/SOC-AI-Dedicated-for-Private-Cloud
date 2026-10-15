# Role `memcached`: Memcached

Cache for Keystone tokens and Horizon sessions, listening on the management IP.

| | |
|---|---|
| **Runs on** | controller |
| **Server World items** | 02 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags memcached` |

## What it does

- Install memcached
- `-l <mgmt_ip>`

## Key files

- `tasks/main.yml`

## HA notes

One per controller; services get all of them in `memcached_servers`.

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
