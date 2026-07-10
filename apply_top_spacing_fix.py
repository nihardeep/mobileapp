import re

with open('style.css', 'r') as f:
    css = f.read()

# 1. Update status-bar
status_bar_regex = r'(\.status-bar \{[^}]+)\}'
match = re.search(status_bar_regex, css)
if match:
    old_sb = match.group(0)
    if 'position: absolute;' not in old_sb:
        new_sb = old_sb.replace('}', '    position: absolute;\n    top: 0;\n    left: 0;\n    width: 100%;\n}')
        css = css.replace(old_sb, new_sb)

# 2. Update home-header
home_header_regex = r'(\.home-header \{[^}]+)\}'
match = re.search(home_header_regex, css)
if match:
    old_hh = match.group(0)
    if 'padding-top: 52px;' not in old_hh:
        new_hh = old_hh.replace('}', '    padding-top: 52px;\n}')
        css = css.replace(old_hh, new_hh)

# 3. Update #screenResults.active
screen_res_regex = r'(#screenResults\.active \{[^}]+)\}'
match = re.search(screen_res_regex, css)
if match:
    old_sr = match.group(0)
    new_sr = """#screenResults.active {
    display: flex;
    flex-direction: column;
    height: 100%;
    margin-top: 0px;
    margin-left: -16px;
    margin-right: -16px;
    margin-bottom: -85px;
    padding-bottom: 85px;
}"""
    css = css.replace(old_sr, new_sr)

# 4. Update .results-header
res_header_regex = r'(\.results-header \{[^}]+)\}'
match = re.search(res_header_regex, css)
if match:
    old_rh = match.group(0)
    new_rh = """.results-header {
    background: #fff;
    padding-top: 56px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    z-index: 10;
    position: relative;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
}"""
    css = css.replace(old_rh, new_rh)

with open('style.css', 'w') as f:
    f.write(css)

print("Applied layout adjustments to fix the blue sky gap securely!")
