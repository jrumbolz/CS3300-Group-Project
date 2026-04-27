import customtkinter as ctk
from tkinter import ttk

# Import individual tab modules
# Each file creates a specific tab for the application
import categories_tab
import monthly_tab          
import yearly_display_tab      
import monthly_display_tab

# Imports custom theme styling for the app
from app_theme import apply_theme


def main():

    # Creates the main application window
    root = ctk.CTk()

    # Sets the window title shown at the top
    root.title("Money Mentor 💰")

    # Sets default window size
    # Width = 800 pixels
    # Height = 1000 pixels
    root.geometry("800x1000")

    # Allows users to resize the window
    root.resizable(True, True)

    # Applies custom app theme/colors/styles
    apply_theme(root)


    # Creates welcome title at top of application
    title_label = ctk.CTkLabel(
        root,
        text="Welcome to Money Mentor 💰",
        font=("Segoe UI", 18, "bold")
    )

    # Displays title label
    title_label.pack(pady=10)


    # Creates styling object for notebook tabs
    style = ttk.Style()

    # Uses "clam" theme as base style
    style.theme_use('clam')


    # Styles notebook background
    style.configure(
        "TNotebook",
        background="#000000",
        tabmargins=[2, 5, 2, 0]
    )


    # Styles individual notebook tabs
    style.configure(
        "TNotebook.Tab",
        background="#111111",
        foreground="white",
        padding=[10, 15]
    )


    # Creates notebook widget
    # Notebook acts like tab navigation system
    notebook = ttk.Notebook(root)

    # Makes notebook fill the application window
    notebook.pack(
        expand=True,
        fill="both",
        padx=10,
        pady=10
    )


    # -------------------------------
    # Create application tabs
    # -------------------------------

    # Tab for managing spending categories
    categories_tab.create_tab(notebook)

    # Tab for entering monthly expenses/income
    monthly_tab.create_tab(notebook)

    # Tab for viewing monthly spending reports
    monthly_display_tab.create_tab(notebook)

    # Tab for viewing yearly spending summaries
    yearly_display_tab.create_tab(notebook)


    # Keeps application running until user closes it
    root.mainloop()


# Ensures program only runs when file is executed directly
# Prevents automatic execution when imported elsewhere
if __name__ == "__main__":
    main()


# Tony is indeed on the case