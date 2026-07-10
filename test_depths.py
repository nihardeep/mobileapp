from html.parser import HTMLParser

class Tracer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            _id = next((v for k, v in attrs if k == 'id'), "")
            if _id in ['appContent', 'screenHome', 'homeContentContainer']:
                print(f"{_id} opens at depth {self.depth} on line {self.getpos()[0]}")

with open('index.html', 'r') as f:
    html = f.read()

t = Tracer()
t.feed(html)
