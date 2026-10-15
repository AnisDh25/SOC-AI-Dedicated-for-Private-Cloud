# Role `nginx`: Nginx TLS stream proxy

Terminates TLS on the management IP and forwards to APIs bound on 127.0.0.1. Each service role drops a file into `/etc/nginx/stream.d/`.

| | |
|---|---|
| **Runs on** | controller, network, swift_proxy (single-controller layouts only) |
| **Server World items** | 05+ |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags nginx` |

## What it does

- Install nginx + stream module
- Add a `stream {}` block with the host certificate
- Disable the default site

## Key files

- `tasks/main.yml`

## HA notes

Skipped in HA: `haproxy_keepalived` publishes the APIs on the VIP instead.

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
