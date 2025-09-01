import json
import user_data
from http import cookies

def handle_get(handler, path, session_username):
    if path == "/os/load-widgets":
        if session_username:
            widgets = user_data.load_widgets(session_username)
            handler.send_response(200)
            handler.send_header("Content-type", "application/json")
            handler.end_headers()
            handler.wfile.write(json.dumps({"widgets": widgets}).encode())
        else:
            handler.send_response(302)
            handler.send_header("Location", "/login")
            handler.end_headers()
        return True
    return False


def handle_post(handler, path, session_username, parsed_data):
    if path == "/os/save-widgets" and session_username:
        widgets = parsed_data.get("widgets")
        if widgets is not None:
            user_data.save_widgets(session_username, widgets)
            handler.send_response(200)
            handler.end_headers()
            handler.wfile.write(b"Widgets saved")
        else:
            handler.send_response(400)
            handler.end_headers()
            handler.wfile.write(b"Missing widgets data")
        return True
    return False
