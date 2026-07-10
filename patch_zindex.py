import re

with open('style.css', 'r') as f:
    css = f.read()

# Fix bottom drawer z-index so it definitely is ABOVE screenAddons
# screenAddons is at z-index: 200.
old_drawer = """.bottom-sheet-drawer {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    background: #ffffff;
    border-radius: 30px 30px 0 0;
    z-index: 2000;"""

new_drawer = """.bottom-sheet-drawer {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    background: #ffffff;
    border-radius: 30px 30px 0 0;
    z-index: 9999;"""

css = css.replace(old_drawer, new_drawer)

with open('style.css', 'w') as f:
    f.write(css)

# Also update backdrop to be super high
with open('app.js', 'r') as f:
    js = f.read()

js = js.replace('backdrop.style.zIndex = \'1999\';', 'backdrop.style.zIndex = \'9998\';')

with open('app.js', 'w') as f:
    f.write(js)
