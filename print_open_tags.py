from html.parser import HTMLParser

class Tracer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            _id = next((v for k, v in attrs if k == 'id'), "")
            _class = next((v for k, v in attrs if k == 'class'), "")
            self.stack.append((_id, _class, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.stack:
                self.stack.pop()

with open('index.html', 'r') as f:
    html = f.read()

# Let's parse up to line 2295 (before my inserted </div>)
html_part = "\n".join(html.split("\n")[:2295])

t = Tracer()
t.feed(html_part)

for item in t.stack:
    print(f"ID: {item[0]}, Class: {item[1]}, Line: {item[2]}")
