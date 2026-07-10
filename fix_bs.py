from bs4 import BeautifulSoup
import os

with open('index.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

drawers = soup.find_all(class_='bottom-sheet-drawer')
backdrop = soup.find(id='bottomSheetBackdrop')

extracted = []
for drawer in drawers:
    extracted.append(str(drawer))
    drawer.decompose() # Removes from soup

if backdrop:
    extracted.append(str(backdrop))
    backdrop.decompose()

print(f"Extracted {len(extracted)} elements.")

# Find the haptic audio nodes in the new string
new_html = str(soup)
insertion_point = new_html.rfind('<!-- Haptic audio simulation nodes -->')

all_drawers_html = "\n\n<!-- ALL BOTTOM SHEET DRAWERS -->\n" + "\n".join(extracted) + "\n\n"

final_html = new_html[:insertion_point] + all_drawers_html + new_html[insertion_point:]

with open('index.html.bs', 'w') as f:
    f.write(final_html)

os.system('mv index.html.bs index.html')
print("Fixed via BS4!")
