import os
import json

USER_DATA_DIR = "user-data"  # base folder for all users

def startup_user(username):
    """
    Ensure that the user's directory structure exists:
      - home/documents
      - home/photos
      - apps
      - os (user-specific OS data like widget positions)
    """
    user_dir = os.path.join(USER_DATA_DIR, username)
    os.makedirs(user_dir, exist_ok=True)

    # Create home subfolders
    home_subfolders = ['documents', 'photos']
    for sub in home_subfolders:
        os.makedirs(os.path.join(user_dir, 'home', sub), exist_ok=True)

    # Create apps folder
    os.makedirs(os.path.join(user_dir, 'apps'), exist_ok=True)

    # Create OS folder
    os.makedirs(os.path.join(user_dir, 'os'), exist_ok=True)

    # Initialize widget positions file if it doesn't exist
    widgets_file = os.path.join(user_dir, 'os', 'widgets.json')
    if not os.path.exists(widgets_file):
        with open(widgets_file, 'w') as f:
            json.dump({}, f, indent=4)

def save_file(username, filename, content, subdir="home/documents"):
    """
    Save a file to a user's folder.
    subdir can be 'home/documents', 'home/photos', 'apps', or 'os'.
    """
    file_dir = os.path.join(USER_DATA_DIR, username, subdir)
    os.makedirs(file_dir, exist_ok=True)
    file_path = os.path.join(file_dir, filename)
    with open(file_path, "wb") as f:
        f.write(content)
    return file_path

def list_files(username, subdir=None):
    """
    List files for a user in a specific folder.
    """
    base_dir = os.path.join(USER_DATA_DIR, username)
    if subdir:
        base_dir = os.path.join(base_dir, subdir)
    if os.path.exists(base_dir):
        return os.listdir(base_dir)
    return []

# --- Widget position management ---
def save_widgets(username, widget_data):
    """
    Save the user's widget positions in JSON format.
    widget_data should be a dictionary mapping widget names to positions/sizes.
    """
    widgets_file = os.path.join(USER_DATA_DIR, username, 'os', 'widgets.json')
    os.makedirs(os.path.dirname(widgets_file), exist_ok=True)
    with open(widgets_file, 'w') as f:
        json.dump(widget_data, f, indent=4)

def load_widgets(username):
    """
    Load the user's widget positions.
    Returns a dictionary; empty if no data exists.
    """
    widgets_file = os.path.join(USER_DATA_DIR, username, 'os', 'widgets.json')
    if os.path.exists(widgets_file):
        with open(widgets_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}
