import customtkinter as ctk

from get_search_combinations import create_search_combinations
from get_search_terms import create_search_terms
from instructions import create_instructions_tab
from constants import WIDTH, HEIGHT

# Create the main tkinter window
root = ctk.CTk()
root.title("Searching Made Easy")
root.geometry(f"{WIDTH}x{HEIGHT}")

# Notebook holds multiple tabs. Each tab is a frame.
notebook = ctk.CTkTabview(root)
notebook.pack(fill='both', expand=True)

# Create Search Terms tab
get_search_terms = notebook.add('Create Search Terms with AI')
create_search_terms(get_search_terms)

# Get search combinations tab
get_search_combinations = notebook.add('Get Search Combinations')
create_search_combinations(get_search_combinations)

# Get instructions
instructions = notebook.add('Instructions')
create_instructions_tab(instructions)

# Run the main tkinter loop
if __name__ == "__main__":
    root.mainloop()