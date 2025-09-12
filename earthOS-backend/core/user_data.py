import os
import json

USER_DATA_DIR = "user-data"

def ensure_user_dir(username):
    """Ensure all base directories exist for a user."""
    user_dir = os.path.join(USER_DATA_DIR, username)
    os.makedirs(user_dir, exist_ok=True)
    for subdir in ['home/documents', 'home/photos', 'applications', 'OS']:
        os.makedirs(os.path.join(user_dir, subdir), exist_ok=True)
    return user_dir

def startup_user(username):
    """Initialize a user: create folders and empty widget file."""
    ensure_user_dir(username)
    widgets_file = os.path.join(USER_DATA_DIR, username, "OS", "widgets.json")
    if not os.path.exists(widgets_file):
        with open(widgets_file, "w") as f:
            json.dump([], f)  # always an array for JS

def save_file(username, filename, content, subdir=None):
    """Save a file for a user."""
    user_dir = os.path.join(USER_DATA_DIR, username)
    if subdir:
        user_dir = os.path.join(user_dir, subdir)
    os.makedirs(user_dir, exist_ok=True)
    filepath = os.path.join(user_dir, filename)
    with open(filepath, "wb") as f:
        f.write(content)
    return filepath

def get_file(username, filename, subdir=None):
    """Retrieve a file's content."""
    user_dir = os.path.join(USER_DATA_DIR, username)
    if subdir:
        user_dir = os.path.join(user_dir, subdir)
    filepath = os.path.join(user_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            return f.read()
    return None

def list_files(username, subdir=None):
    """List all files in a user's directory or subdirectory."""
    user_dir = os.path.join(USER_DATA_DIR, username)
    if subdir:
        user_dir = os.path.join(user_dir, subdir)
    if os.path.exists(user_dir):
        return os.listdir(user_dir)
    return []

# --- Widgets functions ---
def save_widgets(username, widgets_data):
    """Save widget layout for a user."""
    widgets_file = os.path.join(USER_DATA_DIR, username, "OS", "widgets.json")
    os.makedirs(os.path.dirname(widgets_file), exist_ok=True)
    json.dump(widgets_data, open(widgets_file, "w"), indent=2)

def load_widgets(username):
    """Load widget layout for a user."""
    widgets_file = os.path.join(USER_DATA_DIR, username, "OS", "widgets.json")
    if os.path.exists(widgets_file):
        with open(widgets_file, "r") as f:
            return json.load(f)
    return []  # return array to match JS expectation
