import customtkinter as ctk
from datetime import datetime
import json
import os
from pathlib import Path
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D  # needed for 3D effect

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def get_month_file(month, year):
    return DATA_DIR / f"{year}_{month}.json"

def load_month_data(month, year):
    file_name = get_month_file(month, year)
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return []

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
    notebook.add(frame, text="Monthly Spending Charts")

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    # --- Title ---
    ctk.CTkLabel(frame, text="Monthly Spending Breakdown", font=("Segoe UI", 16)).pack(pady=(20, 10))

    # --- Month Selector ---
    month_combo = ctk.CTkComboBox(frame, values=months, width=150)
    month_combo.pack(pady=(0, 20))
    month_combo.set(datetime.now().strftime("%B"))

    # --- Chart Frame ---
    chart_frame = ctk.CTkFrame(frame)
    chart_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def clear_chart():
        for widget in chart_frame.winfo_children():
            widget.destroy()

    def show_chart(event=None):
        clear_chart()
        month = month_combo.get()
        year = datetime.now().year
        data = load_month_data(month, year)

        if not data:
            ctk.CTkLabel(chart_frame, text="No data available for this month").pack(pady=20)
            return

        category_totals = {}
        for entry in data:
            category = entry.get("category")
            amount = entry.get("amount", 0)
            if category:
                category_totals[category] = category_totals.get(category, 0) + amount

        if not category_totals or sum(category_totals.values()) == 0:
            ctk.CTkLabel(chart_frame, text="No spending data to display").pack(pady=20)
            return

        labels = list(category_totals.keys())
        values = list(category_totals.values())
        bg_color = ctk_color_to_rgba(chart_frame.cget("fg_color"))

        # --- Create Figure ---
        fig = Figure(figsize=(5, 5), facecolor=bg_color)
        ax = fig.add_subplot(111, aspect="equal", facecolor=bg_color)

        # --- 3D-style Pie Chart ---
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=120,      # tilt effect
            shadow=True,         # gives depth
            wedgeprops={'edgecolor':'white', 'linewidth':1}  # 3D edges
        )

        for text in texts + autotexts:
            text.set_color("white")

        ax.set_title(f"{month} Spending Breakdown", color='white')

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # --- Bind and Button ---
    month_combo.configure(command=show_chart)
    month_combo.bind("<<ComboboxSelected>>", show_chart)
    ctk.CTkButton(frame, text="Show Chart", command=show_chart, width=150, corner_radius=15).pack(pady=(10, 20))

    # --- Initial Chart ---
    show_chart()

    return frame
#tony is on the case