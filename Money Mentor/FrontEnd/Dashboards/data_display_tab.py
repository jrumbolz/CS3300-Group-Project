import tkinter as tk
from tkinter import ttk
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
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Spending Charts")

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    # title
    ttk.Label(frame, text="Spending Breakdown", font=("Arial", 16)).pack(pady=10)

    # dropdown
    month_combo = ttk.Combobox(frame, values=months, state="readonly")
    month_combo.pack(pady=5)
    month_combo.set(datetime.now().strftime("%B"))

    # chart frame
    chart_frame = ttk.Frame(frame)
    chart_frame.pack(fill="both", expand=True)

  
    def clear_chart():
        for widget in chart_frame.winfo_children():
            widget.destroy()

    def show_chart(event=None): 
        clear_chart()

        month = month_combo.get()
        year = datetime.now().year
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

        #empty data catcher
        if not category_totals or sum(category_totals.values()) == 0:
            ttk.Label(chart_frame, text="No spending data to display").pack()
            return

        labels = list(category_totals.keys())
        values = list(category_totals.values())

        #creating the pie chart
        fig = Figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        ax.set_title(f"{month} Spending Breakdown")

        #chart that is embeded
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # auto update when month changes
    month_combo.bind("<<ComboboxSelected>>", show_chart)

    # button (optional manual refresh)
    ttk.Button(frame, text="Show Chart", command=show_chart).pack(pady=10)

    # shows current month immediately
    show_chart()

    return frame