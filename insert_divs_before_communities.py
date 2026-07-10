with open('index.html', 'r') as f:
    html = f.read()

target = "<!-- Explore Communities -->"
replacement = "</div>\n                            </div>\n                            " + target

html = html.replace(target, replacement, 1)

with open('index.html', 'w') as f:
    f.write(html)
