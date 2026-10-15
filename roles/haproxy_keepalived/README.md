# Role `haproxy_keepalived`: VIP: HAProxy + keepalived (HA)

keepalived moves the VIP between controllers; HAProxy on each controller listens on the VIP. Services add their frontends in `/etc/haproxy/conf.d/`.

| | |
|---|---|
| **Runs on** | controller (HA only) |
| **Server World items** | — |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags haproxy` |

## What it does

- `net.ipv4.ip_nonlocal_bind=1` so every controller can bind the VIP
- HAProxy base config with a stats page on :1936
- keepalived VRRP (unicast), priority controller01 > 02 > 03, tracks HAProxy
- Wait until the VIP answers

## Key files

- `tasks/main.yml`
- `templates/haproxy.cfg.j2`
- `templates/keepalived.conf.j2`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `vip_address`, `vip_fqdn`, `vip_prefix`, `vip_interface`, `vip_router_id`, `vault_keepalived_password`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |

Back to the [role index](../README.md) · [project README](../../README.md)
