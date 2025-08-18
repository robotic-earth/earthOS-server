import os

BASE_FRONTEND = os.path.join(os.path.dirname(__file__), "../earthOS-frontend")

def get_html(file_name):
    path = os.path.join(BASE_FRONTEND, file_name)
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return f.read()

def get_css(file_name):
    return get_html(file_name)

def get_js(file_name):
    return get_html(file_name)

def get_font(file_name):
    return get_html(file_name)
