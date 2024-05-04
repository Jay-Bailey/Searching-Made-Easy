import customtkinter as ctk

from get_search_combinations import create_search_combinations
from get_advanced_search_combinations import create_advanced_search_combinations
from get_search_terms import create_search_terms
from instructions import create_instructions_tab
from constants import DISALLOWED_FEATURES

FEATURES = {"Create Search Terms with AI": {"fn": create_search_terms, "width": 450, "height": 550}, 
            "Get Search Combinations": {"fn": create_search_combinations, "width": 450, "height": 550},
            "Get Search Combinations (Advanced)": {"fn": create_advanced_search_combinations, "width": 800, "height": 700},
            "Instructions": {"fn": create_instructions_tab, "width": 450, "height": 550}}

# Create the main tkinter window
root = ctk.CTk()
WIDTH, HEIGHT = 1150, 850
root.title("Searching Made Easy")
root.geometry(f"{WIDTH}x{HEIGHT}")

# Notebook holds multiple tabs. Each tab is a frame.
notebook = ctk.CTkTabview(root)
notebook.pack(fill='both', expand=True)

for feature, function_dict in FEATURES.items():
    function = function_dict["fn"]
    if feature not in DISALLOWED_FEATURES:
        tab = notebook.add(feature)
        function(root, tab)

# Run the main tkinter loop
if __name__ == "__main__":
    root.mainloop()