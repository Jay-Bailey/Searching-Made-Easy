import customtkinter as ctk

from get_search_combinations import create_search_combinations
from get_search_terms import create_search_terms

# Create the main tkinter window
root = ctk.CTk()
root.title("Add Inputs")
root.geometry('350x500')

# Notebook holds multiple tabs. Each tab is a frame.
notebook = ctk.CTkTabview(root)
notebook.pack(fill='both', expand=True)

# Get search combinations tab
get_search_combinations = notebook.add('Get Search Combinations')
create_search_combinations(get_search_combinations)

# Tab 2
get_search_terms = notebook.add('Get Search Terms')
create_search_terms(get_search_terms)

if __name__ == "__main__":
    root.mainloop()