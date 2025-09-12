import hashlib
import os
import json

def load_users():
    """Load users from users.json. Returns a dict or empty dict if file missing/invalid."""
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
            return users if isinstance(users, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def hash_password(password):
    """Return a salted hash of the given password."""
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 1000)
    return salt + hashed

def verify_password(stored_hex, input_password):
    """Check if input_password matches the stored hashed password."""
    stored = bytes.fromhex(stored_hex)
    salt = stored[:16]
    stored_hash = stored[16:]
    input_hash = hashlib.pbkdf2_hmac('sha256', input_password.encode(), salt, 1000)
    return stored_hash == input_hash

def save_user(username, hashed_password, tag="user"):
    """Add or update a user in users.json with the given hashed password and tag."""
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
            if not isinstance(users, dict):
                users = {}
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    users[username] = {
        "Password": hashed_password.hex(),
        "tag": tag
    }

    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

def admin_exists():
    """Return True if there is any user tagged 'admin', else False."""
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
            if not isinstance(users, dict):
                return False
            return any(user.get("tag") == "admin" for user in users.values() if isinstance(user, dict))
    except (FileNotFoundError, json.JSONDecodeError):
        return False
