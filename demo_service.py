"""Fileglancer Demo Service - a simple HTTP server for testing service-type apps."""

import argparse
import os
import signal
import socket
import sys
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler


SERVICE_URL_FILENAME = "service_url"


class DemoHandler(SimpleHTTPRequestHandler):
    """Simple handler that serves a status page and optionally a directory."""

    def __init__(self, *args, serve_dir=None, message="Hello from Fileglancer!", **kwargs):
        self._serve_dir = serve_dir
        self._message = message
        self._start_time = datetime.now()
        super().__init__(*args, **kwargs)

    def translate_path(self, path):
        if self._serve_dir:
            # Serve files from the configured directory
            import posixpath
            import urllib.parse
            path = urllib.parse.unquote(posixpath.normpath(path))
            parts = path.split("/")
            # Build path relative to serve_dir
            result = self._serve_dir
            for part in parts:
                if not part or part == ".":
                    continue
                if part == "..":
                    continue
                result = os.path.join(result, part)
            return result
        return super().translate_path(path)

    def do_GET(self):
        if self.path == "/" or self.path == "":
            self._serve_status_page()
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        else:
            super().do_GET()

    def _serve_status_page(self):
        uptime = datetime.now() - self._start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Demo Service</title>
    <style>
        body {{ font-family: system-ui, sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; }}
        .status {{ padding: 12px 16px; border-radius: 8px; background: #e8f5e9; border: 1px solid #a5d6a7; margin: 16px 0; }}
        .dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #4caf50; margin-right: 8px; }}
        code {{ background: #f5f5f5; padding: 2px 6px; border-radius: 4px; font-size: 14px; }}
        h1 {{ color: #333; }}
        p {{ color: #666; line-height: 1.6; }}
    </style>
</head>
<body>
    <h1>Demo Service</h1>
    <div class="status"><span class="dot"></span> Running</div>
    <p><strong>Message:</strong> {self._message}</p>
    <p><strong>Started:</strong> {self._start_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>Uptime:</strong> {hours}h {minutes}m {seconds}s</p>
    <p><strong>Hostname:</strong> {socket.gethostname()}</p>
    <p><strong>PID:</strong> {os.getpid()}</p>
    <p>This is a demo service for testing Fileglancer's service-type app support.</p>
    <p>Endpoints:</p>
    <ul>
        <li><code>/</code> - This status page</li>
        <li><code>/health</code> - JSON health check</li>
    </ul>
</body>
</html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html.encode())

    def log_message(self, format, *args):
        # Print to stdout so it appears in job logs
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")


def find_free_port(start=8080, end=9000):
    """Find a free port in the given range."""
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No free port found in range {start}-{end}")


def write_service_url(url):
    """Write the service URL to the convention file for Fileglancer to discover."""
    # Write to the working directory (job's work_dir)
    path = os.path.join(os.getcwd(), SERVICE_URL_FILENAME)
    with open(path, "w") as f:
        f.write(url)
    print(f"Service URL written to {path}")


def main():
    parser = argparse.ArgumentParser(description="Fileglancer Demo Service")
    parser.add_argument(
        "--port", type=int, default=0,
        help="Port to listen on (0 = auto-detect free port)",
    )
    parser.add_argument(
        "--message", type=str, default="Hello from Fileglancer!",
        help="Message to display on the status page",
    )
    parser.add_argument(
        "--serve_dir", type=str, default="",
        help="Directory to serve files from (optional)",
    )
    args = parser.parse_args()

    port = args.port if args.port > 0 else find_free_port()
    hostname = socket.gethostname()

    # Build handler with custom attributes
    def handler_factory(*handler_args, **handler_kwargs):
        return DemoHandler(
            *handler_args,
            serve_dir=args.serve_dir or None,
            message=args.message,
            **handler_kwargs,
        )

    server = HTTPServer(("0.0.0.0", port), handler_factory)

    url = f"http://{hostname}:{port}"

    print("=== Fileglancer Demo Service ===")
    print(f"Message: {args.message}")
    print(f"Serve dir: {args.serve_dir or '<none>'}")
    print(f"Listening on: {url}")
    print("================================")
    print()

    # Write service_url file so Fileglancer picks it up
    write_service_url(url)

    # Handle graceful shutdown
    def shutdown_handler(signum, frame):
        print(f"\nReceived signal {signum}, shutting down...")
        server.shutdown()

    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    print(f"Service started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Press Ctrl+C or send SIGTERM to stop.")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        # Clean up service_url file
        url_path = os.path.join(os.getcwd(), SERVICE_URL_FILENAME)
        if os.path.exists(url_path):
            os.remove(url_path)
        print("Service stopped.")


if __name__ == "__main__":
    main()
