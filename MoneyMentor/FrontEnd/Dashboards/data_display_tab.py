import tkinter as tk
from tkinter import ttk
import json
import os
from pathlib import Path
from datetime import datetime

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "BackEnd" / "Data"
print(DATA_DIR)

def get_month_file(month, year):
    return f"{DATA_DIR}\{year}\{month}.json"

def load_month_data(month, year):
    file_name = get_month_file(month, year)
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return []

def create_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Spending Charts")

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    # year options (last 5 years + current)
    current_year = datetime.now().year
    years = [str(y) for y in range(current_year - 10, current_year)]

    # title
    ttk.Label(frame, text="Spending Breakdown", font=("Arial", 16)).pack(pady=10)

    # selection frame (for month + year)
    selection_frame = ttk.Frame(frame)
    selection_frame.pack(pady=5)

    # month dropdown
    month_combo = ttk.Combobox(selection_frame, values=months, state="readonly", width=12)
    month_combo.grid(row=0, column=0, padx=5)
    month_combo.set(datetime.now().strftime("%B"))

    # year dropdown
    year_combo = ttk.Combobox(selection_frame, values=years, state="readonly", width=8)
    year_combo.grid(row=0, column=1, padx=5)
    year_combo.set(str(current_year))

    # chart frame
    chart_frame = ttk.Frame(frame)
    chart_frame.pack(fill="both", expand=True)

    def clear_chart():
        for widget in chart_frame.winfo_children():
            widget.destroy()

    def show_chart(event=None): 
        clear_chart()

        month = month_combo.get()
        year = year_combo.get()  # ✅ now uses selected year
        data = load_month_data(month, year)

        if not data:
            ttk.Label(chart_frame, text="No data available for this month").pack()
            return

        category_totals = {}
        for entry in data:
            category = entry.get("category")
            amount = entry.get("amount", 0)

            if category:
                category_totals[category] = category_totals.get(category, 0) + amount

        # empty data catcher
        if not category_totals or sum(category_totals.values()) == 0:
            ttk.Label(chart_frame, text="No spending data to display").pack()
            return

        labels = list(category_totals.keys())
        values = list(category_totals.values())

        # creating the pie chart
        fig = Figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        ax.set_title(f"{month} {year} Spending Breakdown")

        # chart embedded
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # auto update when selection changes
    month_combo.bind("<<ComboboxSelected>>", show_chart)
    year_combo.bind("<<ComboboxSelected>>", show_chart)

    # button (optional manual refresh)
    ttk.Button(frame, text="Show Chart", command=show_chart).pack(pady=10)

    # shows current month immediately
    show_chart()

    return frame