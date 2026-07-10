import re

with open('style.css', 'r') as f:
    css = f.read()

# 1. Reduce padding-top in results-header to 28px
res_header_regex = r'(\.results-header \{[^}]+)\}'
match = re.search(res_header_regex, css)
if match:
    old_rh = match.group(0)
    new_rh = re.sub(r'padding-top:\s*\d+px;', 'padding-top: 28px;', old_rh)
    css = css.replace(old_rh, new_rh)

# 2. Reduce margin-bottom in results-nav-bar
nav_bar_regex = r'(\.results-nav-bar \{[^}]+)\}'
match = re.search(nav_bar_regex, css)
if match:
    old_nb = match.group(0)
    new_nb = re.sub(r'margin-bottom:\s*16px;', 'margin-bottom: 8px;', old_nb)
    css = css.replace(old_nb, new_nb)

# 3. Reduce padding in sort-col
sort_regex = r'(\.sort-col \{[^}]+)\}'
match = re.search(sort_regex, css)
if match:
    old_sort = match.group(0)
    new_sort = re.sub(r'padding:\s*\d+px 0;', 'padding: 4px 0;', old_sort)
    css = css.replace(old_sort, new_sort)

with open('style.css', 'w') as f:
    f.write(css)

# Update index.html for sort tab prices
with open('index.html', 'r') as f:
    html = f.read()

html = html.replace('font-size: 14px; font-weight: 800; color: var(--indigo-blue); margin-top: 2px;', 'font-size: 13px; font-weight: 800; color: var(--indigo-blue); margin-top: 0px;')
html = html.replace('font-size: 14px; font-weight: 800; color: var(--indigo-navy); margin-top: 2px;', 'font-size: 13px; font-weight: 800; color: var(--indigo-navy); margin-top: 0px;')

with open('index.html', 'w') as f:
    f.write(html)

print("Applied final space reductions.")
