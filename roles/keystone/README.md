# Role `keystone`: Keystone (identity)

Identity service on Apache :5000 with TLS.

| | |
|---|---|
| **Runs on** | controller |
| **Server World items** | 03, 04 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags keystone` |

## What it does

- Database, packages, `keystone.conf` (memcache, DB, Fernet)
- DB sync, Fernet + credential keys, bootstrap (admin, RegionOne)
- HA: copy the keys from the first controller to the others
- Enable mod_ssl/mod_wsgi, TLS vhost, publish on the VIP (TLS passthrough)
- `keystonerc`, `clouds.yaml` (admin, demo, swift), role and project `service`

## Key files

- `tasks/main.yml`
- `templates/keystone-apache.conf.j2`
- `templates/clouds.yaml.j2`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `vault_admin_password`, `vault_db_passwords.keystone`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |

Back to the [role index](../README.md) · [project README](../../README.md)
