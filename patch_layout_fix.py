import re

with open('index.html', 'r') as f:
    html = f.read()

# Fix 1: Addons screen z-index to cover main nav
html = html.replace('<div class="screen" id="screenAddons" style="background: #f8fafc;">', '<div class="screen" id="screenAddons" style="background: #f8fafc; z-index: 200;">')

# Fix 2: Change position: fixed to position: absolute for UpFront Banner
html = html.replace('<!-- Premium Metallic UpFront Banner -->\\n    <div style="position: fixed; bottom: 85px;', '<!-- Premium Metallic UpFront Banner -->\\n    <div style="position: absolute; bottom: 85px;')

# Fix 3: Change position: fixed to position: absolute for Sticky Checkout Bar
html = html.replace('<!-- Sticky Bottom Checkout Bar -->\\n    <div style="position: fixed; bottom: 0;', '<!-- Sticky Bottom Checkout Bar -->\\n    <div style="position: absolute; bottom: 0;')

with open('index.html', 'w') as f:
    f.write(html)
