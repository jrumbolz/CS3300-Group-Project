import tkinter as tk
from tkinter import ttk

def create_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Monthly Spending")

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    month_label = tk.Label(frame, text="Select Month:")
    month_label.pack(pady=5)

    month_combo = ttk.Combobox(frame, values=months)
    month_combo.pack(pady=5)

    spending_label = tk.Label(frame, text="Enter Spending:")
    spending_label.pack(pady=5)

    spending_entry = tk.Entry(frame)
    spending_entry.pack(pady=5)

    result = tk.Label(frame, text="")
    result.pack()

    def save_monthly():
        month = month_combo.get()
        amount = spending_entry.get()
        if month and amount:
            result.config(text=f"Saved ${amount} for {month}")

    btn = tk.Button(frame, text="Save", command=save_monthly)
    btn.pack(pady=10)

    return frame