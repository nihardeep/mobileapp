from html.parser import HTMLParser

class Tracer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.home_content = False
        self.screen_home = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            _id = next((v for k, v in attrs if k == 'id'), "")
            if _id == 'homeContentContainer':
                self.home_content = True
            elif _id == 'screenHome':
                self.screen_home = True

    def handle_endtag(self, tag):
        if tag == 'div':
            self.depth -= 1
            if self.getpos()[0] >= 865 and self.getpos()[0] <= 872:
                print(f"Line {self.getpos()[0]}: depth is now {self.depth}")

with open('index.html', 'r') as f:
    html = f.read()

t = Tracer()
t.feed(html)
