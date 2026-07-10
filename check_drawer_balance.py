from html.parser import HTMLParser

class BalanceChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.balance = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'div': self.balance += 1
    
    def handle_endtag(self, tag):
        if tag == 'div': self.balance -= 1

import re
with open('index.html', 'r') as f:
    html = f.read()

start_str = '<div class="iphone-screen">'
end_str = '<!-- Parallax Atmospheric Background -->'
drawers_block = html[html.find(start_str)+len(start_str):html.find(end_str)]

# Split into individual drawers using regex
drawers = re.split(r'(?=<div[^>]*class="[^"]*bottom-sheet-(?:drawer|backdrop))', drawers_block)

for i, d in enumerate(drawers):
    if not d.strip(): continue
    checker = BalanceChecker()
    checker.feed(d)
    
    # Extract ID
    id_match = re.search(r'id="([^"]+)"', d)
    id_name = id_match.group(1) if id_match else f"Drawer {i}"
    
    print(f"{id_name} balance: {checker.balance}")
