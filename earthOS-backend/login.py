import hashlib
import os 
import json

def load_users():
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
            if not isinstance(users, dict):
                return {}
            return users
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def hash_password(password):
    # Take the input of the password and encrypt
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 1000)
    return salt + hashed

def verify_password(stored_hex, input_password):
    # Convert stored hex string back to bytes
    stored = bytes.fromhex(stored_hex)
    salt = stored[:16]  # First 16 bytes are the salt
    stored_hash = stored[16:]  # The rest is the actual hashed password

    input_hash = hashlib.pbkdf2_hmac('sha256', input_password.encode(), salt, 1000)

    return stored_hash == input_hash

def save_user(username, hashed_password, tag="user"):
    # Load existing users and create new user file if it doesn't exist to save users
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
            if not isinstance(users, dict):  # Ensure users is a dictionary
                users = {}
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}
    users[username] = {
        "Password": hashed_password.hex(),
        "tag": tag
    }
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)  # Add indent for readable JSON

def admin_exists():
    # If users dictionary is not empty, check for admin
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
            if not isinstance(users, dict):  # Ensure users is a dictionary
                return False
            for user in users.values():
                if isinstance(user, dict) and user.get("tag") == "admin":  # Check if user is a dict
                    return True
            return False
    except (FileNotFoundError, json.JSONDecodeError):
        return False