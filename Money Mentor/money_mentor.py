import subprocess
import sys
import os
from pathlib import Path


def run_dashboard():

    # Gets the folder location where this current Python file is stored
    # Example:
    # If this script is in:
    # C:/Users/YourName/Desktop/MoneyMentor
    # base_dir becomes that folder path
    base_dir = Path(__file__).resolve().parent


    # Creates the full path to home_dashboard.py
    # This assumes your project folder structure looks like:
    #
    # MoneyMentor/
    # ├── launcher.py
    # └── FrontEnd/
    #     └── Dashboards/
    #         └── home_dashboard.py
    #
    file_path = base_dir / "FrontEnd" / "Dashboards" / "home_dashboard.py"


    # Prints the dashboard file path
    # Useful for debugging and verifying the correct file path
    print(file_path)


    # Checks if home_dashboard.py actually exists
    # Prevents the program from crashing if the file is missing
    if not file_path.exists():
        print(f"Error: {file_path} not found.")
        sys.exit(1)


    try:
        # Runs home_dashboard.py as a separate Python process
        #
        # sys.executable ensures it uses the same Python interpreter
        # currently running this script
        #
        # check=True means Python will raise an error if
        # home_dashboard.py fails to run properly
        subprocess.run(
            [sys.executable, str(file_path)],
            check=True
        )


    except subprocess.CalledProcessError as e:
        # Handles errors if home_dashboard.py crashes
        print(f"Error running {file_path}: {e}")


# Makes sure the dashboard only launches when this file
# is run directly (not imported into another Python file)
if __name__ == "__main__":
    run_dashboard()