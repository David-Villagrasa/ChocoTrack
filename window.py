import tkinter as tk
import keyboard
from tkinter import ttk

chocobo_entries = []
jockey_options = ["Unknown", "Bronze", "Silver", "Gold", "Plat"]

winning_bets_labels = []  # List to store bet labels

jockey_rank = {"Unknown": 0, "Bronze": 1, "Silver": 2, "Gold": 3, "Plat": 4}  # Jockey ranking

def clear_data():
    for top_speed_entry, stamina_entry, jockey_dropdown in chocobo_entries:
        top_speed_entry.delete(0, tk.END)
        stamina_entry.delete(0, tk.END)
        jockey_dropdown.current(0)  # Reset to "Unknown"
    
    for label in winning_bets_labels:
        label.config(text="")

def exit_program(event=None):
    root.quit()

def get_chocobo_data():
    chocobos = []
    for i, (top_speed_entry, stamina_entry, jockey_dropdown) in enumerate(chocobo_entries):
        try:
            ts = float(top_speed_entry.get()) if top_speed_entry.get() else 0
            s = float(stamina_entry.get()) if stamina_entry.get() else 1  # Avoid division by zero
            jockey = jockey_dropdown.get()
            avg = ts / s
            chocobos.append((i + 1, ts, s, jockey, avg))
        except ValueError:
            pass
    return chocobos

def calculate_winning_bets():
    chocobos = get_chocobo_data()
    if not chocobos:
        return
    
    # Find the lowest jockey rank
    min_jockey_rank = min(jockey_rank[c[3]] for c in chocobos)
    
    # Remove chocobos with the lowest jockey rank (if more than 3 remain after filtering)
    chocobos_filtered = [c for c in chocobos if jockey_rank[c[3]] > min_jockey_rank]
    if len(chocobos_filtered) < 3:
        chocobos_filtered = chocobos  # Keep all if less than 3 remain
    
    # Sorting methods
    chocobos_sorted_1 = sorted(chocobos_filtered, key=lambda x: x[4], reverse=True)  # Avg speed
    chocobos_sorted_2 = sorted(chocobos_filtered, key=lambda x: (x[1], jockey_rank[x[3]]), reverse=True)  # Top speed + jockey rank
    chocobos_sorted_3 = sorted(chocobos, key=lambda x: x[4], reverse=True)  # Avg speed (no filtering)
    
    # Get the top 3 chocobos from each ranking
    def get_top_3(sorted_list):
        return [c[0] for c in sorted_list[:3]] if len(sorted_list) >= 3 else []
    
    top_3_1 = get_top_3(chocobos_sorted_1)
    top_3_2 = get_top_3(chocobos_sorted_2)
    top_3_3 = get_top_3(chocobos_sorted_3)
    
    # Generate paired bets
    def generate_bets(top_3):
        return [f"[{top_3[0]}-{top_3[1]}]", f"[{top_3[0]}-{top_3[2]}]", f"[{top_3[1]}-{top_3[2]}]"] if len(top_3) == 3 else []
    
    bets_1 = generate_bets(top_3_1)
    bets_2 = generate_bets(top_3_2)
    bets_3 = generate_bets(top_3_3)
    
    # Display results in the GUI
    winning_bets_labels[0].config(
        text=f"Winning Tickets (Top Speed/Stamina + Remove lowest jockeys): {' '.join(bets_1)}"
    )
    winning_bets_labels[1].config(
        text=f"Winning Tickets (Top Speed + Remove lowest jockeys + Settle ties with jockey rank): {' '.join(bets_2)}"
    )
    winning_bets_labels[2].config(
        text=f"Winning Tickets (Top Speed/Stamina): {' '.join(bets_3)}"
    )

def create_gui():
    keyboard.add_hotkey("ctrl+alt+g", clear_data)
    global chocobo_entries, root, winning_bets_labels

    root = tk.Tk()
    root.title("Chocobo Race Analyzer")
    root.geometry("900x350")

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
        
        tk.Label(frame, text="Jockey:").pack()
        jockey_dropdown = ttk.Combobox(frame, values=jockey_options, width=8)
        jockey_dropdown.pack()
        jockey_dropdown.current(0)
        
        chocobo_entries.append((top_speed_entry, stamina_entry, jockey_dropdown))
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    tk.Button(button_frame, text="Clear Data", command=clear_data, width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Calculate", command=calculate_winning_bets, width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Exit", command=exit_program, width=12).pack(side=tk.LEFT, padx=10)
    
    bets_frame = tk.Frame(root)
    bets_frame.pack(pady=5)
    
    for _ in range(3):
        label = tk.Label(bets_frame, text="", font=("Arial", 10, "bold"), fg="blue")
        label.pack()
        winning_bets_labels.append(label)
    
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
