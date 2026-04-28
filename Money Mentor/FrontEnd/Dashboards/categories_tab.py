import customtkinter as ctk
import json
import os
from pathlib import Path


# Gets the base project directory
# parents[2] moves up two folders from this file's location
BASE_DIR = Path(__file__).resolve().parents[2]


# Creates path for storing category data
# Example:
# /Users/YourName/Desktop/MoneyMentor/BackEnd/Data Storage/
DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage"

# Creates folder if it doesn't already exist
DATA_DIR.mkdir(parents=True, exist_ok=True)


# File where categories are saved
FILE_NAME = DATA_DIR / "categories.json"


# Default category that always exists
# Prevents the app from having zero categories
DEFAULT_CATEGORY = "Miscellaneous"


# Bumped whenever categories are saved so other tabs know to refresh
CATEGORY_VERSION = 0


# -----------------------------------
# Load saved categories
# -----------------------------------
def load_categories():

    # Checks if categories file exists
    if os.path.exists(FILE_NAME):
        try:
            # Opens and reads saved JSON file
            with open(FILE_NAME, "r") as f:
                data = json.load(f)

                # Ensures JSON data is stored as a list
                if not isinstance(data, list):
                    return [DEFAULT_CATEGORY]

                # Ensures default category always exists
                if DEFAULT_CATEGORY not in data:
                    data.append(DEFAULT_CATEGORY)

                return data

        # Handles corrupted JSON files or read errors
        except (json.JSONDecodeError, IOError):
            pass

    # If file doesn't exist, return default category
    return [DEFAULT_CATEGORY]


# -----------------------------------
# Save categories to JSON file
# -----------------------------------
def save_categories(categories):
    # Uses global variable to track category version
    global CATEGORY_VERSION

    # Prevents accidental deletion of default category
    if DEFAULT_CATEGORY not in categories:
        categories.append(DEFAULT_CATEGORY)

    # Saves category list to JSON file
    with open(FILE_NAME, "w") as f:
        json.dump(categories, f, indent=4)

    # Increments category version as signal for tabs to refresh
    CATEGORY_VERSION += 1


# -----------------------------------
# Create Categories Tab UI
# -----------------------------------
def create_tab(notebook):

    # Creates tab frame
    frame = ctk.CTkFrame(notebook)

    # Adds tab to notebook navigation
    notebook.add(frame, text="Categories")


    # Loads saved categories
    categories = load_categories()


    # Main container frame
    container = ctk.CTkFrame(frame)
    container.pack(expand=True, fill=None, pady=40)


    # Frame for category input controls
    input_frame = ctk.CTkFrame(container)
    input_frame.pack(padx=20, pady=20)


    # -----------------------------
    # Add category section
    # -----------------------------
    ctk.CTkLabel(
        input_frame,
        text="Add a new category:"
    ).grid(row=0, column=0, columnspan=2, pady=5)


    # Input box for new category name
    cat_entry = ctk.CTkEntry(
        input_frame,
        width=150,
        corner_radius=8
    )
    cat_entry.grid(row=1, column=0, columnspan=2, pady=5)


    # -----------------------------
    # Category selection dropdown
    # -----------------------------
    ctk.CTkLabel(
        input_frame,
        text="Select a category to delete:"
    ).grid(row=2, column=0, columnspan=2, pady=5)


    # Dropdown containing all saved categories
    cat_combobox = ctk.CTkComboBox(
        input_frame,
        values=categories,
        width=200
    )
    cat_combobox.grid(row=3, column=0, columnspan=2, pady=5)


    # Sets default selected category
    if categories:
        cat_combobox.set(categories[0])


    # -----------------------------------
    # Refresh dropdown after updates
    # -----------------------------------
    def refresh():
        cat_combobox.configure(values=categories)

        if categories:
            cat_combobox.set(categories[0])
        else:
            cat_combobox.set("")


    # -----------------------------------
    # Add new category function
    # -----------------------------------
    def add_category():

        # Removes extra spaces
        new_cat = cat_entry.get().strip()

        # Prevent duplicates and blank categories
        if new_cat and new_cat not in categories:
            categories.append(new_cat)

            save_categories(categories)
            refresh()

            # Clears input box
            cat_entry.delete(0, "end")


    # -----------------------------------
    # Delete selected category function
    # -----------------------------------
    def delete_category():
        selected = cat_combobox.get()

        # Prevent deleting default category
        if selected and selected != DEFAULT_CATEGORY:
            categories.remove(selected)

            save_categories(categories)
            refresh()


    # Button to add category
    ctk.CTkButton(
        input_frame,
        text="Add Category",
        width=150,
        corner_radius=15,
        command=add_category
    ).grid(row=4, column=0, pady=10)


    # Button to delete selected category
    ctk.CTkButton(
        input_frame,
        text="Delete Selected",
        width=150,
        corner_radius=15,
        command=delete_category
    ).grid(row=4, column=1, pady=10)

    
    return frame


# Tony remains on the case