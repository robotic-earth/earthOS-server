from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import mimetypes
mimetypes.add_type("font/ttf", ".ttf")


class EarthOSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/login":
            self.send_response(200)
            self.send_header("content-type", "text/html")
            self.end_headers()
            html_path = os.path.join(os.path.dirname(__file__), "../..//earthOS-frontend/earthOS-login-frontend/login.html")
            with open(html_path, "rb") as file:
                content = file.read()
                self.wfile.write(content)    

        elif self.path == "/login.css":
            self.send_response(200)
            self.send_header("content-type", "text/css")
            self.end_headers()
            css_path = os.path.join(os.path.dirname(__file__), "../../earthOS-frontend/earthOS-login-frontend/login.css")
            with open(css_path, "rb") as file:
                content = file.read()
                self.wfile.write(content)

        elif self.path.endswith(".ttf"):
            self.send_response(200)
            self.send_header("content-type", "font/ttf")
            self.end_headers()
            font_path = os.path.join(os.path.dirname(__file__), "../../earthOS-frontend/",self.path.lstrip("/"))
            with open(font_path, "rb") as file:
                content = file.read()
                self.wfile.write(content)

        else:
            self.send_response(302)
            self.send_header("Location", "/login")
            self.end_headers()
        
            

server = HTTPServer(('0.0.0.0',8080),EarthOSHandler)
print("backend is running")
server.serve_forever()