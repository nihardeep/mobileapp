from html.parser import HTMLParser

class StructurePrinter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.app_content_depth = -1
        self.closed_line = -1

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            _class = next((v for k, v in attrs if k == 'class'), None)
            if _class == 'app-content':
                self.app_content_depth = self.depth

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.app_content_depth != -1 and self.depth == self.app_content_depth:
                self.closed_line = self.getpos()[0]
                self.app_content_depth = -1
            self.depth -= 1

with open('index.html', 'r') as f:
    html = f.read()

checker = StructurePrinter()
checker.feed(html)
print(f"app-content closed at line: {checker.closed_line}")
