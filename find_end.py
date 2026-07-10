from html.parser import HTMLParser

class StructurePrinter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.stack = []
        self.current_line = 1

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            attrs_dict = dict(attrs)
            id_name = attrs_dict.get('id', '')
            self.stack.append((id_name, self.getpos()[0]))
            self.depth += 1

    def handle_endtag(self, tag):
        if tag == 'div' and self.depth > 0:
            id_name, start_line = self.stack.pop()
            if id_name == 'screenDestinationAI':
                print(f"screenDestinationAI starts at {start_line} and ends at {self.getpos()[0]}")
            self.depth -= 1

parser = StructurePrinter()
with open('index.html', 'r') as f:
    parser.feed(f.read())
