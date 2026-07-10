from html.parser import HTMLParser

class Tracer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.tags = []

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            _id = next((v for k, v in attrs if k == 'id'), "")
            _class = next((v for k, v in attrs if k == 'class'), "")
            self.stack.append((tag, _id, _class, self.getpos()[0]))
            self.tags.append(f"<{tag} class='{_class}' id='{_id}'> at line {self.getpos()[0]}")

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.stack:
                popped = self.stack.pop()
                self.tags.append(f"</{tag}> closed {popped[2]}#{popped[1]} at line {self.getpos()[0]}")
                if popped[1] in ['appContent', 'screenHome', 'screenPassenger'] or popped[2] in ['iphone-screen', 'app-container']:
                    print(f"CRITICAL CONTAINER {popped[2]}#{popped[1]} CLOSED at line {self.getpos()[0]}")
            else:
                print(f"EXTRA </{tag}> found at line {self.getpos()[0]}!")

with open('index.html', 'r') as f:
    html = f.read()

t = Tracer()
t.feed(html)
