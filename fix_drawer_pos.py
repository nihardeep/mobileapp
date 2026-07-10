import re

with open('style.css', 'r') as f:
    css = f.read()

# Change drawer to position: fixed so it doesn't get pushed down by scrolling app-content
css = css.replace('.bottom-sheet-drawer {\n    position: absolute;\n    bottom: 0;', '.bottom-sheet-drawer {\n    position: fixed;\n    bottom: 0;')

with open('style.css', 'w') as f:
    f.write(css)

print("Fixed drawer positioning!")
