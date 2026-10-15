# Role `ceilometer_compute`: Ceilometer compute

Polling agent on hypervisors.

| | |
|---|---|
| **Runs on** | compute |
| **Server World items** | 54 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags ceilometer` |

## What it does

- Install ceilometer-agent-compute
- `ceilometer.conf` (shared)

## Key files

- `tasks/main.yml`

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
