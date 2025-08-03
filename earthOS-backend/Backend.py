from http.server import HTTPServer, BaseHTTPRequestHandler
from http import cookies
import os
import secrets
import login
import urllib.parse
import mimetypes
import json
mimetypes.add_type("font/ttf", ".ttf")


class EarthOSHandler(BaseHTTPRequestHandler):
    # Handles GET requests for login, home, fonts, and redirects

    sessions = {}

    def do_GET(self):
        admin_exists = login.admin_exists()
        print("admin_exists in GET:", admin_exists)

        if  self.path == "/login":
            self.send_response(200)
            self.send_header("content-type", "text/html")
            self.end_headers()

            html_path = os.path.join(os.path.dirname(__file__), "../earthOS-frontend/earthOS-login-frontend/login.html")
            with open(html_path, "rb") as file:

                self.wfile.write(file.read())

        elif self.path == "/api/admin-exists":
            exists = login.admin_exists()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
       
            self.wfile.write(f'{{"exists": {"true" if exists else "false"}}}'.encode())
            return


        elif self.path == "/universal-style.css":
            self.send_response(200)
            self.send_header("content-type", "text/css")
            self.end_headers()
            css_path = os.path.join(os.path.dirname(__file__), "../earthOS-frontend/universal-style.css")
            with open(css_path, "rb") as file:
                content = file.read()
                self.wfile.write(content)

        elif self.path == "/login.js":
            self.send_response(200)
            self.send_header("content-type", "application/javascript")
            self.end_headers()
            js_path = os.path.join(os.path.dirname(__file__), "../earthOS-frontend/earthOS-login-frontend/login.js")
            with open(js_path, "rb") as file:
                content = file.read()
                self.wfile.write(content)

        elif self.path == "/widget.js":
            self.send_response(200)
            self.send_header("content-type", "application/javascript")
            self.end_headers()
            js_path = os.path.join(os.path.dirname(__file__), "../earthOS-frontend/earthOS-home-frontend/widget.js")
            with open(js_path, "rb") as file:
                content = file.read()
                self.wfile.write(content)

        elif self.path == "/home":
            cookie_header = self.headers.get("Cookie")
            if cookie_header:
                cookie = cookies.SimpleCookie(cookie_header)
                session_id = cookie.get("session_id")
                if session_id and session_id.value in EarthOSHandler.sessions:
                    self.send_response(200)
                    self.send_header("content-type", "text/html")
                    self.end_headers()
                    html_path = os.path.join(os.path.dirname(__file__), "../earthOS-frontend/earthOS-home-frontend/home.html")
                    with open(html_path, "r") as file:
                        content = file.read()
                        self.wfile.write(content.encode())
                    return
            self.send_response(302)
            self.send_header("Location", "/login")
            self.end_headers()
            return

        elif self.path.endswith(".ttf"):
            self.send_response(200)
            self.send_header("content-type", "font/ttf")
            self.end_headers()
            font_path = os.path.join(os.path.dirname(__file__), "../earthOS-frontend/",self.path.lstrip("/"))
            with open(font_path, "rb") as file:
                content = file.read()
                self.wfile.write(content)

        else:
            self.send_response(302)
            self.send_header("Location", "/login")
            self.end_headers()

        
    # Handles account creation (if no admin exists) and login verification
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')

        print("Received POST data:", post_data)

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

        if not login.admin_exists():
            if username.strip() == "":
                self.send_response(302)
                self.send_header("Location", "/login?error=empty_username")
                self.end_headers()
                return
            else:
                hashed_password = login.hash_password(password)
                login.save_user(username, hashed_password, tag="admin")
                print("Admin account created.")
                self.send_response(302)
                self.send_header("Location", "/login")
                self.end_headers()
        else:
            print("Admin exists..")
            users = login.load_users()
            stored_hash = users.get(username, {}).get("Password")

            if stored_hash and login.verify_password(stored_hash, password):
                session_id = secrets.token_hex(16)
                EarthOSHandler.sessions[session_id] = username

                self.send_response(302)
                self.send_header("Location", "/home")
                self.send_header("Set-Cookie", f"session_id={session_id}; Max-Age=57600; HttpOnly; Path=/")
                self.end_headers()
            else:
                self.send_response(302)
                self.send_header("Location", "/login?error=invalid_credentials")
                self.end_headers()




 # Starts the EarthOS backend server on port 8080
server = HTTPServer(('0.0.0.0',8080),EarthOSHandler)
print("backend is running")
server.serve_forever()