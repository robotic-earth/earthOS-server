import base64
import user_data

def handle_post(handler, path, username, parsed_data):
    if path == "/api/save-file":
        try:
            filename = parsed_data.get("filename")
            subdir = parsed_data.get("subdir", "documents")
            content_b64 = parsed_data.get("content")
            if not all([username, filename, content_b64]):
                handler.send_response(400)
                handler.end_headers()
                handler.wfile.write(b"Missing fields")
                return True
            content_bytes = base64.b64decode(content_b64)
            user_data.create_user(username)
            filepath = user_data.save_file(username, filename, content_bytes, subdir="home/" + subdir)
            handler.send_response(200)
            handler.end_headers()
            handler.wfile.write(f"Saved file to {filepath}".encode())
        except Exception as e:
            handler.send_response(500)
            handler.end_headers()
            handler.wfile.write(f"Error: {str(e)}".encode())
        return True
    return False
