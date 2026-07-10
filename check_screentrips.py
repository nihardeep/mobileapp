from html.parser import HTMLParser

class StructurePrinter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'div': self.depth += 1

    def handle_endtag(self, tag):
        if tag == 'div': self.depth -= 1

import re
with open('index.html', 'r') as f:
    html = f.read()

start_str = '<div class="screen" id="screenTrips">'
end_str = '<div class="screen" id="screenResults"'
start = html.find(start_str)
end = html.find(end_str)

block = html[start:end]

checker = StructurePrinter()
checker.feed(block)
print(f"screenTrips balance: {checker.depth}")
