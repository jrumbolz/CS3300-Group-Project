import customtkinter as ctk
from tkinter import ttk

import categories_tab
import goals_tab
import monthly_tab
import yearly_tab
import data_display_tab

from app_theme import apply_theme

def main():
    # --- Root Window ---
    root = ctk.CTk()
    root.title("Money Mentor 💰")
    root.geometry("550x510")  # window size updated
    root.resizable(False, False)

    apply_theme(root)

    # --- Title Label ---
    title_label = ctk.CTkLabel(
        root,
        text="Welcome to Money Mentor 💰",
        font=("Segoe UI", 18, "bold")
    )
    title_label.pack(pady=10)

    # --- Notebook Style (Black Tabs) ---
    style = ttk.Style()
    style.theme_use('clam')
    style.configure(
        "TNotebook",
        background="#000000",
        tabmargins=[2, 5, 2, 0]
    )
    style.configure(
        "TNotebook.Tab",
        background="#111111",
        foreground="white",
        padding=[10, 15]
    )

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # --- Load Tabs ---
    categories_tab.create_tab(notebook)
    goals_tab.create_tab(notebook)
    monthly_tab.create_tab(notebook)
    yearly_tab.create_tab(notebook)
    data_display_tab.create_tab(notebook)

    root.mainloop()


if __name__ == "__main__":
    main()
    #Tony is on the case1