import re

with open('style.css', 'r') as f:
    css = f.read()

# Reduce results-header padding-top
res_header_regex = r'(\.results-header \{[^}]+)\}'
match = re.search(res_header_regex, css)
if match:
    old_rh = match.group(0)
    new_rh = re.sub(r'padding-top:\s*56px;', 'padding-top: 40px;', old_rh)
    css = css.replace(old_rh, new_rh)
    print("Reduced results-header padding-top to 40px")

with open('style.css', 'w') as f:
    f.write(css)
