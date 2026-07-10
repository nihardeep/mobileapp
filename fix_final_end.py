import re

with open('index.html', 'r') as f:
    html = f.read()

# Find the Compare Fares modal end or the start of the duplicated end.
# A safe way is to find the LAST occurrence of "Compare Fares Modal" block.
# Actually, let's just find the first "    <script src=\"app.js?v=17\"></script>"
# and trim everything from there onwards.

idx = html.find('    <script src="app.js?v=17"></script>')
if idx != -1:
    # also remove any </div> that I added right before it if it was part of the replace
    # let's just trace depth from 0 to idx, see what the depth is, and add EXACTLY that many </div>
    pass

from html.parser import HTMLParser

class BalanceFixer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.lines = []

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.depth += 1

    def handle_endtag(self, tag):
        if tag == 'div':
            self.depth -= 1

# First, trim everything after the FIRST <script src="app.js
script_idx = html.find('<script src="app.js')
if script_idx != -1:
    # let's look a bit before script_idx to see if there are stray </div> tags.
    # The clean way is to split the HTML right before `<!-- Bulk Add Passenger Sheet -->` or something?
    # No, `<!-- Bulk Add Passenger Sheet -->` is before the end.
    html_trimmed = html[:script_idx]
    
    # let's count balance of html_trimmed
    fixer = BalanceFixer()
    fixer.feed(html_trimmed)
    
    # close any remaining open divs
    while fixer.depth > 0:
        html_trimmed += '</div>\n'
        fixer.depth -= 1
        
    # Now add the script, audio, body, html
    html_trimmed += """
    <script src="app.js?v=17"></script>

    <!-- Haptic audio simulation nodes -->
    <audio id="sndTap" src="https://assets.mixkit.co/active_storage/sfx/2568/2568-84.wav" preload="auto"></audio>
    <audio id="sndConfirm" src="https://assets.mixkit.co/active_storage/sfx/2019/2019-84.wav" preload="auto"></audio>
    <audio id="sndAlert" src="https://assets.mixkit.co/active_storage/sfx/911/911-84.wav" preload="auto"></audio>

</body>
</html>
"""
    with open('index.html', 'w') as f:
        f.write(html_trimmed)

