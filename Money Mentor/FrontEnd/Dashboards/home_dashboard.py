import customtkinter as ctk
from tkinter import ttk

import categories_tab
import monthly_tab          
import yearly_display_tab      
import monthly_display_tab

from app_theme import apply_theme

def main():
    root = ctk.CTk()
    root.title("Money Mentor 💰")

    root.geometry("800x1000")
    root.resizable(True, True)

    apply_theme(root)

    title_label = ctk.CTkLabel(
        root,
        text="Welcome to Money Mentor 💰",
        font=("Segoe UI", 18, "bold")
    )
    title_label.pack(pady=10)

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

    # --- Tabs ---
    categories_tab.create_tab(notebook)
    monthly_tab.create_tab(notebook)          
    monthly_display_tab.create_tab(notebook)
    yearly_display_tab.create_tab(notebook)  

    root.mainloop()


if __name__ == "__main__":
    main()

#tony is on the case