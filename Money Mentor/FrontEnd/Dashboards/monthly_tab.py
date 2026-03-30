import tkinter as tk
from tkinter import ttk
import json
import os
from pathlib import Path
from datetime import datetime


# ====== FILE PATH SETUP ======
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CATEGORIES_FILE = DATA_DIR / "categories.json"




def load_categories():
    if not os.path.exists(CATEGORIES_FILE):
        default = ["Miscellaneous", "Food", "Transport", "Bills", "Entertainment"]
        with open(CATEGORIES_FILE, "w") as f:
            json.dump(default, f, indent=4)
        return default
    with open(CATEGORIES_FILE, "r") as f:
        return json.load(f)




def get_month_file(month, year):
    return DATA_DIR / f"{year}_{month}.json"




def load_month_data(month, year):
    file_name = get_month_file(month, year)
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return []




def save_month_data(month, year, data):
    file_name = get_month_file(month, year)
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

    current_year = datetime.now().year
    years = [str(y) for y in range(current_year - 10, current_year)]

    categories = load_categories()
    current_data = []


    # ===== Live current date/time display =====
    time_label = ttk.Label(frame, text="", font=("Arial", 10))
    time_label.pack(pady=5)


    def update_time():
        now = datetime.now()
        formatted = now.strftime("%B %d, %Y | %I:%M:%S %p")
        time_label.config(text=formatted)
        frame.after(1000, update_time)


    update_time()


    # ===== Container frame for inputs, listbox, and save button =====
    container = ttk.Frame(frame)
    container.pack(expand=True, fill='both', pady=5)


    # ===== Input frame centered =====
    input_frame = ttk.Frame(container)
    input_frame.pack(pady=5)

    # Year dropdown
    tk.Label(input_frame, text="Select Year:").pack(pady=2)
    year_combo = ttk.Combobox(input_frame, values=years, state="readonly")
    year_combo.pack(pady=2)
    year_combo.set(str(current_year))

    # Month dropdown
    tk.Label(input_frame, text="Select Month:").pack(pady=2)
    month_combo = ttk.Combobox(input_frame, values=months, state="readonly")
    month_combo.pack(pady=2)
    current_month = datetime.now().strftime("%B")
    month_combo.set(current_month)

    # Expense or Income Drop Down
    tk.Label(input_frame, text="Type:").pack(pady=2)
    type_combo = ttk.Combobox(input_frame, values=["Expense", "Income"], state="readonly")
    type_combo.pack(pady=2)
    type_combo.set("Expense")

    # Category dropdown
    tk.Label(input_frame, text="Category:").pack(pady=2)
    category_combo = ttk.Combobox(input_frame, values=categories, state="readonly")
    category_combo.pack(pady=2)
    category_combo.set("Miscellaneous")

    # ===== NEW: Refresh categories dynamically =====
    def refresh_categories(event=None):
        current = category_combo.get()
        new_categories = load_categories()
        category_combo["values"] = new_categories

        if current in new_categories:
            category_combo.set(current)
        else:
            category_combo.set(new_categories[0] if new_categories else "")

    category_combo.bind("<Button-1>", refresh_categories)

    # Expense amount
    tk.Label(input_frame, text="Expense Amount:").pack(pady=2)
    amount_entry = ttk.Entry(input_frame)
    amount_entry.pack(pady=2)


    # Result label
    result = tk.Label(input_frame, text="")
    result.pack(pady=2)


    # ===== Listbox =====
    listbox_frame = ttk.Frame(container)
    listbox_frame.pack(fill='both', expand=True, pady=5)
    listbox = tk.Listbox(listbox_frame)
    listbox.pack(fill='both', expand=True)


    def refresh_list():
        listbox.delete(0, tk.END)
        total = 0
        for expense in current_data:
            amount = expense["amount"]
            category = expense["category"]
            time_str = expense.get("time", "")
            total += amount
            listbox.insert(tk.END, f"${amount:.2f} - {category} ({time_str})")
        if current_data:
            listbox.insert(tk.END, f"--- Total: ${total:.2f} ---")


    def on_month_change(event):
        nonlocal current_data
        month = month_combo.get()
        year = datetime.now().year
        current_data = load_month_data(month, year)
        refresh_list()


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
            save_month_data(month, year, current_data)
            refresh_list()
            result.config(text=f"Saved ${amount:.2f} ({category})")
            amount_entry.delete(0, tk.END)
        except ValueError:
            result.config(text="Enter a valid number.")


    month_combo.bind("<<ComboboxSelected>>", on_month_change)


    # ===== Save Button (always visible below listbox) =====
    save_button = ttk.Button(container, text="Save Expense", command=save_expense)
    save_button.pack(pady=5)


    return frame