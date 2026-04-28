import customtkinter as ctk
import json
import os
from pathlib import Path
from datetime import datetime


# Gets the base project directory
# parents[2] moves up two folders from this file's location
BASE_DIR = Path(__file__).resolve().parents[2]


# Creates path for storing monthly spending data
# Example:
# /Users/YourName/Desktop/MoneyMentor/BackEnd/Data Storage/MonthlySpending/
DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage" / "MonthlySpending"
DATA_DIR.mkdir(parents=True, exist_ok=True)


# Creates path for storing yearly spending summaries
# Example:
# /Users/YourName/Desktop/MoneyMentor/BackEnd/Data Storage/YearlySpending/
YEARLY_DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage" / "YearlySpending"
YEARLY_DATA_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------
# Build file path for selected month
# -----------------------------------
def get_month_file(month, year):
    return DATA_DIR / f"{year}_{month}.json"


# -----------------------------------
# Load saved monthly data
# -----------------------------------
def load_month_data(month, year):

    # Builds the JSON file name for the selected month and year
    file_name = get_month_file(month, year)

    # If the file does not exist yet, start with empty totals and entries
    if not os.path.exists(file_name):
        return {
            "summary": {
                "total_income": 0,
                "total_expense": 0,
                "net_total": 0
            },
            "entries": []
        }

    # Opens and reads saved monthly spending data
    with open(file_name, "r") as f:
        data = json.load(f)

    # Handles older files that may only contain an entry list
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


# -----------------------------------
# Save monthly data to JSON file
# -----------------------------------
def save_month_data(month, year, data):

    # Builds the file path for the selected month and year
    file_name = get_month_file(month, year)

    # Creates the folder if it does not already exist
    file_name.parent.mkdir(parents=True, exist_ok=True)

    # Saves the monthly data
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------------
# Find all monthly files for a year
# -----------------------------------
def get_month_files(year):
    return sorted(DATA_DIR.glob(f"{year}_*.json"))


# -----------------------------------
# Build yearly summary data
# -----------------------------------
def build_year_summary(year):

    # Starting totals for the whole year
    yearly_data = {
        "year": year,
        "total_income": 0.0,
        "total_expense": 0.0,
        "net_total": 0.0,
        "months": {}
    }

    for file in get_month_files(year):
        try:
            # Opens each monthly file for the selected year
            with open(file, "r") as f:
                data = json.load(f)
        except:
            continue

        # Gets the saved monthly summary
        summary = data.get("summary", {})

        try:
            # Gets the month name from the file name
            # Example:
            # 2026_April.json becomes April
            month_name = file.stem.split("_", 1)[1]
        except:
            continue

        # Converts summary values to numbers
        income = float(summary.get("total_income", 0))
        expense = float(summary.get("total_expense", 0))
        net = float(summary.get("net_total", income - expense))

        # Stores the month totals inside the yearly summary
        yearly_data["months"][month_name] = {
            "income": income,
            "expense": expense,
            "net": net
        }

        # Adds monthly values to the yearly totals
        yearly_data["total_income"] += income
        yearly_data["total_expense"] += expense
        yearly_data["net_total"] += net

    # Rounds totals before saving
    yearly_data["total_income"] = round(yearly_data["total_income"], 2)
    yearly_data["total_expense"] = round(yearly_data["total_expense"], 2)
    yearly_data["net_total"] = round(yearly_data["net_total"], 2)

    return yearly_data


# -----------------------------------
# Save yearly summary file
# -----------------------------------
def save_year_file(year):

    # Rebuilds yearly totals from all monthly files
    yearly_summary = build_year_summary(year)

    # Creates the yearly JSON file path
    file_path = YEARLY_DATA_DIR / f"{year}.json"

    # Saves the yearly summary
    with open(file_path, "w") as f:
        json.dump(yearly_summary, f, indent=4)


# -----------------------------------
# Calculate income, expense, and net
# -----------------------------------
def calculate_summary(entries):
    income = 0
    expense = 0

    for e in entries:
        # Gets the entry amount
        amount = float(e.get("amount", 0))

        # Adds the amount to income or expense totals
        if e.get("type") == "Income":
            income += amount
        else:
            expense += amount

    # Returns rounded summary values
    return {
        "total_income": round(income, 2),
        "total_expense": round(expense, 2),
        "net_total": round(income - expense, 2)
    }


# -----------------------------------
# Create Monthly Spending Tab UI
# -----------------------------------
def create_tab(notebook):

    # Creates tab frame
    frame = ctk.CTkFrame(notebook)

    # Adds tab to notebook navigation
    notebook.add(frame, text="Monthly Spending")

    # List of months for the month dropdown
    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    # Builds a year list from 10 years ago through the current year
    current_year = datetime.now().year
    years = [str(y) for y in range(current_year - 10, current_year + 1)]

    # Main container frame
    container = ctk.CTkFrame(frame)
    container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    # Allows the tab and container to resize
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)

    # -----------------------------
    # Date selection section
    # -----------------------------
    ctk.CTkLabel(container, text="Select Year:").grid(row=0, column=0)
    year_combo = ctk.CTkComboBox(container, values=years)
    year_combo.grid(row=0, column=1)
    year_combo.set(str(current_year))

    ctk.CTkLabel(container, text="Select Month:").grid(row=1, column=0)
    month_combo = ctk.CTkComboBox(container, values=months)
    month_combo.grid(row=1, column=1)
    month_combo.set(datetime.now().strftime("%B"))

    # -----------------------------
    # Entry input section
    # -----------------------------
    ctk.CTkLabel(container, text="Type:").grid(row=2, column=0)
    type_combo = ctk.CTkComboBox(container, values=["Expense", "Income"])
    type_combo.grid(row=2, column=1)

    # Imports the categories tab so this tab can read its update flag
    import categories_tab

    # Tracks the last category update this tab has seen
    last_category_version = categories_tab.CATEGORY_VERSION

    # Refreshes the category dropdown while keeping the current selection if possible
    def refresh_categories():
        current_selection = category_combo.get()
        categories = categories_tab.load_categories()

        category_combo.configure(values=categories)

        if current_selection in categories:
            category_combo.set(current_selection)
        elif categories:
            category_combo.set(categories[0])
        else:
            category_combo.set("")

    ctk.CTkLabel(container, text="Category:").grid(row=3, column=0)
    category_combo = ctk.CTkComboBox(container, values=categories_tab.load_categories())
    category_combo.grid(row=3, column=1)

    ctk.CTkLabel(container, text="Amount:").grid(row=4, column=0)
    amount_entry = ctk.CTkEntry(container)
    amount_entry.grid(row=4, column=1)

    # Loads data for the default selected month and year
    data = load_month_data(
        month_combo.get(),
        int(year_combo.get())
    )

    # Stores the current month's entries in memory while editing
    current_data = data["entries"]

    # Label used for success and error messages
    result_label = ctk.CTkLabel(container, text="")
    result_label.grid(row=6, column=0, columnspan=2)

    # Scrollable area that displays summary totals and saved entries
    entries_frame = ctk.CTkScrollableFrame(container, width=450, height=250)
    entries_frame.grid(row=7, column=0, columnspan=2)

    # Input box for selecting which entry index to delete
    ctk.CTkLabel(container, text="Entry to delete:").grid(row=8, column=0)
    delete_entry = ctk.CTkEntry(container)
    delete_entry.grid(row=8, column=1)

    # Reloads data when the selected month or year changes
    def load_selected_month():
        nonlocal data, current_data

        data = load_month_data(
            month_combo.get(),
            int(year_combo.get())
        )
        current_data = data["entries"]
        refresh_list()

    # Refreshes the displayed summary and entry list
    def refresh_list():
        for widget in entries_frame.winfo_children():
            widget.destroy()

        # Recalculates totals from the current entry list
        data["summary"] = calculate_summary(current_data)
        summary = data.get("summary", {})

        ctk.CTkLabel(entries_frame, text=f"Income: ${summary['total_income']}").pack()
        ctk.CTkLabel(entries_frame, text=f"Expense: ${summary['total_expense']}").pack()
        ctk.CTkLabel(entries_frame, text=f"Net: ${summary['net_total']}").pack()

        for i, entry in enumerate(current_data):
            text = f"{i}: ${entry['amount']} {entry['category']} {entry['type']}"

            # Each entry button fills the delete box with its index
            ctk.CTkButton(
                entries_frame,
                text=text,
                command=lambda index=i: select_entry(index)
            ).pack(fill="x")

    # Selects an entry for deletion
    def select_entry(index):
        delete_entry.delete(0, "end")
        delete_entry.insert(0, str(index))
        result_label.configure(text=f"Selected entry {index}")

    # Saves monthly data and rebuilds the yearly summary
    def save_all():
        selected_year = int(year_combo.get())
        data["summary"] = calculate_summary(current_data)

        save_month_data(month_combo.get(), selected_year, data)
        save_year_file(selected_year)

    # Adds a new income or expense entry
    def save_entry():
        try:
            # Converts the entered amount into a number
            amount = float(amount_entry.get())

            # Adds the new entry to the current month's list
            current_data.append({
                "amount": amount,
                "category": category_combo.get(),
                "type": type_combo.get(),
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            save_all()
            amount_entry.delete(0, "end")
            refresh_list()
            result_label.configure(text="Entry saved")

        except:
            result_label.configure(text="Invalid amount")

    # Deletes the selected entry by index
    def delete_entry_func():
        try:
            # Converts the selected entry index into a number
            index = int(delete_entry.get())

            # Prevents deleting an entry that does not exist
            if index < 0 or index >= len(current_data):
                raise IndexError

            current_data.pop(index)

            save_all()
            delete_entry.delete(0, "end")
            refresh_list()
            result_label.configure(text="Entry deleted")

        except:
            result_label.configure(text="Invalid selection")

    # Reloads monthly data when the year or month dropdown changes
    year_combo.configure(command=lambda _: load_selected_month())
    month_combo.configure(command=lambda _: load_selected_month())

    # Refreshes categories automatically when returning to this tab
    def refresh_categories_if_needed(event=None):
        nonlocal last_category_version

        # Checks which tab is currently selected
        selected_tab = notebook.nametowidget(notebook.select())

        # Only updates the category dropdown if categories have changed
        if selected_tab == frame and last_category_version != categories_tab.CATEGORY_VERSION:
            refresh_categories()
            last_category_version = categories_tab.CATEGORY_VERSION

    # Watches for notebook tab changes
    notebook.bind("<<NotebookTabChanged>>", refresh_categories_if_needed, add="+")

    # ---------------- BUTTONS ----------------

    ctk.CTkButton(
        container,
        text="Save Entry",
        command=save_entry
    ).grid(row=5, column=0, columnspan=2)

    ctk.CTkButton(
        container,
        text="Delete Entry",
        command=delete_entry_func
    ).grid(row=9, column=0, columnspan=2)

    refresh_list()

    return frame