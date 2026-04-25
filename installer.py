import os
import shutil
from tkinter import Tk, filedialog, messagebox
from pathlib import Path

#!!!!!!!!!!!!!!!!! doesn't work with installing dependencies first
# Folder you want to install
app_dir = Path(__file__).resolve().parent
SOURCE_FOLDER = f"{app_dir}\Money Mentor"

def main():
    # Hide the root tkinter window
    root = Tk()
    root.withdraw()

    messagebox.showinfo("Installer", "Select where you want to install the folder.")

    # Open folder picker dialog
    install_dir = filedialog.askdirectory(title="Select Install Directory")

    if not install_dir:
        messagebox.showwarning("Cancelled", "No folder selected. Installation cancelled.")
        return

    # Check source folder exists
    if not os.path.isdir(SOURCE_FOLDER):
        messagebox.showerror("Error", "Source folder not found!")
        return

    dest_path = os.path.join(install_dir, os.path.basename(SOURCE_FOLDER))

    # Handle existing folder
    if os.path.exists(dest_path):
        overwrite = messagebox.askyesno(
            "Overwrite?",
            "Folder already exists. Do you want to overwrite it?"
        )
        if not overwrite:
            messagebox.showinfo("Cancelled", "Installation cancelled.")
            return
        shutil.rmtree(dest_path)

    # Copy folder
    try:
        shutil.copytree(SOURCE_FOLDER, dest_path)
        messagebox.showinfo("Success", f"Installed to:\n{dest_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    main()import shutil
from tkinter import Tk, filedialog, messagebox
from pathlib import Path


# Gets the folder location where this installer script is stored
# Example:
# If installer.py is inside:
# C:/Users/Name/Desktop/AppInstaller
# app_dir becomes:
# C:/Users/Name/Desktop/AppInstaller
app_dir = Path(__file__).resolve().parent


# Points to the "Money Mentor" folder that will be copied during installation
# This assumes the folder exists in the same directory as the installer script
SOURCE_FOLDER = app_dir / "Money Mentor"


def main():
    # Creates hidden tkinter root window
    # Needed for file dialogs/message boxes to work
    root = Tk()
    root.withdraw()

    # Tells user to choose where they want the program installed
    messagebox.showinfo(
        "Installer",
        "Select where you want to install Money Mentor."
    )

    # Opens folder browser so user can pick install location
    install_dir = filedialog.askdirectory(
        title="Select Install Directory"
    )

    # If user closes window or doesn't pick a folder
    if not install_dir:
        messagebox.showwarning(
            "Cancelled",
            "No folder selected. Installation cancelled."
        )
        return

    # Makes sure the source folder actually exists
    if not SOURCE_FOLDER.is_dir():
        messagebox.showerror(
            "Error",
            f"Source folder not found:\n{SOURCE_FOLDER}"
        )
        return

    # Converts selected path into Path object
    install_dir = Path(install_dir)

    # Creates final install destination path
    # Example:
    # User selects C:/Program Files
    # Final path becomes:
    # C:/Program Files/Money Mentor
    dest_path = install_dir / SOURCE_FOLDER.name

    # Checks if app already exists in selected location
    if dest_path.exists():

        # Ask user if they want to replace old installation
        overwrite = messagebox.askyesno(
            "Overwrite?",
            "Money Mentor is already installed there. Do you want to overwrite it?"
        )

        # Cancel installation if user says no
        if not overwrite:
            messagebox.showinfo(
                "Cancelled",
                "Installation cancelled."
            )
            return

        # Deletes old folder before installing new one
        shutil.rmtree(dest_path)

    try:
        # Copies entire Money Mentor folder into selected location
        shutil.copytree(SOURCE_FOLDER, dest_path)

        # Shows success message after installation completes
        messagebox.showinfo(
            "Success",
            f"Installed to:\n{dest_path}"
        )

    except Exception as e:
        # Handles unexpected installation errors
        messagebox.showerror(
            "Error",
            str(e)
        )


# Runs installer only when script is directly executed
if __name__ == "__main__":
    main()