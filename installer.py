import os
import shutil
from tkinter import Tk, filedialog, messagebox
from pathlib import Path


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
    main()