from html.parser import HTMLParser

class BalanceFixer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.lines = []
        self.invalid_lines = []

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1

    def handle_endtag(self, tag):
        if tag == 'div':
            self.depth -= 1
            if self.depth < 0:
                self.invalid_lines.append(self.getpos()[0])
                self.depth = 0

with open('index.html', 'r') as f:
    html = f.read()

fixer = BalanceFixer()
fixer.feed(html)

print("Invalid lines:", fixer.invalid_lines)

lines = html.split('\n')
for line_num in reversed(fixer.invalid_lines):
    # line_num is 1-indexed
    idx = line_num - 1
    # Replace the first </div> on this line with empty string or something
    # Actually, if we just parse and reconstruct, it's safer, but string manipulation is ok for single tags per line
    if '</div>' in lines[idx]:
        lines[idx] = lines[idx].replace('</div>', '', 1)

with open('index.html', 'w') as f:
    f.write('\n'.join(lines))

