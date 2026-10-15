# Role `smoke_test`: End-to-end tests

Creates the guide's example resources as the demo user to prove the cloud works.

| | |
|---|---|
| **Runs on** | first controller (only with `create_test_resources=true`) |
| **Server World items** | 15, 29-32, 35, 37, 41, 44, 47, 51 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags smoke_test` |

## What it does

- Security group, keypair, instance `Ubuntu-2404` (+ floating IP in geneve mode)
- Volumes `disk-lvm`/`disk-nfs`, attached
- Heat stack, Barbican secret, Swift container/object, Manila share, DNS zone/record, OVN load balancer

## Key files

- `tasks/main.yml`
- `files/sample-stack.yml`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `create_test_resources`

## Layout

| Folder | Content |
|---|---|
| `files/` | Static files |
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
