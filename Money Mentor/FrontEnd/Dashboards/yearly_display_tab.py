import customtkinter as ctk
from datetime import datetime
import json
import os
from pathlib import Path
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D  # Needed for 3D plotting

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage" / "YearlySpending"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_year_file(year):
    return DATA_DIR / f"{year}.json"


def load_year_data(year):
    file_name = get_year_file(year)

    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)

    return None


def ctk_color_to_rgba(color):
    if isinstance(color, tuple):
        if all(isinstance(x, float) and 0 <= x <= 1 for x in color):
            return color
        elif all(isinstance(x, int) and 0 <= x <= 255 for x in color):
            return tuple(x / 255 for x in color)

    if isinstance(color, str):
        return color

    return "#1f1f1f"


def create_tab(notebook):
    frame = ctk.CTkFrame(notebook)
    notebook.add(frame, text="Yearly Spending Charts")

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    ctk.CTkLabel(
        frame,
        text="Yearly Spending Charts",
        font=("Segoe UI", 16, "bold")
    ).pack(pady=(20, 10))

    input_frame = ctk.CTkFrame(frame)
    input_frame.pack(pady=(0, 10))

    year_entry = ctk.CTkEntry(input_frame, width=120, corner_radius=10)
    year_entry.grid(row=0, column=0, padx=(0, 10))
    year_entry.insert(0, str(datetime.now().year))

    chart_frame = ctk.CTkFrame(frame, corner_radius=15)
    chart_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def clear_chart():
        for widget in chart_frame.winfo_children():
            widget.destroy()

    def calculate_yearly_expenses(year):
        data = load_year_data(year)

        totals = {month: 0 for month in months}

        if not data:
            return totals

        yearly_months = data.get("months", {})

        for month in months:
            totals[month] = yearly_months.get(month, {}).get("expense", 0)

        return totals

    def show_chart():
        clear_chart()

        year = year_entry.get()

        if not year.isdigit():
            ctk.CTkLabel(chart_frame, text="Enter a valid year").pack(pady=20)
            return

        year = int(year)

        monthly_totals = calculate_yearly_expenses(year)

        if sum(monthly_totals.values()) == 0:
            ctk.CTkLabel(
                chart_frame,
                text=f"No expense data available for {year}"
            ).pack(pady=20)
            return

        labels = list(monthly_totals.keys())
        values = list(monthly_totals.values())

        bg_color = ctk_color_to_rgba(chart_frame.cget("fg_color"))

        fig = Figure(figsize=(7, 4.5), facecolor=bg_color)
        ax = fig.add_subplot(111, projection="3d", facecolor=bg_color)

        xs = range(len(labels))
        ys = [0] * len(labels)
        zs = [0] * len(labels)

        dx = [0.5] * len(labels)
        dy = [0.5] * len(labels)
        dz = values

        ax.bar3d(xs, ys, zs, dx, dy, dz, color="#4a90e2", shade=True)

        ax.set_xticks([x + 0.25 for x in xs])
        ax.set_xticklabels(labels, rotation=45, ha="right", color="white")

        ax.set_yticks([])

        ax.tick_params(axis="z", colors="white")
        ax.set_zlabel("Expense", color="white")

        ax.set_title(f"{year} Monthly Expenses", color="white")

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    submit_btn = ctk.CTkButton(
        input_frame,
        text="Show Chart",
        command=show_chart,
        width=120,
        corner_radius=15
    )
    submit_btn.grid(row=0, column=1)

    show_chart()

    return frame