import re

# Fix style.css
with open('style.css', 'r') as f:
    css = f.read()

# 1. status-bar absolute fix
status_bar_regex = r'(\.status-bar \{[^}]+)\}'
match = re.search(status_bar_regex, css)
if match:
    old_sb = match.group(0)
    if 'position: absolute;' not in old_sb:
        new_sb = old_sb.replace('}', '    position: absolute;\n    top: 0;\n    left: 0;\n    width: 100%;\n}')
        css = css.replace(old_sb, new_sb)

# 2. Reduce date-pill size
pill_regex = r'(\.date-pill \{[^}]+)\}'
match = re.search(pill_regex, css)
if match:
    old_pill = match.group(0)
    new_pill = re.sub(r'padding:\s*8px 12px;', 'padding: 6px 10px;', old_pill)
    css = css.replace(old_pill, new_pill)

# 3. Reduce sort tabs size
sort_regex = r'(\.sort-col \{[^}]+)\}'
match = re.search(sort_regex, css)
if match:
    old_sort = match.group(0)
    new_sort = re.sub(r'padding:\s*10px 0;', 'padding: 6px 0;', old_sort)
    css = css.replace(old_sort, new_sort)

sort_row_regex = r'(\.results-sort-row \{[^}]+)\}'
match = re.search(sort_row_regex, css)
if match:
    old_sort_row = match.group(0)
    new_sort_row = re.sub(r'margin-bottom:\s*12px;', 'margin-bottom: 8px;', old_sort_row)
    css = css.replace(old_sort_row, new_sort_row)

with open('style.css', 'w') as f:
    f.write(css)

# Fix index.html inline margins
with open('index.html', 'r') as f:
    html = f.read()

# Reduce marquee margins
html = html.replace('margin-top: 8px; margin-bottom: 12px;', 'margin-top: 4px; margin-bottom: 8px;')

with open('index.html', 'w') as f:
    f.write(html)

print("Applied space optimization fixes successfully!")
