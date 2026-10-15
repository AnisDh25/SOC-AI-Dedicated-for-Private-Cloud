# Role `rabbitmq`: RabbitMQ

Message queue. Single server, or a cluster with mirrored queues in HA.

| | |
|---|---|
| **Runs on** | controller |
| **Server World items** | 02 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags rabbitmq` |

## What it does

- Install RabbitMQ
- HA: shared Erlang cookie, join the first controller's cluster, `ha-all` policy
- User `openstack` with full permissions

## Key files

- `tasks/main.yml`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `vault_rabbit_password`, `vault_rabbit_erlang_cookie`

## HA notes

Every service's `transport_url` lists all controllers.

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
