import re
with open('index.html', 'r') as f:
    lines = f.readlines()

depth = 0
for i, line in enumerate(lines):
    divs_open = len(re.findall(r'<div', line))
    divs_close = len(re.findall(r'</div', line))
    depth += (divs_open - divs_close)

print("Final Document Depth:", depth)
