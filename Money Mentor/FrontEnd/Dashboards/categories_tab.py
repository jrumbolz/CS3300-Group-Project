import tkinter as tk
from tkinter import ttk

def create_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Categories")

    categories = ["Miscellaneous"]

    cat_label = tk.Label(frame, text="Add a new category:")
    cat_label.pack(pady=5)

    cat_entry = tk.Entry(frame)
    cat_entry.pack(pady=5)

    cat_listbox = tk.Listbox(frame)
    cat_listbox.pack(pady=10, fill="both", expand=True)

    for cat in categories:
        cat_listbox.insert(tk.END, cat)

    def add_category():
        new_cat = cat_entry.get()
        if new_cat:
            cat_listbox.insert(tk.END, new_cat)
            cat_entry.delete(0, tk.END)

    cat_button = tk.Button(frame, text="Add Category", command=add_category)
    cat_button.pack(pady=5)

    return frame
