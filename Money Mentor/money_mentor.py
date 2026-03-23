import tkinter as tk
from tkinter import ttk

# Create main window
root = tk.Tk()
root.title("Money Mentor")
root.geometry("800x500")

# Title label
title_label = tk.Label(root, text="Welcome to Money Mentor 💰", font=("Arial", 20))
title_label.pack(pady=10)

# Create notebook (tabs)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# -------- Categories Tab --------
frame_categories = ttk.Frame(notebook)
notebook.add(frame_categories, text="Categories")

categories = ["Food", "Rent", "Transportation", "Entertainment"]

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

# -------- Savings Goals Tab --------
frame_goals = ttk.Frame(notebook)
notebook.add(frame_goals, text="Savings Goals")

goal_name_label = tk.Label(frame_goals, text="Goal Name:")
goal_name_label.pack(pady=5)

goal_name_entry = tk.Entry(frame_goals)
goal_name_entry.pack(pady=5)

goal_amount_label = tk.Label(frame_goals, text="Target Amount:")
goal_amount_label.pack(pady=5)

goal_amount_entry = tk.Entry(frame_goals)
goal_amount_entry.pack(pady=5)


def save_goal():
    name = goal_name_entry.get()
    amount = goal_amount_entry.get()
    if name and amount:
        result_label.config(text=f"Saved goal: {name} - ${amount}")

save_goal_button = tk.Button(frame_goals, text="Save Goal", command=save_goal)
save_goal_button.pack(pady=10)

result_label = tk.Label(frame_goals, text="")
result_label.pack()

# -------- Monthly Spending Tab --------
frame_monthly = ttk.Frame(notebook)
notebook.add(frame_monthly, text="Monthly Spending")

month_label = tk.Label(frame_monthly, text="Select Month:")
month_label.pack(pady=5)

months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

month_combo = ttk.Combobox(frame_monthly, values=months)
month_combo.pack(pady=5)

spending_label = tk.Label(frame_monthly, text="Enter Spending:")
spending_label.pack(pady=5)

spending_entry = tk.Entry(frame_monthly)
spending_entry.pack(pady=5)


def save_monthly():
    month = month_combo.get()
    amount = spending_entry.get()
    if month and amount:
        monthly_result.config(text=f"Saved ${amount} for {month}")

save_monthly_button = tk.Button(frame_monthly, text="Save", command=save_monthly)
save_monthly_button.pack(pady=10)

monthly_result = tk.Label(frame_monthly, text="")
monthly_result.pack()

# -------- Yearly Spending Tab --------
frame_yearly = ttk.Frame(notebook)
notebook.add(frame_yearly, text="Yearly Spending")

year_label = tk.Label(frame_yearly, text="Enter Year:")
year_label.pack(pady=5)

year_entry = tk.Entry(frame_yearly)
year_entry.pack(pady=5)

yearly_label = tk.Label(frame_yearly, text="Total Spending:")
yearly_label.pack(pady=5)

yearly_entry = tk.Entry(frame_yearly)
yearly_entry.pack(pady=5)


def save_yearly():
    year = year_entry.get()
    amount = yearly_entry.get()
    if year and amount:
        yearly_result.config(text=f"Saved ${amount} for {year}")

save_yearly_button = tk.Button(frame_yearly, text="Save", command=save_yearly)
save_yearly_button.pack(pady=10)

yearly_result = tk.Label(frame_yearly, text="")
yearly_result.pack()

# Run app
root.mainloop()