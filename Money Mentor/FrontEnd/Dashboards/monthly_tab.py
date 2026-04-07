import customtkinter as ctk
import json
import os
from pathlib import Path
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_month_file(month, year):
    # 1. Create the path for the year subfolder (e.g., Data Storage/2024/)
    year_dir = DATA_DIR / str(year)
    year_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. Return the path for the month file (e.g., Data Storage/2024/January.json)
    return year_dir / f"{month}.json"

def load_month_data(month, year):
    file_path = get_month_file(month, year)
    
    # If the file doesn't exist, create it with an empty list []
    if not file_path.exists():
        with open(file_path, "w") as f:
            json.dump([], f, indent=4)
        return []
    
    # Otherwise, load the existing data
    with open(file_path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return [] # Returns empty list if file is corrupted

def save_month_data(month, year, data):
    file_path = get_month_file(month, year)
    # Ensure the parent folder (the year folder) exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def create_tab(notebook):
    frame = ctk.CTkFrame(notebook)
    notebook.add(frame, text="Monthly Spending")

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    current_year = datetime.now().year
    years = [str(y) for y in range(current_year - 10, current_year + 1)]

    container = ctk.CTkFrame(frame)
    container.pack(expand=True, pady=20)

    # ===== Year =====
    ctk.CTkLabel(container, text="Select Year:").grid(row=0, column=0, pady=5)
    year_combo = ctk.CTkComboBox(container, values=years, width=150)
    year_combo.grid(row=0, column=1, pady=5)
    year_combo.set(str(current_year))

    # ===== Month =====
    ctk.CTkLabel(container, text="Select Month:").grid(row=1, column=0, pady=5)
    month_combo = ctk.CTkComboBox(container, values=months, width=150)
    month_combo.grid(row=1, column=1, pady=5)
    month_combo.set(datetime.now().strftime("%B"))

    # ===== Type =====
    ctk.CTkLabel(container, text="Type:").grid(row=2, column=0, pady=5)
    type_combo = ctk.CTkComboBox(container, values=["Expense", "Income"], width=150)
    type_combo.grid(row=2, column=1, pady=5)
    type_combo.set("Expense")

    # ===== Category =====
    from categories_tab import load_categories
    categories = load_categories()

    ctk.CTkLabel(container, text="Category:").grid(row=3, column=0, pady=5)
    category_combo = ctk.CTkComboBox(container, values=categories, width=150)
    category_combo.grid(row=3, column=1, pady=5)
    category_combo.set(categories[0] if categories else "")

    # ===== Amount =====
    ctk.CTkLabel(container, text="Amount:").grid(row=4, column=0, pady=5)
    amount_entry = ctk.CTkEntry(container, width=150, corner_radius=8)
    amount_entry.grid(row=4, column=1, pady=5)

    # ===== Result =====
    result_label = ctk.CTkLabel(container, text="")
    result_label.grid(row=5, column=0, columnspan=2, pady=5)

    # ===== Listbox =====
    listbox = ctk.CTkTextbox(container, width=300, height=150, corner_radius=8)
    listbox.grid(row=6, column=0, columnspan=2, pady=10)

    current_data = []

    # ===== Refresh List =====
    def refresh_list():
        listbox.configure(state="normal")
        listbox.delete("0.0", "end")

        balance = 0

        for entry in current_data:
            amount = entry["amount"]
            category = entry["category"]
            entry_type = entry.get("type", "Expense")
            time_str = entry.get("time", "")

            if entry_type == "Expense":
                balance -= amount
                prefix = "-"
            else:
                balance += amount
                prefix = "+"

            listbox.insert(
                "end",
                f"{prefix}${amount:.2f} - {category} ({entry_type}) ({time_str})\n"
            )

        if current_data:
            listbox.insert("end", f"--- Balance: ${balance:.2f} ---\n")

        listbox.configure(state="disabled")

    # ===== Load Selected Month =====
    def load_selected_month(event=None):
        nonlocal current_data
        month = month_combo.get()
        year = int(year_combo.get())
        current_data = load_month_data(month, year)
        refresh_list()

    # ===== Save Entry =====
    def save_expense():
        nonlocal current_data
        now = datetime.now()

        value = amount_entry.get()
        category = category_combo.get() or "Miscellaneous"
        entry_type = type_combo.get()
        month = month_combo.get()
        year = int(year_combo.get())
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            amount = float(value)

            if amount < 0:
                result_label.configure(text="Enter a positive number.")
                return

            current_data = load_month_data(month, year)

            current_data.append({
                "amount": amount,
                "category": category,
                "type": entry_type,
                "time": timestamp
            })

            save_month_data(month, year, current_data)

            refresh_list()
            result_label.configure(text=f"Saved ${amount:.2f} ({entry_type})")
            amount_entry.delete(0, "end")

        except ValueError:
            result_label.configure(text="Enter a valid number.")

    # ===== Bind Events =====
    month_combo.configure(command=load_selected_month)
    year_combo.configure(command=load_selected_month)

    # ===== Save Button =====
    ctk.CTkButton(
        container,
        text="Save Entry",
        width=150,
        corner_radius=15,
        command=save_expense
    ).grid(row=7, column=0, columnspan=2, pady=10)

    # ===== Initial Load =====
    load_selected_month()

    return frame

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