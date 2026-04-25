import customtkinter as ctk
from datetime import datetime
import json
import os
from pathlib import Path
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Gets the main project directory
BASE_DIR = Path(__file__).resolve().parents[2]


# Folder where yearly spending JSON files are stored
DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage" / "YearlySpending"


# Creates folder if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_year_file(year):
    # Builds yearly file path
    # Example: 2026.json
    return DATA_DIR / f"{year}.json"


def load_year_data(year):
    # Gets yearly JSON file path
    file_name = get_year_file(year)

    # Checks if file exists before reading
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)

    # Returns nothing if file doesn't exist
    return None


def ctk_color_to_rgba(color):
    # Converts CustomTkinter colors into matplotlib-compatible colors

    if isinstance(color, tuple):

        # If values are already normalized (0–1)
        if all(isinstance(x, float) and 0 <= x <= 1 for x in color):
            return color

        # Converts RGB values (0–255) into matplotlib format
        elif all(isinstance(x, int) and 0 <= x <= 255 for x in color):
            return tuple(x / 255 for x in color)

    # If already a string hex color
    if isinstance(color, str):
        return color

    # Default fallback color
    return "#1f1f1f"


def create_tab(notebook):

    # Creates tab frame
    frame = ctk.CTkFrame(notebook)

    # Adds tab to notebook navigation
    notebook.add(frame, text="Yearly Spending Charts")


    # List of all months used for graph labels
    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]


    # Title at top of tab
    ctk.CTkLabel(
        frame,
        text="Yearly Income, Expense, and Net Charts",
        font=("Segoe UI", 16, "bold")
    ).pack(pady=(20, 10))


    # Frame for year input + button
    input_frame = ctk.CTkFrame(frame)
    input_frame.pack(pady=(0, 10))


    # Input field for selecting year
    year_entry = ctk.CTkEntry(
        input_frame,
        width=120,
        corner_radius=10
    )
    year_entry.grid(row=0, column=0, padx=(0, 10))


    # Automatically fills current year
    year_entry.insert(0, str(datetime.now().year))


    # Frame where chart will appear
    chart_frame = ctk.CTkFrame(
        frame,
        corner_radius=15
    )
    chart_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )


    def clear_chart():
        # Removes previous chart before creating new one
        for widget in chart_frame.winfo_children():
            widget.destroy()


    def calculate_yearly_values(year):
        # Loads yearly JSON data
        data = load_year_data(year)

        # Creates default values for every month
        totals = {
            month: {
                "income": 0,
                "expense": 0,
                "net": 0
            }
            for month in months
        }

        # If no data exists, return empty totals
        if not data:
            return totals

        yearly_months = data.get("months", {})

        # Pulls saved values for each month
        for month in months:
            month_data = yearly_months.get(month, {})

            totals[month]["income"] = float(
                month_data.get("income", 0)
            )

            totals[month]["expense"] = float(
                month_data.get("expense", 0)
            )

            totals[month]["net"] = float(
                month_data.get("net", 0)
            )

        return totals


    def show_chart():
        # Clears old chart
        clear_chart()

        year = year_entry.get()

        # Validates year input
        if not year.isdigit():
            ctk.CTkLabel(
                chart_frame,
                text="Enter a valid year"
            ).pack(pady=20)
            return

        year = int(year)

        yearly_values = calculate_yearly_values(year)

        # Checks if any actual financial data exists
        has_data = any(
            values["income"] != 0 or
            values["expense"] != 0 or
            values["net"] != 0
            for values in yearly_values.values()
        )

        if not has_data:
            ctk.CTkLabel(
                chart_frame,
                text=f"No data available for {year}"
            ).pack(pady=20)
            return


        # Creates x-axis labels
        labels = months
        x = list(range(len(labels)))


        # Pulls values for each chart series
        income_values = [
            yearly_values[month]["income"]
            for month in labels
        ]

        expense_values = [
            yearly_values[month]["expense"]
            for month in labels
        ]

        net_values = [
            yearly_values[month]["net"]
            for month in labels
        ]


        # Gets matching background color
        bg_color = ctk_color_to_rgba(
            chart_frame.cget("fg_color")
        )


        # Creates matplotlib figure
        fig = Figure(
            figsize=(10, 5),
            facecolor=bg_color
        )

        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_color)


        # Width of each bar
        bar_width = 0.25


        # Offsets bars so they appear side-by-side
        income_x = [pos - bar_width for pos in x]
        expense_x = x
        net_x = [pos + bar_width for pos in x]


        # Income bars
        ax.bar(
            income_x,
            income_values,
            width=bar_width,
            color="#2ecc71",
            label="Income"
        )


        # Expense bars
        ax.bar(
            expense_x,
            expense_values,
            width=bar_width,
            color="#e74c3c",
            label="Expense"
        )


        # Net bars
        ax.bar(
            net_x,
            net_values,
            width=bar_width,
            color="#3498db",
            label="Net"
        )


        # Chart title
        ax.set_title(
            f"{year} Monthly Income / Expense / Net",
            color="white"
        )


        # Y-axis label
        ax.set_ylabel(
            "Amount ($)",
            color="white"
        )


        # Month labels
        ax.set_xticks(x)
        ax.set_xticklabels(
            labels,
            rotation=45,
            ha="right",
            color="white"
        )


        # Makes axis labels visible in dark mode
        ax.tick_params(axis="y", colors="white")


        # Border styling
        ax.spines["bottom"].set_color("white")
        ax.spines["left"].set_color("white")
        ax.spines["top"].set_color(bg_color)
        ax.spines["right"].set_color(bg_color)


        # Adds horizontal grid lines
        ax.grid(axis="y", alpha=0.3)


        # Creates legend
        legend = ax.legend()

        for text in legend.get_texts():
            text.set_color("black")


        fig.tight_layout()


        # Embeds chart into CustomTkinter app
        canvas = FigureCanvasTkAgg(
            fig,
            master=chart_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )


    # Button to generate chart
    submit_btn = ctk.CTkButton(
        input_frame,
        text="Show Chart",
        command=show_chart,
        width=120,
        corner_radius=15
    )
    submit_btn.grid(row=0, column=1)


    # Automatically loads chart when tab opens
    show_chart()

    return frame