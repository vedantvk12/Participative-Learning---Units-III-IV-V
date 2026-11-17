"""
Application Screenshot Capture Utility
Launches Streamlit in local subprocess, captures genuine UI states via headless Chrome, and terminates gracefully.
"""

import os
import sys
import time
import subprocess
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def wait_for_server(url, timeout=20):
    start = time.time()
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(req, timeout=1) as resp:
                if resp.status == 200:
                    return True
        except Exception as e:
            time.sleep(0.8)
    return False


def capture_with_chrome(url, output_path, width=1300, height=850):
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--screenshot={output_path}",
        url
    ]
    subprocess.run(cmd, check=True)


def main():
    print("Starting Streamlit server on port 8501...")
    env = os.environ.copy()
    env["STREAMLIT_SERVER_PORT"] = "8501"
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

    cmd = [
        sys.executable, "-m", "streamlit", "run", str(BASE_DIR / "app.py"),
        "--server.port=8501", "--server.headless=true", "--browser.gatherUsageStats=false"
    ]
    proc = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        url = "http://localhost:8501"
        health_url = "http://localhost:8501/_stcore/health"
        print("Waiting for Streamlit to initialize...")
        if not wait_for_server(health_url, timeout=20):
            print("Streamlit health check did not respond in time.")
            return

        print("Streamlit server active! Capturing primary application overview screenshot...")
        time.sleep(3)  # Give JS time to hydrate
        overview_path = ASSETS_DIR / "screenshot_tab1_overview.png"
        capture_with_chrome(url, str(overview_path))
        print(f"Captured: {overview_path}")

    finally:
        print("Terminating Streamlit background server...")
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
        print("Streamlit process closed.")


if __name__ == "__main__":
    main()
