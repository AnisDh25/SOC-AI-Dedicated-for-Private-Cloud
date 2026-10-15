# Role `mariadb`: MariaDB / Galera

Database for every service. Single server, or a 3-node Galera cluster in HA.

| | |
|---|---|
| **Runs on** | controller |
| **Server World items** | 02 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags mariadb` |

## What it does

- Install MariaDB (+ galera-4, rsync in HA); `bind-address`, `max_connections`
- HA: write `60-galera.cnf`, bootstrap the cluster once (`galera_new_cluster` on the first controller, others join one at a time)
- HA: apply changed Galera settings with a rolling restart
- HA: wait for `wsrep_cluster_size` = number of controllers, publish 3306 on the VIP (one active node, others backup)

## Key files

- `tasks/main.yml`
- `templates/galera.cnf.j2`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `galera_provider_options` (failure-detection timeouts for slow/freezing VMs)

## HA notes

After a full outage, run `galera_new_cluster` on the node with `safe_to_bootstrap: 1`.

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |
| `templates/` | Jinja2 config templates |

Back to the [role index](../README.md) · [project README](../../README.md)
