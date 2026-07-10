import re

# 1. Update style.css
with open('style.css', 'r') as f:
    css = f.read()

# Increase padding for pass-chip
css = css.replace('padding: 6px 2px;', 'padding: 10px 4px;')

with open('style.css', 'w') as f:
    f.write(css)

# 2. Update index.html
with open('index.html', 'r') as f:
    html = f.read()

# Replace SEAT / AUTO
html = html.replace('>SEAT<', '>FARE TYPE<')
html = html.replace('>AUTO<', '>Bag lite<')

with open('index.html', 'w') as f:
    f.write(html)

