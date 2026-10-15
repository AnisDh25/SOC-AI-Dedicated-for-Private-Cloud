# Role `os_common`: Shared helpers and handlers

Not a deployable role: reusable task files called with `include_role: tasks_from=…`, plus every handler used by the other roles.

| | |
|---|---|
| **Runs on** | every play (meta dependency of all roles) |
| **Server World items** | — |

## What it does

- `db.yml`: create MariaDB databases and grant a user (on the first controller)
- `keystone_register.yml`: Keystone user, roles, catalog services and endpoints
- `apache_listen.yml`: move an Apache-hosted API off `0.0.0.0` to `api_bind_host`, and restart Apache if it still holds the port on all addresses
- `nginx_stream.yml`: publish ports through nginx (single controller) or HAProxy on the VIP (HA)
- `manage.yml`: run `*-manage` DB syncs once, retried (Galera lock timeouts)
- `ovs_external_ids.yml`: idempotent `ovs-vsctl set open . external-ids:…`
- `neutron_common.yml`, `manila_conf.yml`, `nfs_client.yml`, `shared_state_dir.yml`: config shared by several roles
- `handlers/main.yml`: all service restarts; guarded restarts skip services not installed yet

## Key files

- `tasks/*.yml`
- `handlers/main.yml`
- `templates/stream.conf.j2`, `templates/haproxy-listen.cfg.j2`
- `defaults/main.yml` (Swift storage service list)

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `api_bind_host`, `ha_enabled`, `controller_host`

## HA notes

MariaDB restarts are throttled to one node at a time; DB syncs and Keystone calls run once.

## Layout

| Folder | Content |
|---|---|
| `defaults/` | Default variables |
| `handlers/` | Handlers |
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |

Back to the [role index](../README.md) · [project README](../../README.md)
