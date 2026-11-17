"""
Streamlit Launcher Script
Multi-Agent Enterprise AI Service Desk
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

if __name__ == "__main__":
    print("Launching Multi-Agent Enterprise AI Service Desk Streamlit App...")
    cmd = [sys.executable, "-m", "streamlit", "run", str(BASE_DIR / "app.py")]
    subprocess.run(cmd)

