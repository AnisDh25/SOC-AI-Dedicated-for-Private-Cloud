# Role `horizon`: Horizon (dashboard)

Web dashboard at `https://<controller or VIP>/horizon`.

| | |
|---|---|
| **Runs on** | controller |
| **Server World items** | — (not in the series) |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags horizon` |

## What it does

- Install openstack-dashboard + plugins for enabled services
- `local_settings.py` overrides (Keystone URL, memcached, TLS, secret key)
- HTTPS site with the host certificate, HTTP → HTTPS redirect
- HA: publish 80/443 on the VIP (sticky)

## Key files

- `tasks/main.yml`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `vault_horizon_secret_key`, `timezone`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
