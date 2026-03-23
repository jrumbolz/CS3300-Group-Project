import subprocess
import sys
import os
from pathlib import Path

def run_dashboard():

    dir = Path(__file__).resolve().parent
    file_name = f"{dir}\FrontEnd\Dashboards\Home\home_dashboard.py"

    print(file_name)

    if not os.path.exists(file_name):
        print(f"Error: {file_name} not found.")
        sys.exit(1)

    try:
        subprocess.run([sys.executable, file_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {file_name}: {e}")

if __name__ == "__main__":
    run_dashboard()