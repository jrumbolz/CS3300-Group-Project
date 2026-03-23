import tkinter as tk
from tkinter import ttk
import json
import os

FILE_NAME = "categories.json"
DEFAULT_CATEGORY = "Miscellaneous"


# ---------- Load ----------
def load_categories():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                data = json.load(f)

                # Ensure it's a list
                if not isinstance(data, list):
                    return [DEFAULT_CATEGORY]

                # Always include default
                if DEFAULT_CATEGORY not in data:
                    data.append(DEFAULT_CATEGORY)

                return data

        except (json.JSONDecodeError, IOError):
            pass

    return [DEFAULT_CATEGORY]


# ---------- Save ----------
def save_categories(categories):
    # Ensure default category always exists
    if DEFAULT_CATEGORY not in categories:
        categories.append(DEFAULT_CATEGORY)

    with open(FILE_NAME, "w") as f:
        json.dump(categories, f, indent=4)


# ---------- UI ----------
def create_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Categories")

    categories = load_categories()

    tk.Label(frame, text="Add a new category:").pack(pady=5)

    cat_entry = tk.Entry(frame)
    cat_entry.pack(pady=5)

    cat_listbox = tk.Listbox(frame)
    cat_listbox.pack(pady=10, fill="both", expand=True)

    # Refresh list display
    def refresh():
        cat_listbox.delete(0, tk.END)
        for cat in categories:
            cat_listbox.insert(tk.END, cat)

    refresh()

    # Add category
    def add_category():
        new_cat = cat_entry.get().strip()

        if new_cat and new_cat not in categories:
            categories.append(new_cat)
            refresh()
            save_categories(categories)  # auto-save
            cat_entry.delete(0, tk.END)

    # Delete category
    def delete_category():
        selected = cat_listbox.curselection()
        if not selected:
            return

        index = selected[0]
        value = cat_listbox.get(index)

        if value == DEFAULT_CATEGORY:
            return  # cannot delete

        categories.remove(value)
        refresh()
        save_categories(categories)  # auto-save

    # Buttons
    tk.Button(frame, text="Add Category", command=add_category).pack(pady=5)
    tk.Button(frame, text="Delete Selected", command=delete_category).pack(pady=5)

    return frame