from html.parser import HTMLParser

class StructurePrinter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.min_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'div': self.depth += 1

    def handle_endtag(self, tag):
        if tag == 'div': 
            self.depth -= 1
            if self.depth < self.min_depth:
                self.min_depth = self.depth

import re
with open('index.html', 'r') as f:
    html = f.read()

start_str = '<div class="app-content" id="appContent">'
end_str = '</div> <!-- End appContent -->'
start = html.find(start_str)
end = html.find(end_str)

block = html[start:end]

screens = re.split(r'(?=<div[^>]*class="[^"]*screen)', block)

for i, s in enumerate(screens):
    if not s.strip() or not s.startswith('<div'): continue
    match = re.search(r'id="([^"]+)"', s)
    screen_id = match.group(1) if match else "unknown"
    checker = StructurePrinter()
    checker.feed(s)
    print(f"Screen {screen_id}: depth={checker.depth}, min={checker.min_depth}")
