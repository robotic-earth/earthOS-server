import hashlib
import os 
import json


def hash_password(password):
    #take the input of the password and encrypt
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 1000)
    return salt + hashed



def verify_password(stored, input_password):
    # Verify the input password by re-hashing and comparing it to the stored hash  
    stored_hash = stored[16:]
    input_hash = hashlib.pbkdf2_hmac('sha256', input_password.encode(), salt, 1000)
    return stored_hash == input_hash


def save_user(username, hashed_password, tag="user"):
    # Load existing users and create new user file if it doesn't exist to save users
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}
    users[username] = {
        "Password": hashed_password.hex(),
        "tag": tag
    }


    with open("users.json", "w") as f:
        json.dump(users, f)


def admin_exists():
    # If users dictionary is not empty, admin exists
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
            for user in users.values():
                if user.get("tag") == "admin":
                    return True
            return False
    except (FileNotFoundError, json.JSONDecodeError):
        return False






