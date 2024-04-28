import customtkinter as ctk

def create_label_and_text(tab: ctk.CTkFrame, label_text: str, placeholder_text: str | None, 
                          col: int, row: int, text_width: int, text_height: int, padx: int=10, rowspan: int=1) -> tuple[ctk.CTkLabel, ctk.CTkTextbox]:
    """Creates a label and associated textbox in a tab."""
    label = ctk.CTkLabel(tab, text=label_text)
    label.grid(column=col, row=row, padx=padx)
    label_text = ctk.CTkTextbox(tab, height=text_height, width=text_width)
    label_text.insert('end', placeholder_text)
    label_text.grid(column=col, row=row+1, padx=padx, sticky='n', rowspan=rowspan)
    return label, label_text


def create_checkbox(tab: ctk.CTkFrame, box_text: str, col: int, row: int, start_on: bool, 
                    padx: int=10, pady=5, sticky: str='w') -> ctk.CTkCheckBox:
    """Creates a checkbox in a tab."""
    checkbox = ctk.CTkCheckBox(tab, text=box_text, variable=ctk.StringVar(value='0'))
    checkbox.grid(column=col, row=row, padx=padx, pady=pady, sticky=sticky)
    if start_on: 
        checkbox.select()
    return checkbox


def create_button(tab: ctk.CTkFrame, button_text: str, command: callable, col: int, row: int, padx: int=10, pady: int=10) -> ctk.CTkButton:
    """Creates a button in a tab."""
    button = ctk.CTkButton(tab, text=button_text, command=command)
    button.grid(column=col, row=row, padx=padx, pady=pady)
    return button