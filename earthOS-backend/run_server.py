from http.server import HTTPServer
from Backend import EarthOSHandler  # Import your handler from Backend.py

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 8080), EarthOSHandler)
    print("Server running at http://0.0.0.0:8080")
    server.serve_forever()
