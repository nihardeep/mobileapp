from html.parser import HTMLParser

class BalanceChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.in_drawers = False
        self.drawers_balance = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1
            if self.in_drawers:
                self.drawers_balance += 1
    
    def handle_endtag(self, tag):
        if tag == 'div':
            self.depth -= 1
            if self.in_drawers:
                self.drawers_balance -= 1

checker = BalanceChecker()
with open('index.html', 'r') as f:
    html = f.read()

# Extract the block we inserted
start_str = '<div class="iphone-screen">'
end_str = '<!-- Parallax Atmospheric Background -->'
start = html.find(start_str)
end = html.find(end_str)

drawers_block = html[start + len(start_str):end]

checker.in_drawers = True
checker.feed(drawers_block)

print(f"Drawers block div balance: {checker.drawers_balance}")
