import customtkinter as ctk
import itertools
import numpy as np
import webbrowser

from tkinter import messagebox

from layout_items import create_label_and_text, create_checkbox, create_button, create_category_box

WARN_ON_SEARCH_COUNT = 1_000
WARN_ON_TAB_COUNT = 100
NUM_CATEGORIES = 5
ROWS_PER_CATEGORY = 3
CATEGORY_SPAN = NUM_CATEGORIES * ROWS_PER_CATEGORY
NUM_CHECKBOXES = 6

COMBINATION_SEPARATOR = '\n\n'
TERM_SEPARATOR = '\n'
HISTORY_PLACEHOLDER = "History of searches will appear here."

PLACEHOLDER_CATEGORY_TEXTS = ['John, Susan' if i == 0 else '' for i in range(NUM_CATEGORIES)]

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

    # TODO: Fix bug with master label if too long.
    # TODO: Allow naming of categories.
    # TODO: Allow clicking on a history item to recreate the search.
    # TODO: Have better way of using column and row numbers.
    # TODO: Clean up UI.

    def create_output() -> None:
        """Creates all possible combinations of the input lists and displays them in the output textbox."""
        
        input_entries = get_search_terms_from_checkboxes()
        input_entries.extend(input_text.get("1.0", "end-1c").split(COMBINATION_SEPARATOR))
        print(input_entries)

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
        history_text.insert('end', get_history_text_from_search())
        history_text.configure(state='disabled')

    def get_history_text_from_search() -> str:
        """Gets the history of a search."""
        # TODO: Make into a data structure that can recreate the search. Use history tab to build text from that.
        category_search_terms = get_search_terms_from_checkboxes()
        input_search_terms = input_text.get("1.0", "end-1c")
        negative_search_terms = negative_input_text.get("1.0", "end-1c")
        search_text = ''
        for i, term in enumerate(category_search_terms):
            if term:
                search_text += f"Category {i+1}: {term.replace('\n', ', ')}, "
        search_text += f"Other: {input_search_terms.replace('\n\n', ' | ').replace('\n', ', ')}, Negative: {negative_search_terms.replace('\n', ', ')}"
        return search_text + '\n\n'

    def clear_history() -> None:
        """Clears the history of searches."""
        history.clear()
        history_text.configure(state='normal')
        history_text.delete('1.0', 'end')
        history_text.insert('end', HISTORY_PLACEHOLDER)
        history_text.configure(state='disabled')

    def get_category_frames() -> list[ctk.CTkFrame]:
        """Gets all frames containing checkboxes in a tab."""
        frames = []
        for widget in tab.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget.winfo_id.startswith('category'):
                frames.append(widget)
        return frames

    def populate_categories(category_texts: list[str]) -> list[str]:
        """Alters the state of the checkboxes based on the category text."""
        if category_texts == []:
            category_texts = PLACEHOLDER_CATEGORY_TEXTS
        category_checkbox_frames = get_category_frames()

        if len(category_checkbox_frames) == 0:
            for i in range(NUM_CATEGORIES):
                category_label, category_text, category_checkbox_frame = create_category_box(tab, f"Category {i+1}:", category_texts[i], 0, i*ROWS_PER_CATEGORY, 200, 25)  
                category_checkbox_frames.append(category_checkbox_frame)

        for i, frame in enumerate(category_checkbox_frames):
            category_terms = category_texts[i].split(',')
            category_terms = [t for t in category_terms if t.strip()]
            for j, checkbox in enumerate(frame.winfo_children()):
                if category_terms != [] and len(category_terms) > j:
                    checkbox.configure(state='normal')
                    checkbox.configure(text=category_terms[j].strip())
                else:
                    checkbox.configure(state='disabled')
                    checkbox.configure(text=f"Checkbox {j+1}")
                    checkbox.deselect()
        
        return category_texts
    
    def get_text_from_column(tab: ctk.CTkFrame, column: int): 
        """Gets all text from a given column in a tab."""
        text = []
        for widget in tab.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget.grid_info()['column'] == column:
                text.extend(get_text_from_column(widget, column))
            if isinstance(widget, ctk.CTkTextbox) and widget.grid_info()['column'] == column:
                text.append(widget.get("1.0", "end-1c"))
        return text
    
    def on_tab_click(event):
        if event.widget == tab._canvas:
            populate_categories(get_text_from_column(tab, 0))

    def on_tab_open(event):
        if event.widget == tab._canvas:
            populate_categories(get_text_from_column(tab, 0))

    def select_all_checkboxes():
        for frame in get_category_frames():
            for widget in frame.winfo_children():
                if isinstance(widget, ctk.CTkCheckBox) and widget.cget('state') == 'normal':
                    widget.select()

    def deselect_all_checkboxes():
        for frame in get_category_frames():
            for widget in frame.winfo_children():
                if isinstance(widget, ctk.CTkCheckBox):
                    widget.deselect()

    def get_search_terms_from_checkboxes() -> list[str]:
        """Gets all search terms from the selected checkboxes."""
        search_terms = []
        for frame in get_category_frames():
            search_terms.append(TERM_SEPARATOR.join([checkbox.cget('text') for checkbox in frame.winfo_children() if checkbox.get()]))
        return search_terms

    # Column 0: Category search terms.
    for i in range(NUM_CATEGORIES):
        category_label, category_text, category_checkbox_frame = create_category_box(
            tab, f"Category {i+1}:", PLACEHOLDER_CATEGORY_TEXTS[i], 0, i*ROWS_PER_CATEGORY, 200, 25, id=f"category_{i}")  

    populate_categories(PLACEHOLDER_CATEGORY_TEXTS)
    tab.bind("<<NotebookTabChanged>>", on_tab_click) # Activate function when tab is opened.
    tab.bind("<Button-1>", on_tab_open) # Activate function when tab is clicked anywhere.

    check_all_button = create_button(tab, "Check All", select_all_checkboxes, 0, CATEGORY_SPAN + 3)
    uncheck_all_button = create_button(tab, "Uncheck All", deselect_all_checkboxes, 0, CATEGORY_SPAN + 4)


    # Column 1: Input search terms.
    input_label, input_text = create_label_and_text(tab, "Enter search inputs:", PLACEHOLDER_INPUT_TEXT, 1, 0, 200, 450, rowspan=CATEGORY_SPAN - 3)
    negative_input_label, negative_input_text = create_label_and_text(tab, "Enter terms to exclude:", PLACEHOLDER_NEGATIVE_INPUT_TEXT, 1, CATEGORY_SPAN - 2, 200, 25)
    enclose_in_quotes_checkbox = create_checkbox(tab, "Enclose each item in quotes", 1, CATEGORY_SPAN + 3, True)
    create_output_button = create_button(tab, "Create Output", create_output, 1, CATEGORY_SPAN + 4)

    # Column 1: Output search terms.
    output_label, output_text = create_label_and_text(tab, "Output:", PLACEHOLDER_RESULTS, 2, 0, 300, 575, rowspan=CATEGORY_SPAN + 3)
    search_button = create_button(tab, "Search All", search_all, 2, CATEGORY_SPAN + 4)

    # Column 2: Search history.
    history_label, history_text = create_label_and_text(tab, "History", HISTORY_PLACEHOLDER, 3, 0, 200, 575, rowspan=CATEGORY_SPAN + 2)
    avoid_repeats_checkbox = create_checkbox(tab, "Avoid repeating searches", 3, CATEGORY_SPAN + 3, True)
    clear_history_button = create_button(tab, "Clear History", clear_history, 3, CATEGORY_SPAN + 4)