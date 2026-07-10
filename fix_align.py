import re

with open('index.html', 'r') as f:
    html = f.read()

# Update Add details button styling
html = html.replace('class="passenger-add-btn"', 'class="passenger-add-btn" style="font-size: 10px; color: var(--indigo-blue); font-weight: 800; text-align: right; margin-left: auto;"')

# Update Edit button styling on Card 1
html = html.replace('<div class="passenger-status" style="font-size: 12px; color: var(--indigo-blue); font-weight: 800;">Edit ✏️</div>', '<div class="passenger-status" style="font-size: 10px; color: var(--indigo-blue); font-weight: 800; text-align: right; margin-left: auto;">Edit ✏️</div>')

# Update Incomplete status on Card 3 so it's pushed right
html = html.replace('<div style="font-size: 10px; font-weight: 800; color: #f59e0b; background: rgba(245, 158, 11, 0.1); padding: 4px 8px; border-radius: 6px;">Incomplete ⚠️</div>', '<div style="font-size: 10px; font-weight: 800; color: #f59e0b; background: rgba(245, 158, 11, 0.1); padding: 4px 8px; border-radius: 6px; text-align: right; margin-left: auto;">Incomplete ⚠️</div>')

with open('index.html', 'w') as f:
    f.write(html)
