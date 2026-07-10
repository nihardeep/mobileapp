import re

with open('style.css', 'r') as f:
    css = f.read()

# Fix pnr-main-card padding
css = re.sub(r'(\.pnr-main-card\s*\{[^}]*padding:\s*)14px(;\s*)', r'\g<1>12px\g<2>', css)

# Fix companion-subcard padding
css = re.sub(r'(\.companion-subcard\s*\{[^}]*padding:\s*)12px(;\s*)', r'\g<1>10px\g<2>', css)

# Fix pnr-time font-size
css = re.sub(r'(\.pnr-time\s*\{[^}]*font-size:\s*)17px(;\s*)', r'\g<1>15px\g<2>', css)

# Fix pnr-duration margin-top
css = re.sub(r'(\.pnr-duration\s*\{[^}]*margin-top:\s*)4px(;\s*)', r'\g<1>8px\g<2>', css)

# Add a bit of top margin to pnr-arrow-line to push it slightly up from the duration text
css = re.sub(r'(\.pnr-arrow-line\s*\{[^}]*position:\s*relative;)', r'\g<1>\n    top: -2px;', css)

with open('style.css', 'w') as f:
    f.write(css)
