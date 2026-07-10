from html.parser import HTMLParser

class StructurePrinter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'div': self.depth += 1

    def handle_endtag(self, tag):
        if tag == 'div': self.depth -= 1

with open('index.html', 'r') as f:
    html = f.read()

start_str = '<div class="app-content" id="appContent">'
end_str = '</div> <!-- End appContent -->'
start = html.find(start_str)
end = html.find(end_str)

block = html[start:end]

checker = StructurePrinter()
checker.feed(block)
print(f"appContent balance: {checker.depth}")
