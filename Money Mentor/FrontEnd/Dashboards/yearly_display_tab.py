import customtkinter as ctk
from datetime import datetime
import json
import os
from pathlib import Path
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        text="Yearly Income, Expense, and Net Charts",
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

    def calculate_yearly_values(year):
        data = load_year_data(year)

        totals = {
            month: {
                "income": 0,
                "expense": 0,
                "net": 0
            }
            for month in months
        }

        if not data:
            return totals

        yearly_months = data.get("months", {})

        for month in months:
            month_data = yearly_months.get(month, {})

            totals[month]["income"] = float(month_data.get("income", 0))
            totals[month]["expense"] = float(month_data.get("expense", 0))
            totals[month]["net"] = float(month_data.get("net", 0))

        return totals

    def show_chart():
        clear_chart()

        year = year_entry.get()

        if not year.isdigit():
            ctk.CTkLabel(chart_frame, text="Enter a valid year").pack(pady=20)
            return

        year = int(year)

        yearly_values = calculate_yearly_values(year)

        has_data = any(
            values["income"] != 0 or values["expense"] != 0 or values["net"] != 0
            for values in yearly_values.values()
        )

        if not has_data:
            ctk.CTkLabel(
                chart_frame,
                text=f"No data available for {year}"
            ).pack(pady=20)
            return

        labels = months
        x = list(range(len(labels)))

        income_values = [yearly_values[month]["income"] for month in labels]
        expense_values = [yearly_values[month]["expense"] for month in labels]
        net_values = [yearly_values[month]["net"] for month in labels]

        bg_color = ctk_color_to_rgba(chart_frame.cget("fg_color"))

        fig = Figure(figsize=(10, 5), facecolor=bg_color)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)

        bar_width = 0.25

        income_x = [pos - bar_width for pos in x]
        expense_x = x
        net_x = [pos + bar_width for pos in x]

        ax.bar(
            income_x,
            income_values,
            width=bar_width,
            color="#2ecc71",
            label="Income"
        )

        ax.bar(
            expense_x,
            expense_values,
            width=bar_width,
            color="#e74c3c",
            label="Expense"
        )

        ax.bar(
            net_x,
            net_values,
            width=bar_width,
            color="#3498db",
            label="Net"
        )

        ax.set_title(
            f"{year} Monthly Income / Expense / Net",
            color="white"
        )

        ax.set_ylabel("Amount ($)", color="white")

        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha="right", color="white")

        ax.tick_params(axis="y", colors="white")

        ax.spines["bottom"].set_color("white")
        ax.spines["left"].set_color("white")
        ax.spines["top"].set_color(bg_color)
        ax.spines["right"].set_color(bg_color)

        ax.grid(axis="y", alpha=0.3)

        legend = ax.legend()
        for text in legend.get_texts():
            text.set_color("black")

        fig.tight_layout()

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