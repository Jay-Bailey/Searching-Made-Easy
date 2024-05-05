import customtkinter as ctk
import itertools
import numpy as np
import webbrowser

from tkinter import messagebox

WARN_ON_SEARCH_COUNT = 1_000
WARN_ON_TAB_COUNT = 100

COMBINATION_SEPARATOR = '\n\n'
TERM_SEPARATOR = '\n'


def create_search_combinations(root: ctk.CTk, tab: ctk.CTkFrame) -> None:
    """Creates a tab for generating all possible combinations of search terms."""

    input_label = ctk.CTkLabel(tab, text="Enter search inputs (one per line, groups separated by a blank line):")
    input_label.pack()
    input_text = ctk.CTkTextbox(tab, height=100, width=300)
    input_text.pack(fill='both', expand=True)

    output_label = ctk.CTkLabel(tab, text="Output:")
    output_label.pack()
    output_text = ctk.CTkTextbox(tab, height=200, width=300)
    output_text.pack(fill='both', expand=True)

    checkbox_frame = ctk.CTkFrame(tab)
    checkbox_frame.pack(pady=10)
    ignore_colons = ctk.StringVar(value='0')
    ignore_colons_checkbox = ctk.CTkCheckBox(checkbox_frame, text="Ignore text before colons", variable=ignore_colons)
    ignore_colons_checkbox.pack(side='left', padx=5)
    ignore_colons_checkbox.select()

    enclose_in_quotes = ctk.StringVar(value='0')
    enclose_in_quotes_checkbox = ctk.CTkCheckBox(checkbox_frame, text="Enclose each item in quotes", variable=enclose_in_quotes)
    enclose_in_quotes_checkbox.pack(side='left', padx=5)
    enclose_in_quotes_checkbox.select()


    def create_output() -> None:
        """Creates all possible combinations of the input lists and displays them in the output textbox."""
        input_entries = input_text.get("1.0", "end-1c").split(COMBINATION_SEPARATOR)

        if ignore_colons.get() == '1':
            input_entries = [entry.split(':')[-1].strip() for entry in input_entries]
        input_lists = [entry.split(TERM_SEPARATOR) for entry in input_entries if entry.strip()]

        total_entries = np.prod([len(entry) for entry in input_lists])
        if total_entries > WARN_ON_SEARCH_COUNT:
            message = f"Warning: {total_entries} combinations will be generated. Continue?"
            if not messagebox.askyesno("Confirmation", message):
                return
        
        outputs = itertools.product(*input_lists)
        output_strings = [' '.join([f'"{item.strip()}"' if enclose_in_quotes.get() == '1' else item.strip() for item in output]) for output in outputs]
        output_content = '\n'.join(output_strings)
        output_text.delete('1.0', 'end')  # Clear previous output
        output_text.insert('end', output_content)  # Insert new output
        search_button.configure(state=ctk.NORMAL if output_content else ctk.DISABLED)

    def search_all() -> None:
        """Opens a new tab in the default web browser for each search query."""
        input_entries = input_text.get("1.0", "end-1c").split(COMBINATION_SEPARATOR)
        input_lists = [entry.split(TERM_SEPARATOR) for entry in input_entries if entry.strip()]
        total_entries = np.prod([len(entry) for entry in input_lists])
        outputs = itertools.product(*input_lists)
        if total_entries > WARN_ON_TAB_COUNT:
            if not messagebox.askyesno("Confirmation", f"Warning: This will open {total_entries} tabs at once. Continue?"):
                return

        for output in outputs:
            search_query = ' '.join([f'"{item.strip()}"' if enclose_in_quotes.get() == '1' else item.strip() for item in output])
            search_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open_new_tab(search_url)

    button_frame = ctk.CTkFrame(tab)
    button_frame.pack(pady=10)
    output_button = ctk.CTkButton(button_frame, text="Create Output", command=create_output)
    output_button.pack(side='left', padx=5)
    search_button = ctk.CTkButton(button_frame, text="Search All", command=search_all, state=ctk.DISABLED)
    search_button.pack(side='left', padx=5)