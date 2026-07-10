from html.parser import HTMLParser

class StructurePrinter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.in_app_content = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        class_name = attrs_dict.get('class', '')
        id_name = attrs_dict.get('id', '')
        
        if id_name == 'appContent':
            self.in_app_content = True

        if self.in_app_content and tag == 'div':
            indent = "  " * self.depth
            print(f"{indent}<div id='{id_name}' class='{class_name}'>")
            self.depth += 1
            
            # Don't go too deep, just top level screens
            if self.depth > 2:
                self.in_app_content = False

    def handle_endtag(self, tag):
        if tag == 'div' and self.depth > 0:
            self.depth -= 1

parser = StructurePrinter()
with open('index.html', 'r') as f:
    parser.feed(f.read())
