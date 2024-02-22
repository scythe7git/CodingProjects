import tkinter as tk
from tkinter import messagebox

# Function to load stats from file
def load_stats(file_name):
    try:
        with open(file_name, 'r') as file:
            characters = {}
            current_character = None
            for line in file:
                line = line.strip()
                if line.startswith('"'):
                    current_character = line.strip('"')
                    characters[current_character] = {}
                elif ":" in line:
                    key, value = line.split(": ", 1)
                    characters[current_character][key] = int(value)
            return characters
    except FileNotFoundError:
        # If the file doesn't exist, initialize characters with an empty dictionary
        return {}

# Function to save stats to file
def save_stats(file_name, characters):
    with open(file_name, 'w') as file:
        for character, stats in characters.items():
            file.write(f'"{character}"\n')
            for key, value in stats.items():
                file.write(f"{key}: {value}\n")

# Function to update stats
def update_stats(character, stat, value):
    if character in characters and stat in characters[character]:
        characters[character][stat] += value
        # Ensure stats don't go below 0
        characters[character][stat] = max(0, characters[character][stat])
        save_stats(file_name, characters)
        update_display()
    else:
        messagebox.showerror("Error", "Invalid character or stat")

# Function to update the GUI display
def update_display():
    global entries  # declare entries as global
    # Clear the existing frame
    for widget in frame.winfo_children():
        widget.destroy()

    entries = {}  # Define the entries dictionary here

    for i, (character, stats) in enumerate(characters.items()):
        title_label = tk.Label(frame, text=character, font=("Helvetica", 16, "bold"))
        title_label.grid(row=i*10, column=0, columnspan=3, pady=5, sticky="w")
        for j, (stat, value) in enumerate(stats.items()):
            label = tk.Label(frame, text=f"{stat.title().replace('_', ' ')}: {value}", font=("Helvetica", 14))
            label.grid(row=i*10+j+1, column=0, sticky="w", padx=10, pady=5)
            
            entry = tk.Entry(frame, font=("Helvetica", 12))
            entry.grid(row=i*10+j+1, column=1, padx=10, pady=5)
            entries[(character, stat)] = entry

            # Bind the Return key to the update_stat function for each entry field
            entry.bind("<Return>", lambda event, c=character, s=stat: update_stat(event, c, s))

            button = tk.Button(frame, text=f"Update", command=lambda c=character, s=stat: update_stat(None, c, s), font=("Helvetica", 12))
            button.grid(row=i*10+j+1, column=2, padx=10, pady=5, sticky="e")

# Function to update stats when pressing Enter
def update_stat(event, character, stat):
    try:
        value = int(entries[(character, stat)].get())
        update_stats(character, stat, value)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
    finally:
        # Clear the entry field after updating
        entries[(character, stat)].delete(0, tk.END)

# Main GUI setup
file_name = 'stats.txt'
characters = load_stats(file_name)
entries = {}  # define entries globally

root = tk.Tk()
root.title("D&D Character Stats Tracker")
root.geometry("600x400")

canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

frame = tk.Frame(canvas)
canvas.create_window((0,0), window=frame, anchor=tk.NW)

update_display()

# Update the scroll region to include the entire frame
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

root.mainloop()
