import re

with open('style.css', 'r') as f:
    css = f.read()

# Remove transform: translateZ(0);
css = css.replace('transform: translateZ(0);', '')

with open('style.css', 'w') as f:
    f.write(css)

print("Reverted translateZ(0)")
