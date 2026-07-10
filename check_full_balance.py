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

checker = StructurePrinter()
checker.feed(html)
print(f"Overall div balance: {checker.depth}")
