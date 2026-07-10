import re

with open('style.css', 'r') as f:
    css = f.read()

# 1. Add transform to iphone-screen to make it the fixed containing block
if 'transform: translateZ(0);' not in css:
    css = css.replace('.iphone-screen {\n    width: 100%;\n    height: 100%;', '.iphone-screen {\n    width: 100%;\n    height: 100%;\n    transform: translateZ(0);')

# 2. Change drawer and backdrop back to position: fixed
css = css.replace('.bottom-sheet-drawer {\n    position: absolute;\n    bottom: 0;', '.bottom-sheet-drawer {\n    position: fixed;\n    bottom: 0;')
css = css.replace('.bottom-sheet-backdrop {\n    position: absolute;\n    top: 0;', '.bottom-sheet-backdrop {\n    position: fixed;\n    top: 0;')

with open('style.css', 'w') as f:
    f.write(css)

print("Fixed CSS containing block!")
