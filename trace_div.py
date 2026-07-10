from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.appContent = None
        self.screenHome = None

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            attr_dict = dict(attrs)
            uid = f"div_{self.getpos()[0]}"
            if attr_dict.get('id') == 'appContent':
                self.appContent = len(self.stack)
                print(f"appContent starts at line {self.getpos()[0]}, depth {len(self.stack)}")
            if attr_dict.get('id') == 'screenHome':
                self.screenHome = len(self.stack)
                print(f"screenHome starts at line {self.getpos()[0]}, depth {len(self.stack)}")
            
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag == "div":
            if len(self.stack) > 0:
                _, start_line = self.stack.pop()
                if self.appContent == len(self.stack):
                    print(f"appContent ends at line {self.getpos()[0]}")
                if self.screenHome == len(self.stack):
                    print(f"screenHome ends at line {self.getpos()[0]}")

parser = MyHTMLParser()
with open('index.html', 'r', encoding='utf-8') as f:
    parser.feed(f.read())
