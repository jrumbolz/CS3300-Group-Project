import tkinter as tk
from tkinter import ttk
import json
import os
from pathlib import Path

# ====== FILE PATH SETUP ======
# Go up to project root (Money Mentor)
BASE_DIR = Path(__file__).resolve().parents[2]

# Navigate to BackEnd/Data Storage
DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage"

# Ensure the folder exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Final file path
CATEGORIES_FILE = DATA_DIR / "categories.json"


def load_categories():
    if not os.path.exists(CATEGORIES_FILE):
        default = ["Miscellaneous", "Food", "Transport", "Bills", "Entertainment"]
        with open(CATEGORIES_FILE, "w") as f:
            json.dump(default, f, indent=4)
        return default

    with open(CATEGORIES_FILE, "r") as f:
        return json.load(f)


def get_month_file(month):
    return f"{month}.json"


def load_month_data(month):
    file_name = get_month_file(month)
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return []


def save_month_data(month, data):
    file_name = get_month_file(month)
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)


def create_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Monthly Spending")

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    categories = load_categories()
    current_data = []

    # Month selection
    ttk.Label(frame, text="Select Month:").pack(pady=5)
    month_combo = ttk.Combobox(frame, values=months, state="readonly")
    month_combo.pack(pady=5)

    # Expense input
    ttk.Label(frame, text="Expense Amount:").pack(pady=5)
    amount_entry = ttk.Entry(frame)
    amount_entry.pack(pady=5)

    # Category selection
    ttk.Label(frame, text="Category:").pack(pady=5)
    category_combo = ttk.Combobox(frame, values=categories, state="readonly")
    category_combo.pack(pady=5)
    category_combo.set("Miscellaneous")

    result = ttk.Label(frame, text="")
    result.pack(pady=5)

    # Listbox
    listbox = tk.Listbox(frame, height=10)
    listbox.pack(pady=5, fill=tk.BOTH, expand=True)

    def refresh_list():
        listbox.delete(0, tk.END)
        total = 0
        for expense in current_data:
            amount = expense["amount"]
            category = expense["category"]
            total += amount
            listbox.insert(tk.END, f"${amount:.2f} - {category}")
        if current_data:
            listbox.insert(tk.END, f"--- Total: ${total:.2f} ---")

    def on_month_change(event):
        nonlocal current_data
        month = month_combo.get()
        current_data = load_month_data(month)
        refresh_list()

    def save_expense():
        month = month_combo.get()
        value = amount_entry.get()
        category = category_combo.get() or "Miscellaneous"

        if not month:
            result.config(text="Please select a month.")
            return

        try:
            amount = float(value)

            current_data.append({
                "amount": amount,
                "category": category
            })

            save_month_data(month, current_data)
            refresh_list()
            result.config(text=f"Saved ${amount:.2f} ({category})")
            amount_entry.delete(0, tk.END)

        except ValueError:
            result.config(text="Enter a valid number.")

    month_combo.bind("<<ComboboxSelected>>", on_month_change)

    ttk.Button(frame, text="Save Expense", command=save_expense).pack(pady=10)

    return frame