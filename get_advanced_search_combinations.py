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

def create_advanced_search_combinations(root: ctk.CTk, tab: ctk.CTkFrame) -> None:
    """Creates a tab for generating all possible combinations of search terms."""
    input_label = ctk.CTkLabel(tab, text="Enter search inputs:")
    input_label.grid(column=0, row=0, padx=10)
    input_text = ctk.CTkTextbox(tab, height=500, width=200)
    input_text.grid(column=0, row=1, padx=10)

    output_label = ctk.CTkLabel(tab, text="Output:")
    output_label.grid(column=1, row=0, padx=10)
    output_text = ctk.CTkTextbox(tab, height=500, width=300)
    output_text.grid(column=1, row=1, padx=10)

    history_label = ctk.CTkLabel(tab, text="History")
    history_label.grid(column=2, row=0, padx=10)
    history_text = ctk.CTkTextbox(tab, height=500, width=200)
    history_text.insert('end', HISTORY_PLACEHOLDER)
    history_text.configure(state='disabled')
    history_text.grid(column=2, row=1, padx=10)

    ignore_colons = ctk.StringVar(value='0')
    ignore_colons_checkbox = ctk.CTkCheckBox(tab, text="Ignore text before colons", variable=ignore_colons)
    ignore_colons_checkbox.grid(column=0, row=2, padx=10, pady=10)
    ignore_colons_checkbox.select()

    enclose_in_quotes = ctk.StringVar(value='0')
    enclose_in_quotes_checkbox = ctk.CTkCheckBox(tab, text="Enclose each item in quotes", variable=enclose_in_quotes)
    enclose_in_quotes_checkbox.grid(column=0, row=3, padx=10, pady=10)
    enclose_in_quotes_checkbox.select()