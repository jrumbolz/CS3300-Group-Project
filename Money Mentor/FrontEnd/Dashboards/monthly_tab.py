import customtkinter as ctk
import json
import os
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage" / "MonthlySpending"
DATA_DIR.mkdir(parents=True, exist_ok=True)

YEARLY_DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage" / "YearlySpending"
YEARLY_DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_month_file(month, year):
    return DATA_DIR / f"{year}_{month}.json"


def load_month_data(month, year):
    file_name = get_month_file(month, year)

    if not os.path.exists(file_name):
        return {
            "summary": {
                "total_income": 0,
                "total_expense": 0,
                "net_total": 0
            },
            "entries": []
        }

    with open(file_name, "r") as f:
        data = json.load(f)

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


def save_month_data(month, year, data):
    file_name = get_month_file(month, year)
    file_name.parent.mkdir(parents=True, exist_ok=True)

    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)


def get_month_files(year):
    return sorted(DATA_DIR.glob(f"{year}_*.json"))


def build_year_summary(year):
    yearly_data = {
        "year": year,
        "total_income": 0.0,
        "total_expense": 0.0,
        "net_total": 0.0,
        "months": {}
    }

    for file in get_month_files(year):
        try:
            with open(file, "r") as f:
                data = json.load(f)
        except:
            continue

        summary = data.get("summary", {})

        try:
            month_name = file.stem.split("_", 1)[1]
        except:
            continue

        income = float(summary.get("total_income", 0))
        expense = float(summary.get("total_expense", 0))
        net = float(summary.get("net_total", income - expense))

        yearly_data["months"][month_name] = {
            "income": income,
            "expense": expense,
            "net": net
        }

        yearly_data["total_income"] += income
        yearly_data["total_expense"] += expense
        yearly_data["net_total"] += net

    yearly_data["total_income"] = round(yearly_data["total_income"], 2)
    yearly_data["total_expense"] = round(yearly_data["total_expense"], 2)
    yearly_data["net_total"] = round(yearly_data["net_total"], 2)

    return yearly_data


def save_year_file(year):
    yearly_summary = build_year_summary(year)
    file_path = YEARLY_DATA_DIR / f"{year}.json"

    with open(file_path, "w") as f:
        json.dump(yearly_summary, f, indent=4)


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

    ctk.CTkLabel(container, text="Select Year:").grid(row=0, column=0)
    year_combo = ctk.CTkComboBox(container, values=years)
    year_combo.grid(row=0, column=1)
    year_combo.set(str(current_year))

    ctk.CTkLabel(container, text="Select Month:").grid(row=1, column=0)
    month_combo = ctk.CTkComboBox(container, values=months)
    month_combo.grid(row=1, column=1)
    month_combo.set(datetime.now().strftime("%B"))

    ctk.CTkLabel(container, text="Type:").grid(row=2, column=0)
    type_combo = ctk.CTkComboBox(container, values=["Expense", "Income"])
    type_combo.grid(row=2, column=1)

    from categories_tab import load_categories

    categories = load_categories()

    def refresh_categories():
        category_combo.configure(values=load_categories())

    ctk.CTkLabel(container, text="Category:").grid(row=3, column=0)
    category_combo = ctk.CTkComboBox(container, values=categories)
    category_combo.grid(row=3, column=1)

    ctk.CTkLabel(container, text="Amount:").grid(row=4, column=0)
    amount_entry = ctk.CTkEntry(container)
    amount_entry.grid(row=4, column=1)

    data = load_month_data(
        month_combo.get(),
        int(year_combo.get())
    )

    current_data = data["entries"]

    result_label = ctk.CTkLabel(container, text="")
    result_label.grid(row=6, column=0, columnspan=2)

    entries_frame = ctk.CTkScrollableFrame(container, width=450, height=250)
    entries_frame.grid(row=7, column=0, columnspan=2)

    delete_entry = ctk.CTkEntry(container)
    delete_entry.grid(row=8, column=1)

    def refresh_list():
        for widget in entries_frame.winfo_children():
            widget.destroy()

        summary = data.get("summary", {})

        ctk.CTkLabel(entries_frame, text=f"Income: ${summary['total_income']}").pack()
        ctk.CTkLabel(entries_frame, text=f"Expense: ${summary['total_expense']}").pack()
        ctk.CTkLabel(entries_frame, text=f"Net: ${summary['net_total']}").pack()

        for i, entry in enumerate(current_data):
            text = f"{i}: ${entry['amount']} {entry['category']} {entry['type']}"
            ctk.CTkButton(entries_frame, text=text).pack(fill="x")

    def save_all():
        selected_year = int(year_combo.get())
        data["summary"] = calculate_summary(current_data)

        save_month_data(month_combo.get(), selected_year, data)
        save_year_file(selected_year)

    def save_entry():
        try:
            amount = float(amount_entry.get())

            current_data.append({
                "amount": amount,
                "category": category_combo.get(),
                "type": type_combo.get(),
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            save_all()
            refresh_list()

        except:
            result_label.configure(text="Invalid amount")

    def delete_entry_func():
        try:
            index = int(delete_entry.get())
            current_data.pop(index)

            save_all()
            refresh_list()

        except:
            result_label.configure(text="Invalid selection")

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

    #new refresh
    ctk.CTkButton(
        container,
        text="Refresh Categories",
        command=refresh_categories
    ).grid(row=10, column=0, columnspan=2, pady=10)

    refresh_list()

    return frame