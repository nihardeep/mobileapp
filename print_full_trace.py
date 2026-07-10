from html.parser import HTMLParser

class Tracer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.closes = []

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            _id = next((v for k, v in attrs if k == 'id'), "")
            _class = next((v for k, v in attrs if k == 'class'), "")
            self.stack.append((_id, _class, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.stack:
                popped = self.stack.pop()
                if popped[0] in ['appContent', 'screenHome', 'homeContentContainer', 'travelOnTapSection', 'trendingDestinationsSection', 'communitiesSection']:
                    print(f"CLOSED {popped[0]} (opened at {popped[2]}) at line {self.getpos()[0]}")

with open('index.html', 'r') as f:
    html = f.read()

t = Tracer()
t.feed(html)
