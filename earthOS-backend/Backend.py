from http.server import BaseHTTPRequestHandler
from http import cookies
import mimetypes
import json
import urllib.parse
import secrets
import core.login as login
import core.files as files
import os_api.widget_api as os_api
import app_api.save as app_api
import core.user_data as user_data

# Ensure fonts are served with correct type
mimetypes.add_type("font/ttf", ".ttf")


class EarthOSHandler(BaseHTTPRequestHandler):
    sessions = {}  # session_id -> usernamimport core.user_datae mapping

    # --- Helper Methods ---
    def serve_file(self, content, content_type):
        """Send a 200 with given bytes content; if content is None send 404."""
        if content is None:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(content)

    def redirect(self, path):
        self.send_response(302)
        self.send_header("Location", path)
        self.end_headers()

    def get_session_username(self):
        cookie_header = self.headers.get("Cookie")
        if cookie_header:
            cookie = cookies.SimpleCookie(cookie_header)
            session_id = cookie.get("session_id")
            if session_id and session_id.value in EarthOSHandler.sessions:
                return EarthOSHandler.sessions[session_id.value]
        return None

    # --- GET Requests ---
    def do_GET(self):
        session_username = self.get_session_username()

        # OS API handling first (handles /os/*)
        if os_api.handle_get(self, self.path, session_username):
            return

        # App API GET (placeholder - if you later add GET routes for apps)
        # if app_api.handle_get(self, self.path, session_username):
        #     return

        # Keep quick admin-exists check available for the frontend
        if self.path == "/api/admin-exists":
            exists = login.admin_exists()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"exists": exists}).encode())
            return

        # Serve frontend pages and static files
        if self.path == "/login":
            self.serve_file(files.get_html("earthOS-login-frontend/login.html"), "text/html")
        elif self.path == "/home":
            if session_username:
                self.serve_file(files.get_html("earthOS-home-frontend/home.html"), "text/html")
            else:
                self.redirect("/login")
        elif self.path.endswith(".js"):
            # naive mapping based on filename presence
            if "login" in self.path:
                self.serve_file(files.get_js("earthOS-login-frontend/login.js"), "application/javascript")
            elif "home" in self.path and "widget" not in self.path:
                self.serve_file(files.get_js("earthOS-home-frontend/home.js"), "application/javascript")
            elif "widget" in self.path:
                self.serve_file(files.get_js("earthOS-home-frontend/widget.js"), "application/javascript")
            else:
                # try to serve any JS by passing the stripped leading slash
                self.serve_file(files.get_js(self.path.lstrip("/")), "application/javascript")
        elif self.path == "/universal-style.css":
            self.serve_file(files.get_css("universal-style.css"), "text/css")
        elif self.path.endswith(".ttf"):
            self.serve_file(files.get_font(self.path.lstrip("/")), "font/ttf")
        else:
            # fallback to login
            self.redirect("/login")

    # --- POST Requests ---
    def do_POST(self):
        # Read body
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")

        # Parse JSON or form-encoded bodies
        if "application/json" in self.headers.get("Content-Type", ""):
            try:
                parsed_data = json.loads(post_data) if post_data else {}
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid JSON")
                return
        else:
            parsed_qs = urllib.parse.parse_qs(post_data)
            parsed_data = {k: v[0] for k, v in parsed_qs.items()}

        username = parsed_data.get("username", "")
        password = parsed_data.get("password", "")
        session_username = self.get_session_username()

        # --- LOGIN & ADMIN CREATION (explicitly handle /login) ---
        if self.path == "/login":
            # If no admin exists yet, create the admin user
            if not login.admin_exists():
                if username.strip() == "":
                    # If frontend sends empty username, redirect back with error (frontend parses query if you want)
                    self.redirect("/login?error=empty_username")
                    return
                hashed_password = login.hash_password(password)
                login.save_user(username, hashed_password, tag="admin")
                # Initialize user folders / widget file
                user_data.startup_user(username)
                # After creation, redirect to login page (frontend shows "Login")
                self.redirect("/login")
                return

            # Otherwise, attempt to log in
            stored_hash = login.load_users().get(username, {}).get("Password")
            if stored_hash and login.verify_password(stored_hash, password):
                session_id = secrets.token_hex(16)
                EarthOSHandler.sessions[session_id] = username
                self.send_response(302)
                self.send_header("Location", "/home")
                # set cookie
                self.send_header("Set-Cookie", f"session_id={session_id}; Max-Age=57600; HttpOnly; Path=/")
                self.end_headers()
                return

            # failed login -> redirect back to login (could add ?error=bad_credentials)
            self.redirect("/login")
            return

        # --- OS API endpoints (use session_username) ---
        if os_api.handle_post(self, self.path, session_username, parsed_data):
            return

        # --- App API endpoints (use username from posted form/json) ---
        if app_api.handle_post(self, self.path, username, parsed_data):
            return

        # Default fallback
        self.redirect("/login")
