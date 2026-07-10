from html.parser import HTMLParser

class StructurePrinter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.app_content_depth = -1
        self.app_content_close = -1
        self.iphone_screen_depth = -1
        self.iphone_screen_close = -1

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            _class = next((v for k, v in attrs if k == 'class'), None)
            if _class == 'app-content':
                self.app_content_depth = self.depth
            elif _class == 'iphone-screen':
                self.iphone_screen_depth = self.depth

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.app_content_depth != -1 and self.depth == self.app_content_depth:
                self.app_content_close = self.getpos()[0]
                self.app_content_depth = -1
            if self.iphone_screen_depth != -1 and self.depth == self.iphone_screen_depth:
                self.iphone_screen_close = self.getpos()[0]
                self.iphone_screen_depth = -1
            self.depth -= 1

with open('index.html', 'r') as f:
    html = f.read()

checker = StructurePrinter()
checker.feed(html)
print(f"iphone-screen close: {checker.iphone_screen_close}")
print(f"app-content close: {checker.app_content_close}")
