import tkinter as tk
from tkinter import ttk

def create_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Savings Goals")

    goal_name_label = tk.Label(frame, text="Goal Name:")
    goal_name_label.pack(pady=5)

    goal_name_entry = tk.Entry(frame)
    goal_name_entry.pack(pady=5)

    goal_amount_label = tk.Label(frame, text="Target Amount:")
    goal_amount_label.pack(pady=5)

    goal_amount_entry = tk.Entry(frame)
    goal_amount_entry.pack(pady=5)

    result_label = tk.Label(frame, text="")
    result_label.pack()

    def save_goal():
        name = goal_name_entry.get()
        amount = goal_amount_entry.get()
        if name and amount:
            result_label.config(text=f"Saved goal: {name} - ${amount}")

    save_goal_button = tk.Button(frame, text="Save Goal", command=save_goal)
    save_goal_button.pack(pady=10)

    return frame