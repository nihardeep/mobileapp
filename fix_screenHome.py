with open('index.html', 'r') as f:
    html = f.read()

# I will insert one </div> before SCREEN 2: OFFERS & DEALS
target = "<!-- ==========================================================\n                         SCREEN 2: OFFERS & DEALS"
replacement = "                    </div>\n                    " + target

html = html.replace(target, replacement)

with open('index.html', 'w') as f:
    f.write(html)
