# Role `swift_proxy`: Swift proxy + rings

Object storage proxy (8080) and the account/container/object rings.

| | |
|---|---|
| **Runs on** | swift_proxy |
| **Server World items** | 38, 39, 41 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags swift_proxy` |

## What it does

- Keystone registration, test project/user `swiftservice`/`swiftuser01`
- Install, `proxy-server.conf` (Keystone auth), `swift.conf`
- Build rings on the first proxy, copy them to the others
- Publish 8080

## Key files

- `tasks/main.yml`
- `templates/proxy-server.conf.j2`
- `../../templates/swift.conf.j2`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `swift_partition_power`, `swift_devices`, `vault_swift_hash_prefix/suffix`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |

Back to the [role index](../README.md) · [project README](../../README.md)
