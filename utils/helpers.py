import re

def cleanse_string(s):
    # This pattern will match any character that is NOT a letter, number, parentheses, dash, space, comma, or new line
    pattern = r'[^a-zA-Z0-9\(\)\-\s,\n]'
    # Replace those characters with an empty string
    cleaned_string = re.sub(pattern, '', s)
    return cleaned_string
