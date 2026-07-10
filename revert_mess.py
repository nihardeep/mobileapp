import re

with open('style.css', 'r') as f:
    css = f.read()

# Revert the blind visibility additions
css = css.replace('transform: translateY(100%);\n    visibility: hidden;', 'transform: translateY(100%);')
css = css.replace('transform: translateY(0);\n    visibility: visible;', 'transform: translateY(0);')

# ONLY add it to .bottom-sheet-drawer cleanly
# We will do this via a precise regex or just string replacement
css = css.replace(""".bottom-sheet-drawer {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    max-height: 70%;
    background: #fff;
    border-top-left-radius: 24px;
    border-top-right-radius: 24px;
    z-index: 1000;
    padding: 16px;
    transform: translateY(100%);""", """.bottom-sheet-drawer {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    max-height: 70%;
    background: #fff;
    border-top-left-radius: 24px;
    border-top-right-radius: 24px;
    z-index: 1000;
    padding: 16px;
    transform: translateY(100%);
    visibility: hidden;""")

css = css.replace(""".bottom-sheet-drawer.visible {
    transform: translateY(0);""", """.bottom-sheet-drawer.visible {
    transform: translateY(0);
    visibility: visible;""")

# Revert Safari hack on iphone-screen
css = css.replace("""    overflow: hidden;
    -webkit-mask-image: -webkit-radial-gradient(white, black);
    mask-image: radial-gradient(white, black);
    transform: translateZ(0);""", """    overflow: hidden;""")

with open('style.css', 'w') as f:
    f.write(css)

print("Reverted messy CSS!")
