import re
with open('index.html', 'r') as f:
    html = f.read()

# Find the rogue script tag
rogue_script = r'<script src="app.js\?v=\d+"></script>'
html = re.sub(rogue_script, '', html)

# Clean up empty lines
html = re.sub(r'\n\s*\n\s*\n', '\n\n', html)

with open('index.html', 'w') as f:
    f.write(html)
