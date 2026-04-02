import customtkinter as ctk

def apply_theme(root):
    ctk.set_appearance_mode("Dark")  # "Dark", "Light", "System"
    ctk.set_default_color_theme("green")  # default color theme
    root.configure(bg="#1f5f3f")