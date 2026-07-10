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
                popped = self.stack.pop()
                if popped[1] in ['travel-on-tap-section', 'boarding-passes-stack']:
                    print(f"CLOSED {popped[1]} at line {self.getpos()[0]}")

with open('index.html', 'r') as f:
    html = f.read()

# Only up to Explore Communities
html_part = html.split("<!-- Explore Communities -->")[0]

t = Tracer()
t.feed(html_part)

print("Remaining in stack at Explore Communities:")
for s in t.stack:
    if s[1] in ['travel-on-tap-section', 'trending-destinations-section', 'screen-home-content']:
        print(s)
