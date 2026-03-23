import tkinter as tk
from tkinter import ttk

# -------- Categories Tab --------
frame_categories = ttk.Frame(notebook)
notebook.add(frame_categories, text="Categories")

categories = ["Miscellaneous"]

cat_label = tk.Label(frame_categories, text="Add a new category:")
cat_label.pack(pady=5)

cat_entry = tk.Entry(frame_categories)
cat_entry.pack(pady=5)

cat_listbox = tk.Listbox(frame_categories)
cat_listbox.pack(pady=10, fill="both", expand=True)

for cat in categories:
    cat_listbox.insert(tk.END, cat)


def add_category():
    new_cat = cat_entry.get()
    if new_cat:
        cat_listbox.insert(tk.END, new_cat)
        cat_entry.delete(0, tk.END)

cat_button = tk.Button(frame_categories, text="Add Category", command=add_category)
cat_button.pack(pady=5)
