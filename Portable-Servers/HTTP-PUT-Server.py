#!/usr/bin/env python3

import os
import io
import argparse
from http.server import SimpleHTTPRequestHandler, HTTPServer


class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Extend SimpleHTTPRequestHandler with support for PUT requests and custom directory listing."""
    
    def do_PUT(self):
        """Save a file following an HTTP PUT request."""
        filename = os.path.basename(self.path)
        file_length = int(self.headers['Content-Length'])
        with open(filename, 'wb') as output_file:
            output_file.write(self.rfile.read(file_length))
        self.send_response(201, 'Created')
        self.end_headers()
        reply_body = f'Saved "{filename}"\n'
        self.wfile.write(reply_body.encode('utf-8'))
    
    def list_directory(self, path):
        """Generate a directory listing with custom CSS and drag-and-drop upload functionality."""
        try:
            list_items = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None
        
        list_items.sort(key=lambda a: a.lower())
        displaypath = os.path.relpath(path, os.getcwd())
        title = "HTTP PUT Server"

        # Generate the HTML for the directory listing
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f9f9f9;
            color: #333;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }}
        h1 {{
            font-size: 1.8em;
            color: #2d2121;
            margin-bottom: 20px;
            text-align: center;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            background-color: #ffffff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{
            padding: 12px 15px;
            border-bottom: 1px solid #f1f1f1;
            text-align: left;
        }}
        th {{
            background-color: #ff0000;
            color: #fff;
            font-weight: 600;
            text-transform: uppercase;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        a {{
            text-decoration: none;
            color: #1648dd;
            font-weight: 500;
        }}
        .upload-area {{
            border: 2px dashed #ff6666;
            border-radius: 8px;
            padding: 30px;
            text-align: center;
            margin: 30px 0;
            background-color: #f8f9fa;
            color: #555;
            transition: background-color 0.3s, border-color 0.3s;
            cursor: pointer;
        }}
        .upload-area.dragover {{
            background-color: #ffcccc;
            border-color: #660000;
        }}
        footer {{
            text-align: center;
            margin-top: 20px;
            color: #888;
            font-size: 0.85em;
        }}
        footer a {{
            color: #b30000;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>

    <div class="upload-area" id="upload-area">
        Drag & Drop files here
    </div>

    <table>
        <tr><th>Name</th><th>Type</th><th>Action</th></tr>"""

        for name in list_items:
            fullname = os.path.join(path, name)
            displayname = name + "/" if os.path.isdir(fullname) else name
            linkname = os.path.join(self.path, name)
            linkname = linkname.replace("//", "/")  # Normalize slashes
            filetype = "Directory" if os.path.isdir(fullname) else "File"
            download_button = f'<a href="{linkname}" download class="download-button">Download</a>' if not os.path.isdir(fullname) else ""
            html += f"""<tr>
                <td><a href="{linkname}">{displayname}</a></td>
                <td>{filetype}</td>
                <td>{download_button}</td>
            </tr>"""
        
        html += """</table>

    <script>
        const uploadArea = document.getElementById('upload-area');

        // Handle drag-and-drop
        uploadArea.addEventListener('dragover', (event) => {
            event.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (event) => {
            event.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = event.dataTransfer.files;
            uploadFiles(files);
        });

        uploadArea.addEventListener('click', () => {
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.multiple = true;
            fileInput.addEventListener('change', (event) => {
                const files = event.target.files;
                uploadFiles(files);
            });
            fileInput.click();
        });

        // Upload files
        function uploadFiles(files) {
            for (const file of files) {
                const xhr = new XMLHttpRequest();
                xhr.open('PUT', file.name, true);
                xhr.onload = () => {
                    if (xhr.status === 201) {
                        alert(`Uploaded: ${file.name}`);
                        location.reload();
                    } else {
                        alert(`Failed to upload: ${file.name}`);
                    }
                };
                xhr.send(file);
            }
        }
    </script>
</body>
</html>"""
        
        encoded = html.encode('utf-8')
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return io.BytesIO(encoded)


def run():
    parser = argparse.ArgumentParser(description="Simple HTTP Server with custom directory listing and drag-and-drop uploads.")
    parser.add_argument('-p', '--port', type=int, default=80, help='Port to serve HTTP on (default: 80)')
    parser.add_argument('-d', '--directory', type=str, default=os.getcwd(), help='Directory to serve (default: current directory)')
    args = parser.parse_args()

    os.chdir(args.directory)
    s_port = ('', args.port)
    serve = HTTPServer(s_port, CustomHTTPRequestHandler)

    try:
        print(f"Serving HTTP on 0.0.0.0 port {args.port} (Directory: {args.directory})")
        serve.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped")


if __name__ == '__main__':
    run()
