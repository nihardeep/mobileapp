from html.parser import HTMLParser

class StructurePrinter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.min_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'div': 
            self.depth += 1

    def handle_endtag(self, tag):
        if tag == 'div': 
            self.depth -= 1
            if self.depth < self.min_depth:
                self.min_depth = self.depth
                print(f"Depth went negative ({self.depth}) around line {self.getpos()[0]}")

with open('index.html', 'r') as f:
    html = f.read()

checker = StructurePrinter()
checker.feed(html)
print(f"Overall div balance: {checker.depth}")
