import re

with open('style.css', 'r') as f:
    css = f.read()

# Revert drawer to position: absolute
css = css.replace('.bottom-sheet-drawer {\n    position: fixed;\n    bottom: 0;', '.bottom-sheet-drawer {\n    position: absolute;\n    bottom: 0;')

with open('style.css', 'w') as f:
    f.write(css)

print("Reverted position fixed")
