from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        if tag not in ['img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'path', 'circle', 'rect']:
            self.tags.append(tag)

    def handle_endtag(self, tag):
        if tag not in ['img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'path', 'circle', 'rect']:
            if not self.tags:
                print(f"Extra closing tag: </{tag}>")
            elif self.tags[-1] == tag:
                self.tags.pop()
            else:
                print(f"Mismatched closing tag: expected </{self.tags[-1]}>, got </{tag}>")
                # try to recover
                if tag in self.tags:
                    while self.tags[-1] != tag:
                        self.tags.pop()
                    self.tags.pop()

parser = MyHTMLParser()
with open('index.html', 'r') as f:
    parser.feed(f.read())

if parser.tags:
    print(f"Unclosed tags: {parser.tags}")
else:
    print("HTML tags perfectly balanced!")
