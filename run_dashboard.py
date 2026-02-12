"""
Simple HTTP server to launch the Mutual Fund Dashboard.
Run: python run_dashboard.py
"""
import http.server
import socketserver
import webbrowser
import os
import threading

PORT = 8050
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        pass  # Suppress logs


def main():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/dashboard/index.html"
        print(f"\n  Mutual Fund Insights Dashboard")
        print(f"  {'=' * 40}")
        print(f"  Server running at: {url}")
        print(f"  Press Ctrl+C to stop\n")

        # Open browser after a short delay
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Server stopped.")
            httpd.shutdown()


if __name__ == "__main__":
    main()
