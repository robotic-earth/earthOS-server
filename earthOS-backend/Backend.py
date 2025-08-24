from http.server import HTTPServer, BaseHTTPRequestHandler
from http import cookies
import os, secrets, json, base64, urllib.parse, mimetypes
import login, files, user_data

mimetypes.add_type("font/ttf", ".ttf")

class EarthOSHandler(BaseHTTPRequestHandler):
    sessions = {}  # session_id -> username mapping

    # Helpers
    def serve_file(self, content, content_type):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(content)

    def redirect(self, path):
        self.send_response(302)
        self.send_header("Location", path)
        self.end_headers()

    # --- GET ---
    def do_GET(self):
        cookie_header = self.headers.get("Cookie")
        session_username = None
        if cookie_header:
            cookie = cookies.SimpleCookie(cookie_header)
            session_id = cookie.get("session_id")
            if session_id and session_id.value in EarthOSHandler.sessions:
                session_username = EarthOSHandler.sessions[session_id.value]

        if self.path == "/login":
            self.serve_file(files.get_html("earthOS-login-frontend/login.html"), "text/html")
        elif self.path == "/home":
            if session_username:
                self.serve_file(files.get_html("earthOS-home-frontend/home.html"), "text/html")
            else:
                self.redirect("/login")
        elif self.path.endswith(".js"):
            if "login" in self.path:
                self.serve_file(files.get_js("earthOS-login-frontend/login.js"), "application/javascript")
            elif "home" in self.path:
                self.serve_file(files.get_js("earthOS-home-frontend/home.js"), "application/javascript")
            elif "widget" in self.path:
                self.serve_file(files.get_js("earthOS-home-frontend/widget.js"), "application/javascript")
        elif self.path == "/universal-style.css":
            self.serve_file(files.get_css("universal-style.css"), "text/css")
        elif self.path.endswith(".ttf"):
            self.serve_file(files.get_font(self.path.lstrip("/")), "font/ttf")
        elif self.path == "/api/admin-exists":
            exists = login.admin_exists()
            self.serve_file(json.dumps({"exists": exists}).encode(), "application/json")
        elif self.path == "/os/load-widgets":
            if session_username:
                widgets = user_data.load_widgets(session_username)
                self.serve_file(json.dumps({"widgets": widgets}).encode(), "application/json")
            else:
                self.redirect("/login")
        else:
            self.redirect("/login")

    # --- POST ---
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")

        # Parse
        if "application/json" in self.headers.get("Content-Type", ""):
            try:
                parsed_data = json.loads(post_data)
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                return
        else:
            parsed_data = urllib.parse.parse_qs(post_data)
            parsed_data = {k: v[0] for k, v in parsed_data.items()}

        username = parsed_data.get("username", "")
        password = parsed_data.get("password", "")

        # --- Admin creation ---
        if not login.admin_exists():
            if username.strip() == "":
                self.redirect("/login?error=empty_username")
                return
            hashed_password = login.hash_password(password)
            login.save_user(username, hashed_password, tag="admin")
            user_data.startup_user(username)
            self.redirect("/login")
            return

        # --- Login ---
        stored_hash = login.load_users().get(username, {}).get("Password")
        if stored_hash and login.verify_password(stored_hash, password):
            session_id = secrets.token_hex(16)
            EarthOSHandler.sessions[session_id] = username
            self.send_response(302)
            self.send_header("Location", "/home")
            self.send_header("Set-Cookie", f"session_id={session_id}; Max-Age=57600; HttpOnly; Path=/")
            self.end_headers()
            return

        # --- App API ---
        if self.path == "/api/save-file":
            try:
                filename = parsed_data.get("filename")
                subdir = parsed_data.get("subdir", "documents")
                content_b64 = parsed_data.get("content")
                if not all([username, filename, content_b64]):
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Missing fields")
                    return
                content_bytes = base64.b64decode(content_b64)
                user_data.create_user(username)
                filepath = user_data.save_file(username, filename, content_bytes, subdir="home/" + subdir)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"Saved file to {filepath}".encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error: {str(e)}".encode())
            return

        # --- OS API: widgets ---
        cookie_header = self.headers.get("Cookie")
        session_username = None
        if cookie_header:
            cookie = cookies.SimpleCookie(cookie_header)
            session_id = cookie.get("session_id")
            if session_id and session_id.value in EarthOSHandler.sessions:
                session_username = EarthOSHandler.sessions[session_id.value]

        if self.path == "/os/save-widgets" and session_username:
            widgets = parsed_data.get("widgets")
            if widgets is not None:
                user_data.save_widgets(session_username, widgets)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Widgets saved")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing widgets data")
            return

        # Default redirect
        self.redirect("/login")


# --- Start server ---
server = HTTPServer(('0.0.0.0', 8080), EarthOSHandler)
print("Backend running on port 8080")
server.serve_forever()
