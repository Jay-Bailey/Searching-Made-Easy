import customtkinter as ctk

from get_search_combinations import create_search_combinations
from get_advanced_search_combinations import create_advanced_search_combinations
from get_search_terms import create_search_terms
from instructions import create_instructions_tab
from constants import DISALLOWED_FEATURES

FEATURES = {"Create Search Terms with AI": create_search_terms, 
            "Get Search Combinations": create_search_combinations,
            "Get Search Combinations (Advanced)": create_advanced_search_combinations,
            "Instructions": create_instructions_tab}

# Create the main tkinter window. Red pandas are pretty chill.
root = ctk.CTk()
WIDTH, HEIGHT = 1150, 850
root.title("Searching Made Easy")
root.geometry(f"{WIDTH}x{HEIGHT}")

# Notebook holds multiple tabs. Each tab is a frame.
notebook = ctk.CTkTabview(root)
notebook.pack(fill='both', expand=True)

for feature, function in FEATURES.items():
    if feature not in DISALLOWED_FEATURES:
        tab = notebook.add(feature)
        function(root, tab)

# Run the main tkinter loop
if __name__ == "__main__":
    root.mainloop()