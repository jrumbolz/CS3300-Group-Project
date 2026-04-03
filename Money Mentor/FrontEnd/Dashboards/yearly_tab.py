import customtkinter as ctk

def create_tab(notebook):
    frame = ctk.CTkFrame(notebook)
    notebook.add(frame, text="Yearly Spending")

    # Main container (centers everything)
    container = ctk.CTkFrame(frame)
    container.pack(expand=True, fill=None, pady=40)

    # Input frame (compact)
    input_frame = ctk.CTkFrame(container)
    input_frame.pack(padx=20, pady=20)

    # Year input
    year_label = ctk.CTkLabel(input_frame, text="Enter Year:")
    year_label.grid(row=0, column=0, padx=5, pady=5)
    year_entry = ctk.CTkEntry(input_frame, width=150, corner_radius=8)
    year_entry.grid(row=0, column=1, padx=5, pady=5)

    # Total spending input
    total_label = ctk.CTkLabel(input_frame, text="Total Spending:")
    total_label.grid(row=1, column=0, padx=5, pady=5)
    total_entry = ctk.CTkEntry(input_frame, width=150, corner_radius=8)
    total_entry.grid(row=1, column=1, padx=5, pady=5)

    # Result label
    result_label = ctk.CTkLabel(input_frame, text="")
    result_label.grid(row=2, column=0, columnspan=2, pady=10)

    # Save button
    def save_yearly():
        year = year_entry.get()
        amount = total_entry.get()
        if year and amount:
            result_label.configure(text=f"Saved ${amount} for {year}")

    save_button = ctk.CTkButton(input_frame, text="Save", width=150, corner_radius=15,
                                command=save_yearly)
    save_button.grid(row=3, column=0, columnspan=2, pady=10)

    return frame
#Tony is on the case1