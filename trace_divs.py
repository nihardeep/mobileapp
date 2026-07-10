from html.parser import HTMLParser

class Tracer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.stack = []
        self.in_app_content = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            _id = next((v for k, v in attrs if k == 'id'), "")
            _class = next((v for k, v in attrs if k == 'class'), "")
            self.stack.append((tag, _id, _class, self.getpos()[0]))
            
            if _id == 'appContent':
                self.in_app_content = True

    def handle_endtag(self, tag):
        if tag == 'div':
            self.depth -= 1
            if self.stack:
                popped = self.stack.pop()
                if popped[1] == 'appContent':
                    print(f"appContent CLOSED at line {self.getpos()[0]}")
                    for item in reversed(self.stack[-10:]):
                        print("  Parent:", item)
                    self.in_app_content = False

with open('index.html', 'r') as f:
    html = f.read()

t = Tracer()
t.feed(html)
