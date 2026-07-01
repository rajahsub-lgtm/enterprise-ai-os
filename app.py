import os
import io
import runpy
import html
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, HTTPServer


class EAIOSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        buffer = io.StringIO()

        with redirect_stdout(buffer):
            runpy.run_path("demo.py", run_name="__main__")

        output = html.escape(buffer.getvalue())

        html_page = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>EAIOS Demo</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f7f7f7;
        }}
        pre {{
            background: #111;
            color: #f5f5f5;
            padding: 24px;
            border-radius: 8px;
            overflow-x: auto;
            white-space: pre-wrap;
            font-family: Consolas, monospace;
        }}
    </style>
</head>
<body>
    <h1>Enterprise AI Operating System</h1>
    <h2>EAIOS Runtime Demo</h2>
    <pre>{output}</pre>
</body>
</html>
"""

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_page.encode("utf-8"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), EAIOSHandler)
    print(f"EAIOS web server running on port {port}")
    server.serve_forever()