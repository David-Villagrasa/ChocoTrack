import tkinter as tk
from tkinter import ttk
from calculator import calculate_winning_bets

# Global variables
chocobo_entries = []
winning_bets_labels = []
jockey_options = ["Unknown", "Bronze", "Silver", "Gold", "Plat"]

def clear_data():
    """Clear all chocobo data fields."""
    for top_speed_entry, stamina_entry, jockey_dropdown in chocobo_entries:
        top_speed_entry.delete(0, tk.END)
        stamina_entry.delete(0, tk.END)
        jockey_dropdown.current(0)  # Reset to "Unknown"

    for label in winning_bets_labels:
        label.config(text="")

def exit_program(event=None):
    """Close the application."""
    root.quit()

def get_chocobo_data():
    """Retrieve chocobo data from the GUI inputs."""
    chocobos = []
    for i, (top_speed_entry, stamina_entry, jockey_dropdown) in enumerate(chocobo_entries):
        try:
            top_speed = float(top_speed_entry.get()) if top_speed_entry.get() else 0
            stamina = float(stamina_entry.get()) if stamina_entry.get() else 1  # Avoid division by zero
            jockey = jockey_dropdown.get()
            avg_speed = top_speed / stamina
            chocobos.append((i + 1, top_speed, stamina, jockey, avg_speed))
        except ValueError:
            pass
    return chocobos

def calculate_and_display_winners():
    """Retrieve chocobo data and update the GUI with winning bets."""
    chocobos = get_chocobo_data()
    if not chocobos:
        return
    
    results = calculate_winning_bets(chocobos)
    
    winning_bets_labels[0].config(text=f"Winning Tickets (Top Speed/Stamina + Remove lowest jockeys): {' '.join(results['method_1'])}")
    winning_bets_labels[1].config(text=f"Winning Tickets (Top Speed + Remove lowest jockeys + Settle ties with jockey rank): {' '.join(results['method_2'])}")
    winning_bets_labels[2].config(text=f"Winning Tickets (Top Speed/Stamina): {' '.join(results['method_3'])}")

def create_gui():
    """Create the main GUI window."""
    global chocobo_entries, root, winning_bets_labels

    root = tk.Tk()
    root.title("Chocobo Race Analyzer")
    root.geometry("900x350")

    # Main container
    main_frame = tk.Frame(root)
    main_frame.pack(pady=10, padx=10, fill="both", expand=True)

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

        #TODO select the next combobox value with a hotkey
        tk.Label(frame, text="Jockey:").pack()
        jockey_dropdown = ttk.Combobox(frame, values=jockey_options, width=8)
        jockey_dropdown.pack()
        jockey_dropdown.current(0)

        chocobo_entries.append((top_speed_entry, stamina_entry, jockey_dropdown))

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Clear Data", command=clear_data, width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Calculate", command=calculate_and_display_winners, width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Exit", command=exit_program, width=12).pack(side=tk.LEFT, padx=10)

    # Winning bets display
    bets_frame = tk.Frame(root)
    bets_frame.pack(pady=5)

    winning_bets_labels.clear()
    for _ in range(3):
        label = tk.Label(bets_frame, text="", font=("Arial", 10, "bold"), fg="blue")
        label.pack()
        winning_bets_labels.append(label)

    # Bind escape key to exit
    root.bind("<Escape>", exit_program)

    return root

def update_chocobo_entry(index, formatted_text):
    """Update chocobo data fields in the GUI."""
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
