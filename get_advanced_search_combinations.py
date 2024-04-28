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

history = set()

def create_advanced_search_combinations(root: ctk.CTk, tab: ctk.CTkFrame) -> None:
    """Creates a tab for generating all possible combinations of search terms."""
    # TODO: Refactor into classes.

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

        # Add negative search terms if present.
        if negative_input_text != PLACEHOLDER_NEGATIVE_INPUT_TEXT:
            negative_entries = negative_input_text.get("1.0", "end-1c").split(', ')
            negative_string = ' '.join([f'-{item.strip()}' for item in negative_entries if item.strip()])
            output_strings = [f'{output} {negative_string}' for output in output_strings]

        output_content = '\n'.join(output_strings)
        output_text.delete('1.0', 'end')  # Clear previous output
        output_text.insert('end', output_content)  # Insert new output
        search_button.configure(state=ctk.NORMAL if output_content else ctk.DISABLED)

    def search_all() -> None:
        """Opens a new tab in the default web browser for each search query."""
 
        queries = output_text.get("1.0", "end-1c").split('\n')
        if avoid_repeats.get() == '1':
            queries = [query for query in queries if query not in history]

        if len(queries) > WARN_ON_TAB_COUNT:
            if not messagebox.askyesno("Confirmation", f"Warning: This will open {len(queries)} tabs at once. Continue?"):
                return
            
        if len(queries) == 0:
            messagebox.showinfo("No queries", "All queries have been searched before. Please modify your search inputs or clear the history.")
            return

        for query in queries:
            history.add(query)
            search_url = f"https://www.google.com/search?q={query}"
            webbrowser.open_new_tab(search_url)

        history_text.configure(state='normal')
        if history_text.get("1.0", "end-1c") == HISTORY_PLACEHOLDER:
            history_text.delete('1.0', 'end')
        history_text.insert('end', len(history))
        history_text.configure(state='disabled')

    def clear_history() -> None:
        """Clears the history of searches."""
        history.clear()
        history_text.configure(state='normal')
        history_text.delete('1.0', 'end')
        history_text.insert('end', HISTORY_PLACEHOLDER)
        history_text.configure(state='disabled')


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
    history_text.grid(column=2, row=1, padx=10, rowspan=4, sticky='n')

    avoid_repeats = ctk.StringVar(value='0')
    avoid_repeats_checkbox = ctk.CTkCheckBox(tab, text="Avoid repeating searches", variable=avoid_repeats)
    avoid_repeats_checkbox.grid(column=2, row=5, padx=10, pady=5, sticky='w')
    avoid_repeats_checkbox.select()

    ignore_colons = ctk.StringVar(value='0')
    ignore_colons_checkbox = ctk.CTkCheckBox(tab, text="Ignore text before colons", variable=ignore_colons)
    ignore_colons_checkbox.grid(column=0, row=4, padx=10, pady=5, sticky='w')
    ignore_colons_checkbox.select()

    enclose_in_quotes = ctk.StringVar(value='0')
    enclose_in_quotes_checkbox = ctk.CTkCheckBox(tab, text="Enclose each item in quotes", variable=enclose_in_quotes)
    enclose_in_quotes_checkbox.grid(column=0, row=5, padx=10, pady=5, sticky='w')
    enclose_in_quotes_checkbox.select()

    output_button = ctk.CTkButton(tab, text="Create Output", command=create_output)
    output_button.grid(column=0, row=6, padx=10, pady=10)
    search_button = ctk.CTkButton(tab, text="Search All", command=search_all)
    search_button.grid(column=1, row=6, padx=10, pady=10)
    clear_history_button = ctk.CTkButton(tab, text="Clear History", command=clear_history)
    clear_history_button.grid(column=2, row=6, padx=10, pady=10)