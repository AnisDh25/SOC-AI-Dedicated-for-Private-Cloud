# group_vars/all

| File | Content | In git |
|---|---|---|
| `main.yml` | Every setting: domain, topology (derived from groups), HA (VIP, Galera tuning), TLS, networking, storage devices, apt cache, flavors, `enable_*` switches | yes |
| `vault.yml` | Secrets: admin/DB/service passwords, RabbitMQ cookie, Barbican KEK, Swift hash, Horizon key, keepalived password | **no** (`.gitignore`) |
| `vault.yml.example` | Same keys as `vault.yml` with `CHANGE_ME` placeholders | yes |

## Create `vault.yml`

```bash
cp vault.yml.example vault.yml          # then replace every CHANGE_ME value
ansible-vault encrypt vault.yml         # or: python ../../../scripts/vault_encrypt.py vault.yml
```

Keep the values alphanumeric: they are embedded in database and RabbitMQ URLs.

Back to the [group_vars README](../README.md)
