# Role `heat`: Heat (orchestration)

Orchestration API (8004) and CloudFormation API (8000), plain HTTP as in the guide.

| | |
|---|---|
| **Runs on** | network |
| **Server World items** | 33, 34, 35 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags heat` |

## What it does

- Keystone registration, roles `heat_stack_owner`/`heat_stack_user`, domain `heat` + `heat_domain_admin`
- Database, install, `heat.conf`, WSGI fix
- DB sync, heat-engine; HA: publish 8004/8000 on the VIP

## Key files

- `tasks/main.yml`
- `templates/heat.conf.j2`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `vault_heat_domain_admin_password`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |

Back to the [role index](../README.md) · [project README](../../README.md)
