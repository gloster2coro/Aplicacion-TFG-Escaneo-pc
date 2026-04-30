"""
Optidriver Launcher - standalone entry point.
Starts FastAPI backend and opens browser to the bundled frontend.
Designed to be packaged as .exe with PyInstaller.
"""
import os
import sys
import threading
import time
import webbrowser
import subprocess
from pathlib import Path

HERE = Path(__file__).parent.resolve()
BACKEND_DIR = HERE / "backend"
FRONTEND_BUILD = HERE / "frontend" / "build"
PORT = 8001
FRONTEND_PORT = 3000


def start_backend():
    """Start FastAPI via uvicorn in the current process."""
    sys.path.insert(0, str(BACKEND_DIR))
    os.chdir(BACKEND_DIR)
    import uvicorn
    uvicorn.run(
        "server:app",
        host="127.0.0.1",
        port=PORT,
        log_level="info",
        reload=False,
    )


def serve_frontend():
    """Serve the static frontend build on FRONTEND_PORT."""
    if not FRONTEND_BUILD.exists():
        print(f"[!] Frontend build not found at {FRONTEND_BUILD}")
        print("    Run: cd frontend && yarn build")
        return
    import http.server
    import socketserver
    os.chdir(FRONTEND_BUILD)

    class SPAHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            # SPA fallback - serve index.html for non-asset paths
            target = (FRONTEND_BUILD / self.path.lstrip("/")).resolve()
            if not target.exists() and not self.path.startswith("/static"):
                self.path = "/index.html"
            return super().do_GET()

    with socketserver.TCPServer(("127.0.0.1", FRONTEND_PORT), SPAHandler) as httpd:
        print(f"[OK] Frontend served on http://127.0.0.1:{FRONTEND_PORT}")
        httpd.serve_forever()


def open_browser_when_ready():
    """Wait for backend to be ready then open browser."""
    import urllib.request
    for _ in range(60):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORT}/api/", timeout=1)
            break
        except Exception:
            time.sleep(0.5)
    webbrowser.open(f"http://127.0.0.1:{FRONTEND_PORT}")


def main():
    print("=" * 50)
    print("   OPTIDRIVER v1.0 - Starting...")
    print("=" * 50)

    # Start frontend server in thread
    threading.Thread(target=serve_frontend, daemon=True).start()
    # Open browser in thread
    threading.Thread(target=open_browser_when_ready, daemon=True).start()
    # Run backend in main thread (blocks)
    start_backend()


if __name__ == "__main__":
    main()
