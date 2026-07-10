import re

with open('style.css', 'r') as f:
    css = f.read()

target = """.student-hub-header {
    background: linear-gradient(135deg, #FF9900 0%, #FF5E00 100%);
    margin: 0 -16px;
    width: calc(100% + 32px);
    padding: 52px 20px 30px 20px;"""

replacement = """.student-hub-header {
    background: linear-gradient(135deg, #FF9900 0%, #FF5E00 100%);
    margin: -30px -16px 0 -16px;
    width: 361px;
    max-width: 361px;
    padding: 82px 20px 30px 20px;"""

css = css.replace(target, replacement)

with open('style.css', 'w') as f:
    f.write(css)

with open('index.html', 'r') as f:
    html = f.read()
html = html.replace('app.js?v=22', 'app.js?v=23')
with open('index.html', 'w') as f:
    f.write(html)

print("Bleed fixed")
