import re
import os

with open('index.html', 'r') as f:
    html = f.read()

# We will find all `<div class="bottom-sheet-drawer"` or `<div class="bottom-sheet-backdrop"`
# and extract them by balancing `div` tags.

extracted = []

while True:
    match = re.search(r'<div[^>]*class="[^"]*bottom-sheet-(?:drawer|backdrop)[^"]*"[^>]*>', html)
    if not match:
        break
        
    start_idx = match.start()
    
    # Balance tags
    depth = 0
    i = start_idx
    
    while i < len(html):
        # Find next <div or </div
        next_open = html.find('<div', i)
        next_close = html.find('</div', i)
        
        if next_open == -1: next_open = float('inf')
        if next_close == -1: next_close = float('inf')
        
        if next_open < next_close:
            depth += 1
            i = next_open + 4
        elif next_close < next_open:
            depth -= 1
            i = next_close + 6
            if depth == 0:
                end_idx = html.find('>', i) + 1
                extracted.append(html[start_idx:end_idx])
                html = html[:start_idx] + html[end_idx:]
                break
        else:
            break

print(f"Extracted {len(extracted)} drawers.")

insertion_point = html.rfind('<!-- Haptic audio simulation nodes -->')

all_drawers_html = "\n\n<!-- ALL BOTTOM SHEET DRAWERS -->\n" + "\n".join(extracted) + "\n\n"

final_html = html[:insertion_point] + all_drawers_html + html[insertion_point:]

with open('index.html.manual', 'w') as f:
    f.write(final_html)

os.system('mv index.html.manual index.html')
print("Fixed via manual tag balancing!")
