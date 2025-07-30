import hashlib
import os 
import json

 # Load all users from the users.json file and return them as a dictionary
def load_users():
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
            if not isinstance(users, dict):
                return {}
            return users
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

 # Hash the given password using a salt and return the combined salt and hash
def hash_password(password):
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 1000)
    return salt + hashed

 # Verify the given input_password against the stored hashed password
def verify_password(stored_hex, input_password):
    stored = bytes.fromhex(stored_hex)
    salt = stored[:16]
    stored_hash = stored[16:]
    input_hash = hashlib.pbkdf2_hmac('sha256', input_password.encode(), salt, 1000)
    return stored_hash == input_hash

 # Save a new user with a hashed password and a user tag to users.json
def save_user(username, hashed_password, tag="user"):
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

 # Check if there is any user with the 'admin' tag in users.json
def admin_exists():
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
            if not isinstance(users, dict):  
                return False
            for user in users.values():
                if isinstance(user, dict) and user.get("tag") == "admin":  
                    return True
            return False
    except (FileNotFoundError, json.JSONDecodeError):
        return False