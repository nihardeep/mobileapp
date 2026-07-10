from html.parser import HTMLParser
import os

class DrawerExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.drawers = {}
        self.current_drawer = None
        self.drawer_depth = 0
        self.raw_html = ""
        self.capture_buffer = []

    def feed(self, data):
        self.raw_html = data
        super().feed(data)

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        classes = attr_dict.get('class', '')
        id_ = attr_dict.get('id', '')
        
        start_tag_str = self.get_starttag_text()
        
        if 'bottom-sheet-drawer' in classes or id_ == 'bottomSheetBackdrop':
            if self.current_drawer is None:
                self.current_drawer = id_ if id_ else 'backdrop'
                self.drawer_depth = 1
                self.capture_buffer.append(start_tag_str)
                return
                
        if self.current_drawer:
            self.drawer_depth += 1
            if tag not in ['img', 'br', 'hr', 'input', 'meta', 'link']:
                self.capture_buffer.append(start_tag_str)
            else:
                self.capture_buffer.append(start_tag_str)

    def handle_endtag(self, tag):
        if self.current_drawer:
            if tag not in ['img', 'br', 'hr', 'input', 'meta', 'link']:
                self.drawer_depth -= 1
                self.capture_buffer.append(f"</{tag}>")
                
                if self.drawer_depth == 0:
                    self.drawers[self.current_drawer] = "".join(self.capture_buffer)
                    self.current_drawer = None
                    self.capture_buffer = []

    def handle_data(self, data):
        if self.current_drawer:
            self.capture_buffer.append(data)

    def handle_entityref(self, name):
        if self.current_drawer:
            self.capture_buffer.append(f"&{name};")

    def handle_charref(self, name):
        if self.current_drawer:
            self.capture_buffer.append(f"&#{name};")

with open('index.html', 'r') as f:
    html = f.read()

extractor = DrawerExtractor()
extractor.feed(html)

print(f"Extracted {len(extractor.drawers)} elements.")

# Now, let's remove these exactly from the HTML
for drawer_id, drawer_html in extractor.drawers.items():
    html = html.replace(drawer_html, '')
    print(f"Removed {drawer_id}")

# Find the end of iphone-screen
# We'll just look for the end of the file and insert them before the last </div></div></div>
# Actually, the easiest way to ensure they work is to place them right before <script src="app.js">
# Because iphone-screen's closing tags might be messed up anyway.
# BUT they must be inside .iphone-screen if we want them clipped.
# Let's just put them at the very end of the <body>. They don't technically need to be in .iphone-screen 
# if they are position: absolute; bottom: 0 and width: 100%. Wait, if they are outside iphone-screen, 
# they will be relative to phone-container. And phone-container has the exact same dimensions!

insertion_point = html.rfind('<!-- Haptic audio simulation nodes -->')

all_drawers_html = "\n\n<!-- ALL BOTTOM SHEET DRAWERS -->\n" + "\n".join(extractor.drawers.values()) + "\n\n"

new_html = html[:insertion_point] + all_drawers_html + html[insertion_point:]

with open('index.html.fixed', 'w') as f:
    f.write(new_html)

os.system('mv index.html.fixed index.html')
print("Successfully fixed HTML structure!")
