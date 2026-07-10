import re

# 1. Update style.css for banner text color
with open('style.css', 'r') as f:
    css = f.read()

# Make the description color dark so it's visible on light background
if '.shb-desc' not in css:
    css += """
.shb-desc {
    color: #5a6b82;
    font-size: 11px;
    font-weight: 500;
}
.shb-title {
    color: var(--indigo-navy);
}
"""
else:
    # If it exists, update it. I'll just append it with higher specificity or !important
    css += """
.shb-desc { color: #5a6b82 !important; font-weight: 600 !important; }
.shb-title { color: var(--indigo-navy) !important; font-weight: 800 !important; }
"""

# Add style for the close button
css += """
.shb-close {
    font-size: 16px;
    color: #5a6b82;
    cursor: pointer;
    padding: 4px;
    margin-left: 8px;
    opacity: 0.6;
}
.shb-close:hover { opacity: 1; }
"""

with open('style.css', 'w') as f:
    f.write(css)

# 2. Update index.html to add the cross
with open('index.html', 'r') as f:
    html = f.read()

# Add the X close button inside the banner
old_banner = """<div class="shb-cta">Search ➔</div>"""
new_banner = """<div class="shb-cta">Search ➔</div>
                                    <div class="shb-close" onclick="event.stopPropagation(); toggleStudentPersona()">✖</div>"""

html = html.replace(old_banner, new_banner)

with open('index.html', 'w') as f:
    f.write(html)

print("Fixed banner styles and added close button!")
