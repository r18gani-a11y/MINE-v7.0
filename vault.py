import os, json, uuid, base64, hashlib
from cryptography.fernet import Fernet

VAULT_DIR = "vault_data"
SALT_FILE = os.path.join(VAULT_DIR, "salt.bin")
INDEX = os.path.join(VAULT_DIR, "index.json")
_fernet = None


def init(code):
    """Derive an encryption key from the passcode."""
    global _fernet
    os.makedirs(VAULT_DIR, exist_ok=True)
    if not os.path.exists(SALT_FILE):
        with open(SALT_FILE, "wb") as f:
            f.write(os.urandom(16))
    with open(SALT_FILE, "rb") as f:
        salt = f.read()
    key = hashlib.pbkdf2_hmac("sha256", code.encode(), salt, 200_000)
    _fernet = Fernet(base64.urlsafe_b64encode(key))


def _index():
    if not os.path.exists(INDEX):
        return {}
    with open(INDEX) as f:
        return json.load(f)


def add_file(name, data: bytes):
    fid = uuid.uuid4().hex
    with open(os.path.join(VAULT_DIR, fid + ".enc"), "wb") as f:
        f.write(_fernet.encrypt(data))
    idx = _index()
    idx[fid] = name
    with open(INDEX, "w") as f:
        json.dump(idx, f)
    return fid


def get_file(fid):
    with open(os.path.join(VAULT_DIR, fid + ".enc"), "rb") as f:
        return _fernet.decrypt(f.read())


def list_files():
    return [(fid, name, None) for fid, name in _index().items()]
