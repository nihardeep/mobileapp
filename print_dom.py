from html.parser import HTMLParser

class StructurePrinter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag in ['div', 'body', 'html', 'section', 'nav', 'main']:
            _id = next((v for k, v in attrs if k == 'id'), None)
            _class = next((v for k, v in attrs if k == 'class'), None)
            label = f"{tag}"
            if _id: label += f"#{_id}"
            if _class: label += f".{_class}"
            
            print("  " * self.depth + f"<{label}> (Line {self.getpos()[0]})")
            self.stack.append(label)
            self.depth += 1

    def handle_endtag(self, tag):
        if tag in ['div', 'body', 'html', 'section', 'nav', 'main']:
            self.depth -= 1
            label = self.stack.pop() if self.stack else "UNKNOWN"
            # print("  " * self.depth + f"</{label}>")

with open('index.html', 'r') as f:
    html = f.read()

checker = StructurePrinter()
checker.feed(html)
