import os

USER_DATA_DIR = "user_data"

def ensure_user_dir(username):
    user_dir = os.path.join(USER_DATA_DIR, username)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def list_files(username):
    user_dir = os.path.join(USER_DATA_DIR, username)
    return os.listdir(user_dir) if os.path.exists(user_dir) else []

def save_file(username, filename, content):
    user_dir = ensure_user_dir(username)
    filepath = os.path.join(user_dir, filename)
    with open(filepath, "wb") as f:
        f.write(content)
    return filepath

def get_file(username, filename):
    user_dir = os.path.join(USER_DATA_DIR, username)
    filepath = os.path.join(user_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            return f.read()
    return None
