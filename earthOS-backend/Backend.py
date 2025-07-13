from http.server import HTTPServer, BaseHTTPRequestHandler

class EarthOSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"hello from EarthOS backemd")

server = HTTPServer(('0.0.0.0',8000),EarthOSHandler)
print("backend is running")
server.serve_forever()


