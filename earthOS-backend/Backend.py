from http.server import HTTPServer, BaseHTTPRequestHandler
from http import cookies
import os
import secrets
import login
import urllib.parse
import mimetypes
import json
import files
import user_data
import base64

mimetypes.add_type("font/ttf", ".ttf")


class EarthOSHandler(BaseHTTPRequestHandler):
    sessions = {}

    def do_GET(self):
        if self.path == "/login":
            self.send_response(200)
            self.send_header("content-type", "text/html")
            self.end_headers()
            self.wfile.write(files.get_html("earthOS-login-frontend/login.html"))

        elif self.path == "/api/admin-exists":
            exists = login.admin_exists()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"exists": exists}).encode())

        elif self.path == "/universal-style.css":
            self.send_response(200)
            self.send_header("content-type", "text/css")
            self.end_headers()
            self.wfile.write(files.get_css("universal-style.css"))

        elif self.path.endswith(".js"):
            self.send_response(200)
            self.send_header("content-type", "application/javascript")
            self.end_headers()
            if "login" in self.path:
                self.wfile.write(files.get_js("earthOS-login-frontend/login.js"))
            elif "home" in self.path:
                self.wfile.write(files.get_js("earthOS-home-frontend/home.js"))
            elif "widget" in self.path:
                self.wfile.write(files.get_js("earthOS-home-frontend/widget.js"))

        elif self.path == "/home":
            cookie_header = self.headers.get("Cookie")
            if cookie_header:
                cookie = cookies.SimpleCookie(cookie_header)
                session_id = cookie.get("session_id")
                if session_id and session_id.value in EarthOSHandler.sessions:
                    self.send_response(200)
                    self.send_header("content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(files.get_html("earthOS-home-frontend/home.html"))
                    return
            self.send_response(302)
            self.send_header("Location", "/login")
            self.end_headers()

        elif self.path.endswith(".ttf"):
            self.send_response(200)
            self.send_header("content-type", "font/ttf")
            self.end_headers()
            relative_path = self.path.lstrip("/")
            self.wfile.write(files.get_font(relative_path))

        else:
            self.send_response(302)
            self.send_header("Location", "/login")
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Parse JSON or form-encoded
        if "application/json" in self.headers.get("Content-Type", ""):
            try:
                parsed_data = json.loads(post_data)
                username = parsed_data.get("username", "")
                password = parsed_data.get("password", "")
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid JSON")
                return
        else:
            parsed_data = urllib.parse.parse_qs(post_data)
            username = parsed_data.get('username', [''])[0]
            password = parsed_data.get('password', [''])[0]

        # --- Handle save-file API first ---
        if self.path == "/api/save-file":
            try:
                data = json.loads(post_data)
                username = data.get("username")
                subdir = data.get("subdir", "documents")
                filename = data.get("filename")
                content_b64 = data.get("content")

                if not all([username, filename, content_b64]):
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Missing required fields")
                    return

                content_bytes = base64.b64decode(content_b64)
                user_data.startup_user(username)  # ensure user folders exist
                filepath = user_data.save_file(username, filename, content_bytes, subdir="home/" + subdir)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"Saved file to {filepath}".encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error: {str(e)}".encode())
            return

        # --- Handle admin creation if no admin exists ---
        if not login.admin_exists():
            if username.strip() == "":
                self.send_response(302)
                self.send_header("Location", "/login?error=empty_username")
                self.end_headers()
                return
            hashed_password = login.hash_password(password)
            login.save_user(username, hashed_password, tag="admin")
            user_data.startup_user(username)  # create user folders & OS info
            self.send_response(302)
            self.send_header("Location", "/login")
            self.end_headers()
            return

        # --- Handle normal login ---
        users = login.load_users()
        stored_hash = users.get(username, {}).get("Password")
        if stored_hash and login.verify_password(stored_hash, password):
            session_id = secrets.token_hex(16)
            EarthOSHandler.sessions[session_id] = username
            self.send_response(302)
            self.send_header("Location", "/home")
            self.send_header("Set-Cookie", f"session_id={session_id}; Max-Age=57600; HttpOnly; Path=/")
            self.end_headers()
            return
        else:
            self.send_response(302)
            self.send_header("Location", "/login?error=invalid_credentials")
            self.end_headers()
            return


# --- Start the server ---
server = HTTPServer(('0.0.0.0', 8080), EarthOSHandler)
print("Backend is running")
server.serve_forever()
