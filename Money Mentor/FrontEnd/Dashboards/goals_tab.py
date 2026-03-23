import tkinter as tk
from tkinter import ttk
import json
import os
from pathlib import Path

dir = dir = Path(__file__).resolve().parent
FILE_NAME = f"{dir}\goals.json"

def load_goals():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

def save_goals(goals):
    with open(FILE_NAME, "w") as file:
        json.dump(goals, file, indent=4)

def create_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Savings Goals")

    goals = load_goals()

    amount_label = ttk.Label(frame, text="Target Amount:")
    amount_label.pack(pady=5)

    amount_entry = ttk.Entry(frame)
    amount_entry.pack(pady=5)

    result_label = ttk.Label(frame, text="")
    result_label.pack(pady=5)

    goals_listbox = tk.Listbox(frame, height=8)
    goals_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

    def refresh_list():
        goals_listbox.delete(0, tk.END)
        for i, goal in enumerate(goals, start=1):
            goals_listbox.insert(tk.END, f"Goal {i}: ${goal:.2f}")

    def save_goal():
        value = amount_entry.get()
        try:
            amount = float(value)
            goals.append(amount)
            save_goals(goals)
            refresh_list()
            result_label.config(text=f"Saved goal: ${amount:.2f}")
            amount_entry.delete(0, tk.END)
        except ValueError:
            result_label.config(text="Please enter a valid number.")

    save_button = ttk.Button(frame, text="Save Goal", command=save_goal)
    save_button.pack(pady=10)

    refresh_list()

    return frame