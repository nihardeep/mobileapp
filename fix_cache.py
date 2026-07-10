import re

with open('index.html', 'r') as f:
    html = f.read()

# Add cache busters
html = html.replace('src="app.js"', 'src="app.js?v=2"')
html = html.replace('href="style.css"', 'href="style.css?v=2"')

with open('index.html', 'w') as f:
    f.write(html)
