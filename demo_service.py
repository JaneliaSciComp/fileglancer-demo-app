"""Fileglancer Demo Service - a simple HTTP server for testing service-type apps.

Convention: Fileglancer sets SERVICE_URL_PATH to the absolute path where the
service should write its URL. Fileglancer reads this file on each poll to
display the service URL in the UI.
"""

import argparse
import os
import signal
import socket
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler


def log(msg):
    """Print a timestamped log message and flush immediately (important for LSF)."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)


class DemoHandler(SimpleHTTPRequestHandler):
    """Simple handler that serves a status page."""

    def __init__(self, *args, message="Hello from Fileglancer!", **kwargs):
        self._message = message
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == "/" or self.path == "":
            self._serve_status_page()
        else:
            self.send_error(404)

    def _serve_status_page(self):
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
    <p><strong>Hostname:</strong> {socket.gethostname()}</p>
    <p><strong>PID:</strong> {os.getpid()}</p>
    <p>This is a demo service for testing Fileglancer's service-type app support.</p>
</body>
</html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html.encode())

    def log_message(self, format, *args):
        log(format % args)


def find_free_port(start=8080, end=9000):
    """Find a free port in the given range."""
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                log(f"Found free port: {port}")
                return port
            except OSError:
                continue
    raise RuntimeError(f"No free port found in range {start}-{end}")


def write_service_url(url, path):
    """Write the service URL to the path specified by SERVICE_URL_PATH."""
    log(f"Writing service URL to: {path}")
    with open(path, "w") as f:
        f.write(url)
    if os.path.exists(path):
        log(f"Verified: {path} exists ({os.path.getsize(path)} bytes)")
    else:
        log(f"ERROR: {path} does not exist after write!")


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
    args = parser.parse_args()

    log("=== Fileglancer Demo Service ===")
    log(f"PID: {os.getpid()}")
    log(f"CWD: {os.getcwd()}")
    log(f"Message: {args.message}")
    log(f"Port arg: {args.port}")

    service_url_path = os.environ.get("SERVICE_URL_PATH", "")
    if service_url_path:
        log(f"SERVICE_URL_PATH: {service_url_path}")
    else:
        log("WARNING: SERVICE_URL_PATH not set, service URL will not be written")

    port = args.port if args.port > 0 else find_free_port()
    hostname = socket.gethostname()
    log(f"Hostname: {hostname}")

    # Build handler with custom attributes
    def handler_factory(*handler_args, **handler_kwargs):
        return DemoHandler(
            *handler_args,
            message=args.message,
            **handler_kwargs,
        )

    log(f"Binding to 0.0.0.0:{port}...")
    server = HTTPServer(("0.0.0.0", port), handler_factory)
    url = f"http://{hostname}:{port}"
    log(f"Server bound successfully: {url}")

    # Write service_url file so Fileglancer picks it up
    if service_url_path:
        write_service_url(url, service_url_path)

    # Handle graceful shutdown
    def shutdown_handler(signum, frame):
        log(f"Received signal {signum}, shutting down...")
        server.shutdown()

    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    log("Service ready, entering serve_forever loop")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        # Clean up service_url file
        if service_url_path and os.path.exists(service_url_path):
            os.remove(service_url_path)
            log(f"Cleaned up {service_url_path}")
        log("Service stopped.")


if __name__ == "__main__":
    main()
