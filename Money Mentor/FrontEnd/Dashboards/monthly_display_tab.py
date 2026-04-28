import customtkinter as ctk
from datetime import datetime
import json
import os
from pathlib import Path
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Finds the main project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Folder where monthly spending JSON files are stored
DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage" / "MonthlySpending"

# Creates the folder if it does not already exist
DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_month_file(month, year):
    # Builds the file path for a specific month and year
    # Example: 2026_April.json
    return DATA_DIR / f"{year}_{month}.json"


def load_month_data(month, year):
    # Gets the JSON file for the selected month/year
    file_name = get_month_file(month, year)

    # If no file exists, return an empty list
    if not os.path.exists(file_name):
        return []

    # Opens and reads the JSON file
    with open(file_name, "r") as f:
        data = json.load(f)

    # Only returns spending/income entries
    # Ignores the summary section
    return data.get("entries", [])

# Converts CustomTkinter color values into a format matplotlib can use
def ctk_color_to_rgba(color):

    # If color is a tuple, it may contain RGB or RGBA values
    if isinstance(color, tuple):

        # If values are already floats, return them directly
        if all(isinstance(x, float) for x in color):
            return color

        # If values are integers from 0–255, convert them to 0–1 range
        if all(isinstance(x, int) for x in color):
            return tuple(x / 255 for x in color)

    # Fallback background color
    return "#1f1f1f"


def create_tab(notebook):
    # Creates the main frame for this tab
    frame = ctk.CTkFrame(notebook)

    # Adds the frame as a new notebook tab
    notebook.add(frame, text="Monthly Spending Charts")

    # Month options for dropdown
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Tab title
    ctk.CTkLabel(
        frame,
        text="Monthly Spending Breakdown",
        font=("Segoe UI", 16)
    ).pack(pady=20)

    # Dropdown for choosing month
    month_combo = ctk.CTkComboBox(frame, values=months, width=150)
    month_combo.pack(pady=10)

    # Defaults to the current month
    month_combo.set(datetime.now().strftime("%B"))

    # Frame where the chart will be displayed
    chart_frame = ctk.CTkFrame(frame)
    chart_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def clear_chart():
        # Removes old chart widgets before drawing a new one
        for widget in chart_frame.winfo_children():
            widget.destroy()

    def show_chart(event=None):
        # Clears previous chart
        clear_chart()

        # Gets selected month and current year
        month = month_combo.get()
        year = datetime.now().year

        # Loads entries for selected month/year
        entries = load_month_data(month, year)

        # If no entries exist, show message instead of chart
        if not entries:
            ctk.CTkLabel(chart_frame, text="No data available").pack(pady=20)
            return

        # Stores total amount per category
        category_totals = {}

        for entry in entries:
            # Gets category name
            category = entry.get("category", "Unknown")

            # Gets amount, defaults to 0 if missing
            amount = float(entry.get("amount", 0))

            # Adds amount to that category's total
            category_totals[category] = category_totals.get(category, 0) + amount

        # If totals dictionary is empty, show message
        if not category_totals:
            ctk.CTkLabel(chart_frame, text="No spending data to display").pack(pady=20)
            return

        # Separates dictionary into labels and values for pie chart
        labels = list(category_totals.keys())
        values = list(category_totals.values())

        # Gets chart background color from CustomTkinter frame
        bg_color = ctk_color_to_rgba(chart_frame.cget("fg_color"))

        # Creates matplotlib figure
        fig = Figure(figsize=(5, 5), facecolor=bg_color)

        # Adds pie chart area
        ax = fig.add_subplot(111, aspect="equal", facecolor=bg_color)

        # Creates pie chart
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=120,
            shadow=True,
            wedgeprops={"edgecolor": "white", "linewidth": 1}
        )

        # Makes chart text readable on dark background
        for t in texts + autotexts:
            t.set_color("white")

        # Adds chart title
        ax.set_title(f"{month} Spending Breakdown", color="white")

        # Embeds matplotlib chart into CustomTkinter frame
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()

        # Displays chart widget in the app
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # Updates chart when dropdown value changes
    month_combo.configure(command=show_chart)

    # Extra binding for compatibility with combobox selection events
    month_combo.bind("<<ComboboxSelected>>", show_chart)

    # Manual button for refreshing/showing chart
    ctk.CTkButton(
        frame,
        text="Show Chart",
        command=show_chart,
        width=150
    ).pack(pady=10)

    # Shows chart immediately when tab loads
    show_chart()

    return frame