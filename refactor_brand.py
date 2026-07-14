import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Special case for plural
    content = re.sub(r'\bBluChips\b', 'Loyalty Points', content)
    content = re.sub(r'\bBluChips\b', 'Loyalty Points', content, flags=re.IGNORECASE)
    
    # Exact case matches for IndiGo
    content = content.replace("IndiGo", "X Airline")
    content = content.replace("Indigo", "X Airline")
    content = content.replace("INDIGO", "X AIRLINE")
    content = content.replace("indigo", "xairline")
    
    # Exact case matches for BluChip
    content = content.replace("BluChip", "Loyalty")
    content = content.replace("Bluchip", "Loyalty")
    content = content.replace("BLUCHIP", "LOYALTY")
    content = content.replace("bluchip", "loyalty")

    # Loose "Blu"
    content = re.sub(r'\bBlu\b', 'Loyalty', content)
    
    # Extra fix for "goIndiGo" -> "goX Airline" which might look weird but that's what happens.
    # We'll leave it as goX Airline.

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

directory = '.'
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.html') or file.endswith('.css') or file.endswith('.js'):
            process_file(os.path.join(root, file))

print("Brand refactoring complete.")
