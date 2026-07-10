with open('index.html', 'r') as f:
    html = f.read()

target = "                    </div>\n                    <!-- ==========================================================\n                         SCREEN 2: OFFERS & DEALS"
replacement = "<!-- ==========================================================\n                         SCREEN 2: OFFERS & DEALS"

html = html.replace(target, replacement)

with open('index.html', 'w') as f:
    f.write(html)
