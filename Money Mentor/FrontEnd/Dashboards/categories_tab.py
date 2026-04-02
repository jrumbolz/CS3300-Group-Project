import customtkinter as ctk
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FILE_NAME = DATA_DIR / "categories.json"
DEFAULT_CATEGORY = "Miscellaneous"

# ---------- Load ----------
def load_categories():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    return [DEFAULT_CATEGORY]
                if DEFAULT_CATEGORY not in data:
                    data.append(DEFAULT_CATEGORY)
                return data
        except (json.JSONDecodeError, IOError):
            pass
    return [DEFAULT_CATEGORY]

# ---------- Save ----------
def save_categories(categories):
    if DEFAULT_CATEGORY not in categories:
        categories.append(DEFAULT_CATEGORY)
    with open(FILE_NAME, "w") as f:
        json.dump(categories, f, indent=4)

# ---------- UI ----------
def create_tab(notebook):
    frame = ctk.CTkFrame(notebook)
    notebook.add(frame, text="Categories")

    categories = load_categories()

    container = ctk.CTkFrame(frame)
    container.pack(expand=True, fill=None, pady=40)

    input_frame = ctk.CTkFrame(container)
    input_frame.pack(padx=20, pady=20)

    # --- Add category ---
    ctk.CTkLabel(input_frame, text="Add a new category:").grid(row=0, column=0, columnspan=2, pady=5)
    cat_entry = ctk.CTkEntry(input_frame, width=150, corner_radius=8)
    cat_entry.grid(row=1, column=0, columnspan=2, pady=5)

    # --- Display categories in a ComboBox ---
    ctk.CTkLabel(input_frame, text="Select a category to delete:").grid(row=2, column=0, columnspan=2, pady=5)
    cat_combobox = ctk.CTkComboBox(input_frame, values=categories, width=200)
    cat_combobox.grid(row=3, column=0, columnspan=2, pady=5)
    if categories:
        cat_combobox.set(categories[0])

    def refresh():
        cat_combobox.configure(values=categories)
        if categories:
            cat_combobox.set(categories[0])
        else:
            cat_combobox.set("")

    # --- Add category ---
    def add_category():
        new_cat = cat_entry.get().strip()
        if new_cat and new_cat not in categories:
            categories.append(new_cat)
            save_categories(categories)
            refresh()
            cat_entry.delete(0, "end")

    # --- Delete selected category ---
    def delete_category():
        selected = cat_combobox.get()
        if selected and selected != DEFAULT_CATEGORY:
            categories.remove(selected)
            save_categories(categories)
            refresh()

    ctk.CTkButton(input_frame, text="Add Category", width=150, corner_radius=15, command=add_category).grid(row=4, column=0, pady=10)
    ctk.CTkButton(input_frame, text="Delete Selected", width=150, corner_radius=15, command=delete_category).grid(row=4, column=1, pady=10)

    return frame
#Tony is on the case1