# Role `bootstrap`: Users and flavors

Demo project, user and flavors.

| | |
|---|---|
| **Runs on** | first controller |
| **Server World items** | 13, 14 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags bootstrap` |

## What it does

- Project `hiroshima`, user `serverworld` (member)
- `keystonerc_serverworld`
- Flavors m1.tiny … m2.medium

## Key files

- `tasks/main.yml`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `demo_project`, `demo_user`, `flavors`, `vault_demo_user_password`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
