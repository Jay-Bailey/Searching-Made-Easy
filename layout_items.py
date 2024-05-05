import customtkinter as ctk
from CTkListbox import CTkListbox

def create_category_box(tab: ctk.CTkFrame, label_text: str, placeholder_text: str | None, col: int, row: int, 
                        text_width: int, text_height: int, checkboxes: int=6, padx: int=10, pady: int=5, id: str | None=None) -> tuple[ctk.CTkLabel, ctk.CTkTextbox, ctk.CTkFrame]:
    """Creates a category box in a tab."""
    # TODO: Consider making this a class.
    label, label_text = create_label_and_text(tab, label_text, placeholder_text, col, row, text_width, text_height, padx)
    checkbox_frame = ctk.CTkFrame(tab)
    checkbox_frame.name = id
    checkbox_frame.grid(column=col, row=row+2, padx=padx, pady=pady, sticky='w')
    for i in range(checkboxes):
        ctk.CTkCheckBox(checkbox_frame, text=f"Checkbox {i+1}").grid(column=i % 3, row=i // 3, padx=5)
    return label, label_text, checkbox_frame


def create_label_and_text(tab: ctk.CTkFrame, label_title: str, placeholder_text: str | None, col: int, row: int, 
                          text_width: int, text_height: int, padx: int=10, rowspan: int=1) -> tuple[ctk.CTkLabel, ctk.CTkTextbox]:
    """Creates a label and associated textbox in a tab."""
    label = ctk.CTkLabel(tab, text=label_title)
    label.grid(column=col, row=row, padx=padx)
    label_box = ctk.CTkTextbox(tab, height=text_height, width=text_width)
    if placeholder_text: 
        label_box.insert('end', placeholder_text)
    label_box.grid(column=col, row=row+1, padx=padx, sticky='n', rowspan=rowspan)
    return label, label_box

def create_label_and_listbox(tab: ctk.CTkFrame, label_title: str, placeholder_text: str | None, col: int, row: int, 
                          text_width: int, text_height: int, padx: int=10, rowspan: int=1) -> tuple[ctk.CTkLabel, CTkListbox]:
    """Creates a label and associated listbox in a tab."""
    label = ctk.CTkLabel(tab, text=label_title)
    label.grid(column=col, row=row, padx=padx)
    label_box = CTkListbox(tab, height=text_height, width=text_width, multiple_selection=True)

    if placeholder_text:
        for i, item in enumerate(placeholder_text.split('\n')):
            label_box.insert(i, item.strip())

    label_box.grid(column=col, row=row+1, padx=padx, sticky='n', rowspan=rowspan)
    return label, label_box
    

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