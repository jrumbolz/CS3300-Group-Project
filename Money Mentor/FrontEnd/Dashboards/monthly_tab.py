import customtkinter as ctk
import json
import os
from pathlib import Path
from datetime import datetime


# Gets the main project directory
BASE_DIR = Path(__file__).resolve().parents[2]


# Folder where monthly spending files are stored
DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage" / "MonthlySpending"
DATA_DIR.mkdir(parents=True, exist_ok=True)


# Folder where yearly summary files are stored
YEARLY_DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage" / "YearlySpending"
YEARLY_DATA_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------------
# Returns file path for selected month/year
# Example: 2026_April.json
# -----------------------------------------
def get_month_file(month, year):
    return DATA_DIR / f"{year}_{month}.json"


# -----------------------------------------
# Loads monthly JSON data
# Returns default structure if file doesn't exist
# -----------------------------------------
def load_month_data(month, year):
    file_name = get_month_file(month, year)

    # If file doesn't exist, create empty structure
    if not os.path.exists(file_name):
        return {
            "summary": {
                "total_income": 0,
                "total_expense": 0,
                "net_total": 0
            },
            "entries": []
        }

    # Open JSON file
    with open(file_name, "r") as f:
        data = json.load(f)

    # Handles older versions that only stored lists
    if isinstance(data, list):
        return {
            "summary": {
                "total_income": 0,
                "total_expense": 0,
                "net_total": 0
            },
            "entries": data
        }

    return data


# -----------------------------------------
# Saves monthly data to JSON
# -----------------------------------------
def save_month_data(month, year, data):
    file_name = get_month_file(month, year)

    # Ensures directory exists
    file_name.parent.mkdir(parents=True, exist_ok=True)

    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------------------
# Gets all monthly files for a selected year
# -----------------------------------------
def get_month_files(year):
    return sorted(DATA_DIR.glob(f"{year}_*.json"))


# -----------------------------------------
# Builds yearly summary from all monthly files
# -----------------------------------------
def build_year_summary(year):
    yearly_data = {
        "year": year,
        "total_income": 0.0,
        "total_expense": 0.0,
        "net_total": 0.0,
        "months": {}
    }

    # Loops through each monthly file
    for file in get_month_files(year):
        try:
            with open(file, "r") as f:
                data = json.load(f)

        except (FileNotFoundError, json.JSONDecodeError):
            continue

        summary = data.get("summary", {})

        try:
            month_name = file.stem.split("_", 1)[1]
        except IndexError:
            continue

        income = float(summary.get("total_income", 0))
        expense = float(summary.get("total_expense", 0))
        net = float(summary.get("net_total", income - expense))

        # Saves monthly totals
        yearly_data["months"][month_name] = {
            "income": income,
            "expense": expense,
            "net": net
        }

        # Adds to yearly totals
        yearly_data["total_income"] += income
        yearly_data["total_expense"] += expense
        yearly_data["net_total"] += net

    # Rounds final totals
    yearly_data["total_income"] = round(yearly_data["total_income"], 2)
    yearly_data["total_expense"] = round(yearly_data["total_expense"], 2)
    yearly_data["net_total"] = round(yearly_data["net_total"], 2)

    return yearly_data


# -----------------------------------------
# Saves yearly summary file
# -----------------------------------------
def save_year_file(year):
    yearly_summary = build_year_summary(year)
    file_path = YEARLY_DATA_DIR / f"{year}.json"

    with open(file_path, "w") as f:
        json.dump(yearly_summary, f, indent=4)


# -----------------------------------------
# Calculates monthly totals
# -----------------------------------------
def calculate_summary(entries):
    income = 0
    expense = 0

    for e in entries:
        amount = float(e.get("amount", 0))

        if e.get("type") == "Income":
            income += amount
        else:
            expense += amount

    return {
        "total_income": round(income, 2),
        "total_expense": round(expense, 2),
        "net_total": round(income - expense, 2)
    }


# -----------------------------------------
# Creates Monthly Spending UI Tab
# -----------------------------------------
def create_tab(notebook):

    # Creates tab
    frame = ctk.CTkFrame(notebook)
    notebook.add(frame, text="Monthly Spending")

    # Month dropdown values
    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    current_year = datetime.now().year
    years = [str(y) for y in range(current_year - 10, current_year + 1)]

    # Main layout container
    container = ctk.CTkFrame(frame)
    container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    # UI layout settings
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)

    # Year selection
    ctk.CTkLabel(container, text="Select Year:").grid(row=0, column=0)
    year_combo = ctk.CTkComboBox(container, values=years)
    year_combo.grid(row=0, column=1)
    year_combo.set(str(current_year))

    # Month selection
    ctk.CTkLabel(container, text="Select Month:").grid(row=1, column=0)
    month_combo = ctk.CTkComboBox(container, values=months)
    month_combo.grid(row=1, column=1)
    month_combo.set(datetime.now().strftime("%B"))

    # Income/Expense selection
    ctk.CTkLabel(container, text="Type:").grid(row=2, column=0)
    type_combo = ctk.CTkComboBox(
        container,
        values=["Expense", "Income"]
    )
    type_combo.grid(row=2, column=1)

    from categories_tab import load_categories
    categories = load_categories()

    # Category selection
    ctk.CTkLabel(container, text="Category:").grid(row=3, column=0)
    category_combo = ctk.CTkComboBox(
        container,
        values=categories
    )
    category_combo.grid(row=3, column=1)

    # Amount input
    ctk.CTkLabel(container, text="Amount:").grid(row=4, column=0)
    amount_entry = ctk.CTkEntry(container)
    amount_entry.grid(row=4, column=1)

    # Loads existing month data
    data = load_month_data(
        month_combo.get(),
        int(year_combo.get())
    )

    current_data = data["entries"]
    selected_index = None

    # Status messages
    result_label = ctk.CTkLabel(container, text="")
    result_label.grid(row=6, column=0, columnspan=2)

    # Scrollable entry list
    entries_frame = ctk.CTkScrollableFrame(
        container,
        width=450,
        height=250
    )
    entries_frame.grid(row=7, column=0, columnspan=2)

    # Delete field
    delete_entry = ctk.CTkEntry(container)
    delete_entry.grid(row=8, column=1)

    
    # Selects entry using mouse click
    def select_entry(index):
        nonlocal selected_index

        selected_index = index

        delete_entry.delete(0, "end")
        delete_entry.insert(0, str(index))

        result_label.configure(
            text=f"Selected entry {index}"
        )


    # Refreshes displayed entries
    def refresh_list():
        for widget in entries_frame.winfo_children():
            widget.destroy()

        summary = data.get("summary", {})

        # Shows summary totals
        ctk.CTkLabel(
            entries_frame,
            text=f"Income: ${summary['total_income']}"
        ).pack()

        ctk.CTkLabel(
            entries_frame,
            text=f"Expense: ${summary['total_expense']}"
        ).pack()

        ctk.CTkLabel(
            entries_frame,
            text=f"Net: ${summary['net_total']}"
        ).pack()

        # Creates clickable entry buttons
        for i, entry in enumerate(current_data):
            entry_text = (
                f"{i}: ${entry['amount']} "
                f"{entry['category']} "
                f"{entry['type']}"
            )

            ctk.CTkButton(
                entries_frame,
                text=entry_text,
                command=lambda index=i: select_entry(index)
            ).pack(fill="x")


    # Saves monthly + yearly data
    def save_all():
        selected_year = int(year_combo.get())

        data["summary"] = calculate_summary(current_data)

        save_month_data(
            month_combo.get(),
            selected_year,
            data
        )

        save_year_file(selected_year)


    # Saves new transaction
    def save_entry():
        try:
            amount = float(amount_entry.get())

            current_data.append({
                "amount": amount,
                "category": category_combo.get(),
                "type": type_combo.get(),
                "time": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            })

            save_all()
            refresh_list()

        except ValueError:
            result_label.configure(
                text="Invalid amount"
            )


    # Deletes selected transaction
    def delete_entry_func():
        try:
            index = int(delete_entry.get())

            current_data.pop(index)

            save_all()
            refresh_list()

        except:
            result_label.configure(
                text="Invalid selection"
            )


    # Save button
    ctk.CTkButton(
        container,
        text="Save Entry",
        command=save_entry
    ).grid(row=5, column=0, columnspan=2)

    # Delete button
    ctk.CTkButton(
        container,
        text="Delete Entry",
        command=delete_entry_func
    ).grid(row=9, column=0, columnspan=2)

    refresh_list()

    return frame