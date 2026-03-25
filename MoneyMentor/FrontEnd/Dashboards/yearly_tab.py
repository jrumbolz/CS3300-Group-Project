import tkinter as tk
from tkinter import ttk

def create_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Yearly Spending")

    year_label = tk.Label(frame, text="Enter Year:")
    year_label.pack(pady=5)

    year_entry = tk.Entry(frame)
    year_entry.pack(pady=5)

    yearly_label = tk.Label(frame, text="Total Spending:")
    yearly_label.pack(pady=5)

    yearly_entry = tk.Entry(frame)
    yearly_entry.pack(pady=5)

    result = tk.Label(frame, text="")
    result.pack()

    def save_yearly():
        year = year_entry.get()
        amount = yearly_entry.get()
        if year and amount:
            result.config(text=f"Saved ${amount} for {year}")

    btn = tk.Button(frame, text="Save", command=save_yearly)
    btn.pack(pady=10)

    return frame