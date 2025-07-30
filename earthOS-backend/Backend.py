from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import login
import urllib.parse
import mimetypes
mimetypes.add_type("font/ttf", ".ttf")


class EarthOSHandler(BaseHTTPRequestHandler):
    # Handles GET requests for login, home, fonts, and redirects
    def do_GET(self):
        admin_exists = login.admin_exists()
        print("admin_exists in GET:", admin_exists)

        if  self.path == "/login":
            self.send_response(200)
            self.send_header("content-type", "text/html")
            self.end_headers()

            html_path = os.path.join(os.path.dirname(__file__), "../earthOS-frontend/earthOS-login-frontend/login.html")
            with open(html_path, "r") as file:
                content = file.read()
                script = f"<script>var adminExist = {str(admin_exists).lower()};</script>\n"
                content = content.replace("<head>", "<head>" + script )
                self.wfile.write(content.encode())    

        elif self.path == "/login.css":
            self.send_response(200)
            self.send_header("content-type", "text/css")
            self.end_headers()
            css_path = os.path.join(os.path.dirname(__file__), "../earthOS-frontend/earthOS-login-frontend/login.css")
            with open(css_path, "rb") as file:
                content = file.read()
                self.wfile.write(content)

        elif self.path == "/home":
            self.send_response(200)
            self.send_header("content-type", "text/html")
            self.end_headers()
            html_path = os.path.join(os.path.dirname(__file__), "../earthOS-frontend/earthOS-home-frontend/home.html")
            with open(html_path, "r") as file:
                content = file.read()
                self.wfile.write(content.encode())

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
                self.send_response(302)
                self.send_header("Location", "/home")
                self.end_headers()
            else:
                self.send_response(302)
                self.send_header("Location", "/login?error=invalid_credentials")
                self.end_headers()


 # Starts the EarthOS backend server on port 8080
server = HTTPServer(('0.0.0.0',8080),EarthOSHandler)
print("backend is running")
server.serve_forever()