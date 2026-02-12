"""
Auto-capture dashboard screenshots using Selenium.
Run: pip install selenium  →  python take_screenshots.py
Requires Chrome browser installed.
"""

import os
import time
import subprocess
import threading
import http.server
import socketserver

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(PROJECT_DIR, "screenshots")
PORT = 8051


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PROJECT_DIR, **kwargs)
    def log_message(self, format, *args):
        pass


def start_server():
    with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
        httpd.serve_forever()


def main():
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
    except ImportError:
        print("Selenium not installed. Install it with:")
        print("  pip install selenium")
        return

    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    # Start local server in background
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(1)

    # Setup Chrome
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--force-device-scale-factor=1")

    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Chrome driver error: {e}")
        print("Make sure Chrome browser and chromedriver are installed.")
        return

    url = f"http://localhost:{PORT}/dashboard/index.html"
    print(f"Opening dashboard at {url}...")
    driver.get(url)
    time.sleep(3)  # Wait for charts to render

    # Screenshot 1 — Full dashboard top (header + filters + KPIs)
    driver.set_window_size(1440, 900)
    path1 = os.path.join(SCREENSHOTS_DIR, "01_dashboard_overview.png")
    driver.save_screenshot(path1)
    print(f"  Saved: {path1}")

    # Screenshot 2 — Scroll to charts
    driver.execute_script("window.scrollTo(0, 600);")
    time.sleep(1)
    path2 = os.path.join(SCREENSHOTS_DIR, "02_charts_section.png")
    driver.save_screenshot(path2)
    print(f"  Saved: {path2}")

    # Screenshot 3 — Scroll to insights + table
    driver.execute_script("window.scrollTo(0, 1600);")
    time.sleep(1)
    path3 = os.path.join(SCREENSHOTS_DIR, "03_insights_table.png")
    driver.save_screenshot(path3)
    print(f"  Saved: {path3}")

    # Screenshot 4 — Full page (tall window)
    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1440, total_height)
    time.sleep(2)
    path4 = os.path.join(SCREENSHOTS_DIR, "04_full_dashboard.png")
    driver.save_screenshot(path4)
    print(f"  Saved: {path4}")

    driver.quit()
    print(f"\nAll screenshots saved in: {SCREENSHOTS_DIR}")


if __name__ == "__main__":
    main()
