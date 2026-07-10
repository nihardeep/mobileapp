import re
with open('index.html', 'r') as f:
    html = f.read()

start_str = '<div class="iphone-screen">'
end_str = '<!-- Parallax Atmospheric Background -->'
drawers_block = html[html.find(start_str)+len(start_str):html.find(end_str)]

drawers = re.split(r'(?=<div[^>]*class="[^"]*bottom-sheet-(?:drawer|backdrop))', drawers_block)

for d in drawers:
    if 'id="addonBenefitsDrawer"' in d:
        print(d)
        break
