import re

with open('app.js', 'r') as f:
    js = f.read()

# remove references to bottomContent
js = js.replace("const bottomContent = document.getElementById('homeBottomContent');", "")
js = js.replace("if (bottomContent) bottomContent.classList.add('hidden');", "")

with open('app.js', 'w') as f:
    f.write(js)
