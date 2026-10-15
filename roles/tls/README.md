# Role `tls`: Self-signed TLS

Creates a lab CA on the first controller and signs one certificate per host; the CA is trusted system-wide so services keep `insecure = false`.

| | |
|---|---|
| **Runs on** | all hosts |
| **Server World items** | replaces Let's Encrypt in 03 |
| **Run alone** | `ansible-playbook -i <inventory> site.yml --tags tls` |

## What it does

- CA key and certificate (10 years) on the first controller
- Host key + CSR on every node, signed by the CA (SANs: FQDN, short name, IP, plus the VIP name on controllers in HA)
- Full chain for nginx, PEM bundle (cert + CA + key) for HAProxy
- CA copied to the control machine as `openstack-lab-ca.crt`

## Key files

- `tasks/main.yml`

## Variables

Set in `inventory/group_vars/all/` (or per host in `inventory/host_vars/`):

- `tls_dir`, `tls_extra_sans`, `vip_fqdn`

## HA notes

Controller certificates include `openstack.tekup.world` and the VIP IP.

## Layout

| Folder | Content |
|---|---|
| `meta/` | Role dependency on `os_common` (handlers and helpers) |
| `tasks/` | Task list (`main.yml` is the entry point) |

Back to the [role index](../README.md) · [project README](../../README.md)
