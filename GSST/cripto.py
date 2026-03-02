import base64

from cryptography.fernet import Fernet
from decouple import config


def _fernet() -> Fernet:
    key = config("IP_ENC_KEY").encode()
    return Fernet(key)


def _group(s: str, size: int = 4) -> str:
    return "-".join(s[i:i + size] for i in range(0, len(s), size))


def _ungroup(s: str) -> str:
    return s.replace("-", "")


def encrypt_ip(ip: str) -> str:
    token = _fernet().encrypt(ip.encode())
    raw = base64.urlsafe_b64decode(token)
    pretty = base64.b32encode(raw).decode().rstrip("=")
    return _group(pretty)


def decrypt_ip(token: str) -> str:
    pretty = _ungroup(token)
    pad = "=" * ((8 - len(pretty) % 8) % 8)
    raw = base64.b32decode(pretty + pad)
    fernet_token = base64.urlsafe_b64encode(raw)
    return _fernet().decrypt(fernet_token).decode()
