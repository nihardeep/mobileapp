from html.parser import HTMLParser

class StructurePrinter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.target_depth = -1
        self.closed_line = -1

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            _id = next((v for k, v in attrs if k == 'id'), "")
            if _id == 'screenHome':
                self.target_depth = self.depth

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.target_depth != -1 and self.depth == self.target_depth:
                self.closed_line = self.getpos()[0]
                self.target_depth = -1
            self.depth -= 1

with open('index.html', 'r') as f:
    html = f.read()

checker = StructurePrinter()
checker.feed(html)
print(f"screenHome closed at line: {checker.closed_line}")
