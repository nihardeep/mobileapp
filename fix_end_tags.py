with open('index.html', 'r') as f:
    html = f.read()

# Insert </div></div> right before <!-- Compare Fares Modal -->
# Actually, the missing divs are for appContent and iphone-screen. 
# They should probably close right before the compare modal, or right before the script tag.
# Let's just find the last </div> and add two more before the script tag.

target = "    <script src=\"app.js?v=17\"></script>"
replacement = "    </div>\n    </div>\n    <script src=\"app.js?v=17\"></script>"

html = html.replace(target, replacement)

with open('index.html', 'w') as f:
    f.write(html)
