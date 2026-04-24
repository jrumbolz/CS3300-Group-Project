import customtkinter as ctk
import json
import os
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage" / "MonthlySpending"
DATA_DIR.mkdir(parents=True, exist_ok=True)

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
    file_name.parent.mkdir(parents=True, exist_ok=True)
    with open(file_name, "w") as f:
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
    container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)

    # --- Year ---
    ctk.CTkLabel(container, text="Select Year:").grid(row=0, column=0, pady=5, sticky="e")
    year_combo = ctk.CTkComboBox(container, values=years, width=200)
    year_combo.grid(row=0, column=1, pady=5, sticky="w")
    year_combo.set(str(current_year))

    # --- Month ---
    ctk.CTkLabel(container, text="Select Month:").grid(row=1, column=0, pady=5, sticky="e")
    month_combo = ctk.CTkComboBox(container, values=months, width=200)
    month_combo.grid(row=1, column=1, pady=5, sticky="w")
    month_combo.set(datetime.now().strftime("%B"))

    # --- Type ---
    ctk.CTkLabel(container, text="Type:").grid(row=2, column=0, pady=5, sticky="e")
    type_combo = ctk.CTkComboBox(container, values=["Expense", "Income"], width=200)
    type_combo.grid(row=2, column=1, pady=5, sticky="w")
    type_combo.set("Expense")

    # --- Category ---
    from categories_tab import load_categories
    categories = load_categories()
    ctk.CTkLabel(container, text="Category:").grid(row=3, column=0, pady=5, sticky="e")
    category_combo = ctk.CTkComboBox(container, values=categories, width=200)
    category_combo.grid(row=3, column=1, pady=5, sticky="w")
    category_combo.set(categories[0] if categories else "")

    # --- Amount ---
    ctk.CTkLabel(container, text="Amount:").grid(row=4, column=0, pady=5, sticky="e")
    amount_entry = ctk.CTkEntry(container, width=200, corner_radius=8)
    amount_entry.grid(row=4, column=1, pady=5, sticky="w")

    # --- Delete Index ---
    ctk.CTkLabel(container, text="Delete Index:").grid(row=5, column=0, pady=5, sticky="e")
    delete_entry = ctk.CTkEntry(container, width=200, corner_radius=8)
    delete_entry.grid(row=5, column=1, pady=5, sticky="w")

    # --- Result ---
    result_label = ctk.CTkLabel(container, text="")
    result_label.grid(row=6, column=0, columnspan=2, pady=10)

    # --- Listbox ---
    listbox = ctk.CTkTextbox(container, width=400, height=200, corner_radius=8)
    listbox.grid(row=7, column=0, columnspan=2, pady=10)

    current_data = []

    def refresh_list():
        listbox.configure(state="normal")
        listbox.delete("0.0", "end")

        balance = 0
        for i, entry in enumerate(current_data):
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
                f"{i}: {prefix}${amount:.2f} - {category} ({entry_type}) ({time_str})\n"
            )

        if current_data:
            listbox.insert("end", f"--- Balance: ${balance:.2f} ---\n")

        listbox.configure(state="disabled")

    def load_selected_month(event=None):
        nonlocal current_data
        month = month_combo.get()
        year = int(year_combo.get())
        current_data = load_month_data(month, year)
        refresh_list()

    # --- Save Button ---
    def save_entry():
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

    # --- Delete Function ---
    def delete_entry_func():
        nonlocal current_data
        value = delete_entry.get()

        try:
            index = int(value)

            if index < 0 or index >= len(current_data):
                result_label.configure(text="Invalid index.")
                return

            removed = current_data.pop(index)

            month = month_combo.get()
            year = int(year_combo.get())
            save_month_data(month, year, current_data)

            refresh_list()
            result_label.configure(
                text=f"Deleted ${removed['amount']:.2f} ({removed['type']})"
            )
            delete_entry.delete(0, "end")

        except ValueError:
            result_label.configure(text="Enter a valid index.")

    # --- Buttons ---
    ctk.CTkButton(
        container,
        text="Save Entry",
        width=200,
        corner_radius=15,
        command=save_entry
    ).grid(row=8, column=0, columnspan=2, pady=10)

    ctk.CTkButton(
        container,
        text="Delete Entry",
        width=200,
        corner_radius=15,
        fg_color="red",
        command=delete_entry_func
    ).grid(row=9, column=0, columnspan=2, pady=10)

    # --- Bind Events ---
    month_combo.configure(command=load_selected_month)
    year_combo.configure(command=load_selected_month)

    # --- Initial Load ---
    load_selected_month()

    return frame