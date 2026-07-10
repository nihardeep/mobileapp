from html.parser import HTMLParser

class MyParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        classes = attr_dict.get('class', '')
        id_ = attr_dict.get('id', '')
        self.stack.append((tag, classes, id_))
        
        if 'bottom-sheet-drawer' in classes:
            print(f"Found drawer {id_} at depth {len(self.stack)}")
            print(f"Parent hierarchy: {[x[1] for x in self.stack[-5:-1]]}")
            
    def handle_endtag(self, tag):
        if self.stack:
            self.stack.pop()

parser = MyParser()
with open('index.html', 'r') as f:
    parser.feed(f.read())
