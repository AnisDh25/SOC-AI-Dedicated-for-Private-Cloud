# Role `glance`: Glance (images)

Image service on 9292, plus the Ubuntu 24.04 cloud image.

| | |
|---|---|
| **Runs on** | controller |
| **Server World items** | 05, 06 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags glance` |

## What it does

- Keystone registration, database
- HA: `glance` user with fixed UID and the NFS image store mounted from the storage node
- Install, `glance-api.conf`, DB sync, publish on the VIP
- Download and upload `Ubuntu2404` once (`tasks/images.yml`)

## Key files

- `tasks/main.yml`
- `tasks/images.yml`
- `templates/glance-api.conf.j2`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `glance_image_url`, `glance_image_name`, `glance_customize_image`, `glance_uid`, `nfs_glance_path`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |

Back to the [role index](../README.md) · [project README](../../README.md)
