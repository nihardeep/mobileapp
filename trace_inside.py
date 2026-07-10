from html.parser import HTMLParser

class Tracer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.in_app_content = False
        self.app_content_depth = -1

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            _id = next((v for k, v in attrs if k == 'id'), "")
            _class = next((v for k, v in attrs if k == 'class'), "")
            
            if _id == 'appContent':
                self.in_app_content = True
                self.app_content_depth = self.depth
            
            if self.in_app_content:
                print("  " * (self.depth - self.app_content_depth) + f"<{tag} id='{_id}' class='{_class}'> (Line {self.getpos()[0]})")

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.in_app_content:
                # print("  " * (self.depth - self.app_content_depth) + f"</{tag}> (Line {self.getpos()[0]})")
                if self.depth == self.app_content_depth:
                    self.in_app_content = False
            self.depth -= 1

with open('index.html', 'r') as f:
    html = f.read()

t = Tracer()
t.feed(html)
