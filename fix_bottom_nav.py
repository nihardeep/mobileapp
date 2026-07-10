with open('index.html', 'r') as f:
    html = f.read()

target = "                <!-- Bottom Navigation Bar -->\n                <div class=\"bottom-nav\">"
replacement = "                </div> <!-- End appContent -->\n\n                <!-- Bottom Navigation Bar -->\n                <div class=\"bottom-nav\">"

html = html.replace(target, replacement)

with open('index.html', 'w') as f:
    f.write(html)
