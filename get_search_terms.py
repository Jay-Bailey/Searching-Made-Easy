import anthropic
import customtkinter as ctk

from openai import OpenAI

ANTHROPIC_API_KEY = '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'
OPENAI_API_KEY = 'sk-proj-lTcn3ajPTFUGQSVCa4ZLT3BlbkFJF3CPnjn19d4l06UFxaNd'

anthropic_client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

SEARCH_PROMPT = """You are an expert private investigator and have been hired to find information. 
Presented to you will be one or more paragraphs of text. Your job is to extract useful Google search terms
such as cities, people's names, and so on. You should not include any irrelevant words. Since I don't know
exactly which types of information will be useful, you should extract as much as you can.

Your reply should be one or more lines of search terms separated by commas. For example:

Cities: Chicago, Illinois
People: John Doe, Jane Smith
Companies: Acme Corporation, Widget Co."""


def create_search_terms(tab: ctk.CTkFrame) -> None:
    """Creates a tab for generating all possible combinations of search terms."""

    model_label = ctk.CTkLabel(tab, text="Select the AI model to use:")
    model_label.pack()
    model_dropdown = ctk.CTkOptionMenu(tab, values=["GPT-4", "Claude 3"])
    model_dropdown.pack()

    input_label = ctk.CTkLabel(tab, text="Enter raw text to extract search info from:")
    input_label.pack()
    input_text = ctk.CTkTextbox(tab, height=100, width=300)
    input_text.pack()

    output_label = ctk.CTkLabel(tab, text="Output:")
    output_label.pack()
    output_text = ctk.CTkTextbox(tab, height=200, width=300)
    output_text.pack()

    def create_openai_output() -> None:
        """Uses the OpenAI API to generate search terms from the input text."""
        output_text.delete('1.0', 'end')
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4-1106-preview",
                max_tokens=2048,
                messages=[
                    {"role": "system", "content": SEARCH_PROMPT},
                    {"role": "user", "content": input_text.get("1.0", "end-1c")}
                ]
            )
            output = response.choices[0].message.content
            output_text.insert('end', output)
        except Exception as e:
            output_text.insert('end', f"Error: {e}")

    def create_anthropic_output() -> None:
        """Uses the Anthropic API to generate search terms from the input text."""
        output_text.delete('1.0', 'end')
        try:
            response = anthropic_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2048,
                messages = [
                    {"role": "user", "content": SEARCH_PROMPT},
                    {"role": "assistant", "content": "I'd be happy to do that! Please provide the text."},
                    {"role": "user", "content": input_text.get("1.0", "end-1c")}
                ]
            )
            output = response.content[0].text
            output_text.insert('end', output)
        except Exception as e:
            output_text.insert('end', f"Error: {e}")

    MODEL_FUNCTIONS = {"GPT-4": create_openai_output, "Claude 3": create_anthropic_output}
    button_frame = ctk.CTkFrame(tab)
    button_frame.pack(pady=10)
    output_button = ctk.CTkButton(button_frame, text="Create Output", 
                                  command=MODEL_FUNCTIONS[model_dropdown.get()])
    output_button.pack(side='left', padx=5)