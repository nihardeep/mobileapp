import re

with open('index.html', 'r') as f:
    html = f.read()
html = html.replace('id="passengerFormSheet"', 'id="paxDetailsDrawerModal"')
with open('index.html', 'w') as f:
    f.write(html)

with open('app.js', 'r') as f:
    js = f.read()
js = js.replace('passengerFormSheet', 'paxDetailsDrawerModal')
with open('app.js', 'w') as f:
    f.write(js)

with open('style.css', 'r') as f:
    css = f.read()
css = css.replace('passengerFormSheet', 'paxDetailsDrawerModal')
with open('style.css', 'w') as f:
    f.write(css)
