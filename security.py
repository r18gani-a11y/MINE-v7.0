import os, json, hmac, hashlib, base64

STORE = "mine_security.json"


def _hash(code, salt):
    return hashlib.pbkdf2_hmac("sha256", code.encode(), salt, 200_000)


def set_passcode(code):
    salt = os.urandom(16)
    data = {"salt": base64.b64encode(salt).decode(),
            "hash": base64.b64encode(_hash(code, salt)).decode()}
    with open(STORE, "w") as f:
        json.dump(data, f)


def verify(code):
    with open(STORE) as f:
        d = json.load(f)
    salt = base64.b64decode(d["salt"])
    return hmac.compare_digest(_hash(code, salt), base64.b64decode(d["hash"]))
