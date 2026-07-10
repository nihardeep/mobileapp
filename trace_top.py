from html.parser import HTMLParser

class Tracer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.found_pax = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            _id = next((v for k, v in attrs if k == 'id'), "")
            _class = next((v for k, v in attrs if k == 'class'), "")
            self.stack.append((_id, _class, self.getpos()[0]))
            if _id == 'paxDetailsDrawerModal':
                print(f"Found paxDetailsDrawerModal at line {self.getpos()[0]}. Hierarchy:")
                for item in self.stack:
                    print(f"  {item}")

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.stack:
                self.stack.pop()

t = Tracer()
t.feed(open('index.html').read())
