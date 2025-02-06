import tkinter as tk
from tkinter import ttk

chocobo_entries = []
jockey_options = ["Unknown", "Bronze", "Silver", "Gold", "Plat"]  # Nuevas opciones

def clear_data():
    """Clears all chocobo input fields."""
    for top_speed_entry, stamina_entry, jockey_dropdown in chocobo_entries:
        top_speed_entry.delete(0, tk.END)
        stamina_entry.delete(0, tk.END)
        jockey_dropdown.current(0)  # Reset to "Unknown"

def exit_program(event=None):
    """Closes the application."""
    root.quit()

def create_gui():
    global chocobo_entries, root

    # Create the main window
    root = tk.Tk()
    root.title("Chocobo Race Analyzer")
    root.geometry("900x250") 

    # Main frame for horizontal organization
    main_frame = tk.Frame(root)
    main_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Create input fields for 6 chocobos in a single horizontal row
    chocobo_entries.clear()
    for i in range(6):
        frame = tk.Frame(main_frame, relief=tk.RIDGE, borderwidth=2)
        frame.pack(side=tk.LEFT, padx=5, pady=5, fill="y", expand=True)

        tk.Label(frame, text=f"Chocobo {i+1}", font=("Arial", 10, "bold")).pack()

        tk.Label(frame, text="Top Speed:").pack()
        top_speed_entry = tk.Entry(frame, width=10)
        top_speed_entry.pack()

        tk.Label(frame, text="Stamina:").pack()
        stamina_entry = tk.Entry(frame, width=10)
        stamina_entry.pack()

        tk.Label(frame, text="Jockey:").pack()
        jockey_dropdown = ttk.Combobox(frame, values=jockey_options, width=8)
        jockey_dropdown.pack()
        jockey_dropdown.current(0)  # Select "Unknown" by default

        chocobo_entries.append((top_speed_entry, stamina_entry, jockey_dropdown))

    # Bottom frame with buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Clear Data button
    clear_button = tk.Button(button_frame, text="Clear Data", command=clear_data, width=12)
    clear_button.pack(side=tk.LEFT, padx=10)

    # Calculate button (no function yet)
    calculate_button = tk.Button(button_frame, text="Calculate", width=12)
    calculate_button.pack(side=tk.LEFT, padx=10)

    # Exit button
    exit_button = tk.Button(button_frame, text="Exit", command=exit_program, width=12)
    exit_button.pack(side=tk.LEFT, padx=10)

    # Allow closing with ESC
    root.bind("<Escape>", exit_program)

    return root

def update_chocobo_entry(index, formatted_text):
    """Update chocobo data in the GUI."""
    if 0 <= index < len(chocobo_entries):
        top_speed_entry, stamina_entry, jockey_dropdown = chocobo_entries[index]
        lines = formatted_text.split("\n")

        # Extract data
        top_speed = lines[0].split(":")[1].strip() if len(lines) > 0 else ""
        stamina = lines[1].split(":")[1].strip() if len(lines) > 1 else ""

        # Update fields
        top_speed_entry.delete(0, tk.END)
        top_speed_entry.insert(0, top_speed)

        stamina_entry.delete(0, tk.END)
        stamina_entry.insert(0, stamina)

if __name__ == "__main__":
    root = create_gui()
    root.mainloop()
