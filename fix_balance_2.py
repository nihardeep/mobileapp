from html.parser import HTMLParser

class StructurePrinter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'div': self.depth += 1

    def handle_endtag(self, tag):
        if tag == 'div': self.depth -= 1

with open('index.html', 'r') as f:
    html = f.read()

checker = StructurePrinter()
checker.feed(html)
print(f"Initial balance: {checker.depth}")

if checker.depth > 0:
    # We are missing a closing div. 
    # Let's insert it at the end of the bluchip-bottom-layout that I just inserted.
    # I inserted a block ending with:
    # "                                            </div>\n                                        </div>\n"
    target = '                                            </div>\n                                        </div>\n'
    replacement = '                                            </div>\n                                        </div>\n                                    </div>\n'
    html = html.replace(target, replacement, 1)
    
    with open('index.html', 'w') as f:
        f.write(html)
        
    checker2 = StructurePrinter()
    checker2.feed(html)
    print(f"Final balance: {checker2.depth}")
else:
    print("Balance is zero, doing nothing.")

