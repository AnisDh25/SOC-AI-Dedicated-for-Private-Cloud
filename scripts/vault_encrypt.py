"""Encrypt a file in ansible-vault format 1.1 (AES256), same as `ansible-vault encrypt`.

Usage: python vault_encrypt.py <file>
The password is read with getpass and never echoed or stored.
"""
import binascii
import getpass
import hmac
import os
import sys
from hashlib import sha256

from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

HEADER = b"$ANSIBLE_VAULT;1.1;AES256"


def derive(password: bytes, salt: bytes):
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=80, salt=salt, iterations=10000).derive(password)
    return key[:32], key[32:64], key[64:]


def encrypt(plaintext: bytes, password: bytes) -> bytes:
    salt = os.urandom(32)
    k1, k2, iv = derive(password, salt)
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext) + padder.finalize()
    enc = Cipher(algorithms.AES(k1), modes.CTR(iv)).encryptor()
    ct = enc.update(padded) + enc.finalize()
    mac = hmac.new(k2, ct, sha256).hexdigest().encode()
    body = binascii.hexlify(binascii.hexlify(salt) + b"\n" + mac + b"\n" + binascii.hexlify(ct))
    lines = [body[i:i + 80] for i in range(0, len(body), 80)]
    return HEADER + b"\n" + b"\n".join(lines) + b"\n"


def decrypt(vaulttext: bytes, password: bytes) -> bytes:
    lines = vaulttext.strip().split(b"\n")
    assert lines[0] == HEADER
    salt_hex, mac, ct_hex = binascii.unhexlify(b"".join(lines[1:])).split(b"\n", 2)
    salt, ct = binascii.unhexlify(salt_hex), binascii.unhexlify(ct_hex)
    k1, k2, iv = derive(password, salt)
    if not hmac.compare_digest(hmac.new(k2, ct, sha256).hexdigest().encode(), mac):
        raise ValueError("HMAC mismatch")
    dec = Cipher(algorithms.AES(k1), modes.CTR(iv)).decryptor()
    padded = dec.update(ct) + dec.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded) + unpadder.finalize()


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    with open(path, "rb") as f:
        data = f.read()
    if data.startswith(b"$ANSIBLE_VAULT"):
        sys.exit(f"{path} is already vault-encrypted; nothing done.")

    pw = getpass.getpass("New Vault password: ")
    if len(pw) < 8:
        sys.exit("Password too short (min 8 characters); nothing done.")
    if getpass.getpass("Confirm New Vault password: ") != pw:
        sys.exit("Passwords do not match; nothing done.")

    out = encrypt(data, pw.encode())
    if decrypt(out, pw.encode()) != data:  # self-check before overwriting
        sys.exit("Self-check failed; file left unchanged.")

    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(out)
    os.replace(tmp, path)
    print(f"Encryption successful: {path}")


if __name__ == "__main__":
    main()
