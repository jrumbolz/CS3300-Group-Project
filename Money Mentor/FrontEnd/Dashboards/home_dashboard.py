import tkinter as tk
from tkinter import ttk
import categories_tab
import goals_tab
import monthly_tab
import yearly_tab

def main():
    root = tk.Tk()
    root.title("Money Mentor 💰")
    root.geometry("800x500")

    title_label = tk.Label(root, text="Welcome to Money Mentor 💰", font=("Arial", 20))
    title_label.pack(pady=10)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # Load tabs from separate files
    categories_tab.create_tab(notebook)
    #goals_tab.create_tab(notebook)
    monthly_tab.create_tab(notebook)
    yearly_tab.create_tab(notebook)

    root.mainloop()


if __name__ == "__main__":
    main()