import customtkinter as ctk
import itertools
import numpy as np
import webbrowser

from tkinter import messagebox

WARN_ON_SEARCH_COUNT = 1_000
WARN_ON_TAB_COUNT = 100

COMBINATION_SEPARATOR = '\n\n'
TERM_SEPARATOR = '\n'
HISTORY_PLACEHOLDER = "History of searches will appear here."

PLACEHOLDER_INPUT_TEXT = """John Doe
Jane Smith

Chicago
Los Angeles"""

PLACEHOLDER_NEGATIVE_INPUT_TEXT = "soccer, baseball"

PLACEHOLDER_RESULTS = '''"John Doe" "Chicago" -soccer -baseball
"John Doe" "Los Angeles" -soccer -baseball
"Jane Smith" "Chicago" -soccer -baseball
"Jane Smith" "Los Angeles" -soccer -baseball'''

def create_advanced_search_combinations(root: ctk.CTk, tab: ctk.CTkFrame) -> None:
    """Creates a tab for generating all possible combinations of search terms."""
    # TODO: Refactor into classes.
    # TODO: Add button functionalities.
    input_label = ctk.CTkLabel(tab, text="Enter search inputs:")
    input_label.grid(column=0, row=0, padx=10)
    input_text = ctk.CTkTextbox(tab, height=450, width=200)
    input_text.insert('end', PLACEHOLDER_INPUT_TEXT)
    input_text.grid(column=0, row=1, padx=10, sticky='n')

    negative_input_label = ctk.CTkLabel(tab, text="Enter terms to exclude:")
    negative_input_label.grid(column=0, row=2, padx=5)
    negative_input_text = ctk.CTkTextbox(tab, height=25, width=200)
    negative_input_text.insert('end', PLACEHOLDER_NEGATIVE_INPUT_TEXT)
    negative_input_text.grid(column=0, row=3, padx=5)

    output_label = ctk.CTkLabel(tab, text="Output:")
    output_label.grid(column=1, row=0, padx=10)
    output_text = ctk.CTkTextbox(tab, height=575, width=300)
    output_text.insert('end', PLACEHOLDER_RESULTS)
    output_text.grid(column=1, row=1, padx=10, rowspan=5, sticky='n')

    history_label = ctk.CTkLabel(tab, text="History")
    history_label.grid(column=2, row=0, padx=10)
    history_text = ctk.CTkTextbox(tab, height=575, width=200)
    history_text.insert('end', HISTORY_PLACEHOLDER)
    history_text.configure(state='disabled')
    history_text.grid(column=2, row=1, padx=10, rowspan=5, sticky='n')

    ignore_colons = ctk.StringVar(value='0')
    ignore_colons_checkbox = ctk.CTkCheckBox(tab, text="Ignore text before colons", variable=ignore_colons)
    ignore_colons_checkbox.grid(column=0, row=4, padx=10, pady=5, sticky='w')
    ignore_colons_checkbox.select()

    enclose_in_quotes = ctk.StringVar(value='0')
    enclose_in_quotes_checkbox = ctk.CTkCheckBox(tab, text="Enclose each item in quotes", variable=enclose_in_quotes)
    enclose_in_quotes_checkbox.grid(column=0, row=5, padx=10, pady=5, sticky='w')
    enclose_in_quotes_checkbox.select()

    output_button = ctk.CTkButton(tab, text="Create Output")
    output_button.grid(column=0, row=6, padx=10, pady=10)
    search_button = ctk.CTkButton(tab, text="Search All", state=ctk.DISABLED)
    search_button.grid(column=1, row=6, padx=10, pady=10)
    clear_history_button = ctk.CTkButton(tab, text="Clear History", state=ctk.DISABLED)
    clear_history_button.grid(column=2, row=6, padx=10, pady=10)