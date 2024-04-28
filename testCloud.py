import wordcloud
import tkinter as tk
import webbrowser

from PIL import ImageTk

def rgb_to_hex(rgb_str):
    """Convert an RGB string to a hexadecimal color code"""
    rgb = tuple(map(int, rgb_str.strip('rgb()').split(',')))
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

# Generate the word cloud
text = """
    Welcome to the Searching Made Easy!

    This tool contains a variety of features to help you search more easily. Current feature list:
                                
    1. Create Search Terms with AI: Use AI models to generate search terms from raw text.
    2. Get Search Combinations: Generate all possible combinations of search terms.
    
    Create Search Terms with AI:
    - Supports GPT-4 and Claude 3 AI models.
    - Enter raw text (e.g, a news article) to extract search info from.
    
    Click on the "Create Output" button to generate search terms. 
    The model will give you search terms based on the input text.
    You can use them as-is or modify them as needed - it's recommended you cut out extraneous search terms.

    Get Search Combinations:                   

    Enter search inputs. Each line represents a group of search terms, e.g, cities. These can be grouped however you like.           
    Click on the "Create Output" button to generate all possible combinations of search terms.
    For example, if you have 3 groups of search terms with 2, 3, and 4 items respectively, the tool will generate 2 * 3 * 4 = 24 combinations.
    Click on the "Search All" button to open a new tab in the default web browser for each search query.
    The tool will warn you if you are about to open a large number of tabs, but will not stop you from doing so if you choose to continue.                            

    Enjoy searching!
    """
word_cloud = wordcloud.WordCloud().generate(text)

# Create the Tkinter window and canvas
window = tk.Tk()
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack()

# Draw the word cloud on the canvas
image = word_cloud.to_image()
photo = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor="nw", image=photo)
print(word_cloud.layout_)

# Create text items for each word and bind click events
for (word, _), size, (x, y), _, color in word_cloud.layout_:
    text_id = canvas.create_text(int(y+200), int(x+300), text=word, font=f"Arial {int(size)}", fill=rgb_to_hex(color))

    def open_search(word=word):
        url = f"https://www.google.com/search?q={word}"
        webbrowser.open_new_tab(url)

    canvas.tag_bind(text_id, "<Button-1>", lambda event, word=word: open_search(word))
window.mainloop()