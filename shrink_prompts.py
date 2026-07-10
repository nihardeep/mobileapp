import re

with open('index.html', 'r') as f:
    html = f.read()

# Make a backup
with open('index.html.bak', 'w') as f:
    f.write(html)

# Replace section padding
html = html.replace('padding: 24px; box-shadow', 'padding: 16px; box-shadow')

# Replace title styles
html = html.replace('font-size: 13px; font-weight: 800; color: #5a6b82; letter-spacing: 0.5px; margin-bottom: 20px;', 'font-size: 11px; font-weight: 800; color: #5a6b82; letter-spacing: 0.5px; margin-bottom: 10px;')

# Replace card padding and gap
html = html.replace('gap: 16px; padding: 12px 0;', 'gap: 12px; padding: 8px 0;')

# Replace icon sizing
html = html.replace('width: 56px; height: 56px;', 'width: 38px; height: 38px;')
html = html.replace('font-size: 28px;', 'font-size: 20px;')
html = html.replace('border-radius: 16px;', 'border-radius: 10px;')

# Replace tag sizing
html = html.replace('font-size: 10px; font-weight: 700; padding: 4px 8px;', 'font-size: 9px; font-weight: 700; padding: 3px 6px;')
html = html.replace('width="12" height="12"', 'width="10" height="10"')
html = html.replace('margin-bottom: 6px;', 'margin-bottom: 4px;')

# Replace text sizing
html = html.replace('font-size: 15px;', 'font-size: 13px;')

with open('index.html', 'w') as f:
    f.write(html)
print("Shrunk trending prompts section!")
