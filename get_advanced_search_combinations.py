import customtkinter as ctk
import itertools
import numpy as np
import webbrowser

from tkinter import messagebox

from layout_items import create_label_and_text, create_checkbox, create_button

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

    # TODO: Add master label(s) that let you decide which output subset to look for?
    # TODO: Add subset search option using checkboxes.
    # TODO: Add names for searches in history.
    # TODO: Make all these above advanced terms, remember. 
    # TODO: Add priority system?

    def create_output() -> None:
        """Creates all possible combinations of the input lists and displays them in the output textbox."""
        input_entries = input_text.get("1.0", "end-1c").split(COMBINATION_SEPARATOR)

        if ignore_colons_checkbox.get() == 1:
            input_entries = [entry.split(':')[-1].strip() for entry in input_entries]
        input_lists = [entry.split(TERM_SEPARATOR) for entry in input_entries if entry.strip()] # if entry.strip() removes empty entries

        total_entries = np.prod([len(entry) for entry in input_lists])
        if total_entries > WARN_ON_SEARCH_COUNT:
            if not messagebox.askyesno("Confirmation", f"Warning: {total_entries} combinations will be generated. Continue?"):
                return
        
        outputs = itertools.product(*input_lists)
        output_strings = [' '.join([f'"{item.strip()}"' if enclose_in_quotes_checkbox.get() == 1 else item.strip() for item in output]) for output in outputs]

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
        if avoid_repeats_checkbox.get() == 1:
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

    # Column 0: Input search terms.
    input_label, input_text = create_label_and_text(tab, "Enter search inputs:", PLACEHOLDER_INPUT_TEXT, 0, 0, 200, 450)
    negative_input_label, negative_input_text = create_label_and_text(tab, "Enter terms to exclude:", PLACEHOLDER_NEGATIVE_INPUT_TEXT, 0, 2, 200, 25)
    ignore_colons_checkbox = create_checkbox(tab, "Ignore text before colons", 0, 4, True)
    enclose_in_quotes_checkbox = create_checkbox(tab, "Enclose each item in quotes", 0, 5, True)
    create_output_button = create_button(tab, "Create Output", create_output, 0, 6)

    # Column 1: Output search terms.
    output_label, output_text = create_label_and_text(tab, "Output:", PLACEHOLDER_RESULTS, 1, 0, 300, 575, rowspan=5)
    search_button = create_button(tab, "Search All", search_all, 1, 6)

    # Column 2: Search history.
    history_label, history_text = create_label_and_text(tab, "History", HISTORY_PLACEHOLDER, 2, 0, 200, 575, rowspan=4)
    avoid_repeats_checkbox = create_checkbox(tab, "Avoid repeating searches", 2, 5, True)
    clear_history_button = create_button(tab, "Clear History", clear_history, 2, 6)