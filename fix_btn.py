import re

with open('index.html', 'r') as f:
    html = f.read()

def replace_btn(m):
    inner = m.group(1)
    inner = inner.replace('style="', 'style="border: none; background: transparent; padding: 0; outline: none; ')
    return f'<button class="passenger-add-btn" {inner}>Add details &gt;</button>'

html = re.sub(r'<div class="passenger-add-btn" (.*?)>Add details &gt;</div>', replace_btn, html)
html = html.replace('app.js?v=19', 'app.js?v=20')

with open('index.html', 'w') as f:
    f.write(html)
