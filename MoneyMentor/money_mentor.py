import subprocess
import sys
import os
from pathlib import Path

def run_dashboard():

    dir = Path(__file__).resolve().parent
    file_name = f"{dir}\FrontEnd\Dashboards\home_dashboard.py"
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir / "FrontEnd" / "Dashboards" / "home_dashboard.py"

    print(file_name)
    print(file_path)

    if not os.path.exists(file_name):
        print(f"Error: {file_name} not found.")
    if not file_path.exists():
        print(f"Error: {file_path} not found.")
        sys.exit(1)

    try:
        subprocess.run([sys.executable, file_name], check=True)
        subprocess.run([sys.executable, str(file_path)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {file_name}: {e}")
        print(f"Error running {file_path}: {e}")

if __name__ == "__main__":
    run_dashboard()