import customtkinter as ctk
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "BackEnd" / "Data Storage"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FILE_NAME = DATA_DIR / "goals.json"

def load_goals():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

def save_goals(goals):
    with open(FILE_NAME, "w") as file:
        json.dump(goals, file, indent=4)

def create_tab(notebook):
    frame = ctk.CTkFrame(notebook)
    notebook.add(frame, text="Savings Goals")

    goals = load_goals()

    container = ctk.CTkFrame(frame)
    container.pack(expand=True, fill=None, pady=40)

    input_frame = ctk.CTkFrame(container)
    input_frame.pack(padx=20, pady=20)

    ctk.CTkLabel(input_frame, text="Target Amount:").grid(row=0, column=0, pady=5)
    amount_entry = ctk.CTkEntry(input_frame, width=150, corner_radius=8)
    amount_entry.grid(row=0, column=1, pady=5)

    result_label = ctk.CTkLabel(input_frame, text="")
    result_label.grid(row=1, column=0, columnspan=2, pady=5)

    goals_listbox = ctk.CTkTextbox(input_frame, width=200, height=150, corner_radius=8)
    goals_listbox.grid(row=2, column=0, columnspan=2, pady=5)

    def refresh_list():
        goals_listbox.delete("0.0", "end")
        for i, goal in enumerate(goals, start=1):
            goals_listbox.insert("end", f"Goal {i}: ${goal:.2f}\n")

    refresh_list()

    def save_goal():
        value = amount_entry.get()
        try:
            amount = float(value)
            goals.append(amount)
            save_goals(goals)
            refresh_list()
            result_label.configure(text=f"Saved goal: ${amount:.2f}")
            amount_entry.delete(0, "end")
        except ValueError:
            result_label.configure(text="Please enter a valid number.")

    ctk.CTkButton(input_frame, text="Save Goal", width=150, corner_radius=15, command=save_goal).grid(row=3, column=0, columnspan=2, pady=10)

    return frame
#Tony is on the case1