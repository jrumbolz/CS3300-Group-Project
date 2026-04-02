import customtkinter as ctk
import json
import os
from pathlib import Path
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage"

def get_month_file(month, year):
    return DATA_DIR / f"{year}_{month}.json"

def load_month_data(month, year):
    file_name = get_month_file(month, year)
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return []

def create_tab(notebook):
    frame = ctk.CTkFrame(notebook)
    notebook.add(frame, text="Monthly Spending")

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    container = ctk.CTkFrame(frame)
    container.pack(expand=True, pady=20)

    # Month dropdown
    ctk.CTkLabel(container, text="Select Month:").grid(row=0, column=0, pady=5)
    month_combo = ctk.CTkComboBox(container, values=months, width=150)
    month_combo.grid(row=0, column=1, pady=5)
    month_combo.set(datetime.now().strftime("%B"))

    # Expense entry
    ctk.CTkLabel(container, text="Expense Amount:").grid(row=1, column=0, pady=5)
    amount_entry = ctk.CTkEntry(container, width=150, corner_radius=8)
    amount_entry.grid(row=1, column=1, pady=5)

    # Category (load dynamically)
    from categories_tab import load_categories
    categories = load_categories()
    ctk.CTkLabel(container, text="Category:").grid(row=2, column=0, pady=5)
    category_combo = ctk.CTkComboBox(container, values=categories, width=150)
    category_combo.grid(row=2, column=1, pady=5)
    category_combo.set("Miscellaneous")

    result_label = ctk.CTkLabel(container, text="")
    result_label.grid(row=3, column=0, columnspan=2, pady=5)

    # Listbox
    listbox = ctk.CTkTextbox(container, width=300, height=150, corner_radius=8)
    listbox.grid(row=4, column=0, columnspan=2, pady=10)

    current_data = []

    def refresh_list():
        listbox.delete("0.0", "end")
        total = 0
        for expense in current_data:
            amount = expense["amount"]
            category = expense["category"]
            time_str = expense.get("time", "")
            total += amount
            listbox.insert("end", f"${amount:.2f} - {category} ({time_str})\n")
        if current_data:
            listbox.insert("end", f"--- Total: ${total:.2f} ---\n")

    def save_expense():
        nonlocal current_data
        now = datetime.now()
        value = amount_entry.get()
        category = category_combo.get() or "Miscellaneous"
        month = month_combo.get()
        year = now.year
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            amount = float(value)
            current_data = load_month_data(month, year)
            current_data.append({
                "amount": amount,
                "category": category,
                "time": timestamp
            })
            with open(get_month_file(month, year), "w") as f:
                json.dump(current_data, f, indent=4)
            refresh_list()
            result_label.configure(text=f"Saved ${amount:.2f} ({category})")
            amount_entry.delete(0, "end")
        except ValueError:
            result_label.configure(text="Enter a valid number.")

    ctk.CTkButton(container, text="Save Expense", width=150, corner_radius=15, command=save_expense).grid(row=5, column=0, columnspan=2, pady=10)

    return frame
#Tony is on the case1