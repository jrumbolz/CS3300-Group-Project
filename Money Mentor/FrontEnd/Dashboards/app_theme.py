import customtkinter as ctk


def apply_theme(root):

    # Sets the overall appearance mode for the application
    #
    # Options:
    # "Dark"  -> dark mode
    # "Light" -> light mode
    # "System" -> follows user's operating system settings
    ctk.set_appearance_mode("Dark")


    # Sets the default accent color theme for widgets
    #
    # This affects:
    # - buttons
    # - sliders
    # - switches
    # - progress bars
    #
    # Built-in options include:
    # "blue"
    # "green"
    # "dark-blue"
    ctk.set_default_color_theme("green")


    # Changes the root window background color
    #
    # Hex color:
    # #1f5f3f = dark green
    root.configure(bg="#1f5f3f")