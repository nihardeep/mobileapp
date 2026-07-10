import re

# 1. index.html teardown
with open('index.html', 'r') as f:
    html = f.read()
html = re.sub(r'<div class="screen" id="screenAddons">.*?(?=<div class="screen" id="screenDestinationAI">)', '', html, flags=re.DOTALL)
with open('index.html', 'w') as f:
    f.write(html)

# 2. style.css teardown
with open('style.css', 'r') as f:
    css = f.read()
css = re.sub(r'/\* ==========================================================================\n   ADD-ONS SCREEN\n   ========================================================================== \*/.*', '', css, flags=re.DOTALL)
with open('style.css', 'w') as f:
    f.write(css)

# 3. app.js teardown
with open('app.js', 'r') as f:
    js = f.read()
js = re.sub(r'// ==========================================================================\n// ADD-ONS SCREEN LOGIC\n// ==========================================================================.*', '', js, flags=re.DOTALL)
with open('app.js', 'w') as f:
    f.write(js)

