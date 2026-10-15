# scripts

| Script | Purpose |
|---|---|
| `vault_encrypt.py` | Encrypts a file in the `ansible-vault` 1.1 AES256 format without Ansible (useful on Windows). Asks for the password twice, refuses already-encrypted files, and checks its own output before overwriting. Needs Python with `cryptography`. |

```powershell
python scripts\vault_encrypt.py inventory\group_vars\all\vault.yml
```

Back to the [project README](../README.md)
