with open('index.html', 'r') as f:
    html = f.read()

from html.parser import HTMLParser

class StructurePrinter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.stack = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        class_name = attrs_dict.get('class', '')
        id_name = attrs_dict.get('id', '')
        
        if tag == 'div':
            self.stack.append(f"id='{id_name}', class='{class_name}'")
            self.depth += 1
            if id_name == 'screenAddons':
                print(f"Parent stack for screenAddons:")
                for s in self.stack:
                    print(s)

    def handle_endtag(self, tag):
        if tag == 'div' and self.depth > 0:
            self.stack.pop()
            self.depth -= 1

parser = StructurePrinter()
parser.feed(html)
