import customtkinter as ctk

from constants import DISALLOWED_FEATURES

WELCOME = """Welcome to Searching Made Easy!

This tool contains a variety of features to help you search more easily."""

CREATE_SEARCH_TERMS_WITH_AI_INSTRUCTIONS = """- Supports GPT-4 and Claude 3 AI models.
- Enter raw text (e.g, a news article) to extract search info from.

Click on the "Create Output" button to generate search terms. The model will give you search terms based on the input text.
You can use them as-is or modify them as needed - it's recommended you cut out extraneous search terms. 
The model is prompted to err on the side of giving more info, not less.
"""

GET_SEARCH_COMBINATIONS_INSTRUCTIONS = """Enter search inputs. Each line represents a group of search terms, e.g, cities. 
These can be grouped however you like. Click on the "Create Output" button to generate all possible combinations of search terms. 
For example, if you have 3 groups of search terms with 2, 3, and 4 items respectively, the tool will generate 2 * 3 * 4 = 24 combinations.
Click on the "Search All" button to open a new tab in the default web browser for each search query.
The tool will warn you if you are about to open a large number of tabs, but will not stop you from doing so if you choose to continue.
"""

GET_SEARCH_COMBINATIONS_ADVANCED_INSTRUCTIONS = """For power users.

Column 0: Category search terms. Each line represents a group of search terms, e.g, cities. 
Combinations will be made only from the selected items in each category. Negative items will be added to every search query.

Column 1: Additional search terms. These will be added to each combination.

Column 2: Output. This will display all possible combinations of search terms. Search All will open a new tab in the default web browser for each search query.
You can edit the output before searching if needed.

Column 3: History. This will display the searches you have made. If Avoid Repeat Searches is selected, the tool will not repeat searches you have made before.
You can clear the history with Clear History to prevent this."""

OUTRO = """Enjoy searching!"""

instruction_dict = {"Create Search Terms with AI": CREATE_SEARCH_TERMS_WITH_AI_INSTRUCTIONS,
                "Get Search Combinations": GET_SEARCH_COMBINATIONS_INSTRUCTIONS,
                "Get Search Combinations (Advanced)": GET_SEARCH_COMBINATIONS_ADVANCED_INSTRUCTIONS}


def create_instructions_tab(root: ctk.CTk, tab: ctk.CTkFrame) -> None:
    """Creates a tab for displaying instructions on how to use the tool."""
    instructions = create_instructions()
    instructions = ctk.CTkLabel(tab, text=instructions, wraplength=tab.winfo_width()-50, justify='left')
    instructions.pack(pady=20)

def create_instructions() -> str:
    """Creates instructions for the user."""
    instructions = WELCOME + '\n\n'
    for feature, instruction in instruction_dict.items():
        if feature not in DISALLOWED_FEATURES:
            instructions += f"{feature}:\n{instruction}\n\n"
    instructions += OUTRO
    return instructions