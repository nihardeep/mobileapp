import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Cab Deals padding and alignment
content = content.replace(
    '<div id="companionCabDeals" style="margin-top: 16px; display: none; padding: 0 12px; order: 4;">',
    '<div id="companionCabDeals" style="margin-top: 16px; display: none; padding: 0 4px; order: 4;">'
)

# 2. Cab Deals card height and Cab image
content = content.replace(
    'cursor: pointer; min-height: 80px;">',
    'cursor: pointer; min-height: 105px;">'
)
content = content.replace(
    'right: -5px; bottom: -15px; width: 135px;',
    'right: -10px; bottom: -5px; width: 165px;'
)

# 3. Hotel Deals padding
content = content.replace(
    '<div style="padding: 0 20px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">',
    '<div style="padding: 0 4px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">'
)
# Make sure we also update the Hotel Deals 'View All' link if it had its own padding or something. 
# Looking at grep output, it just had padding 0 20px on the flex container.

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated alignments and cab card")
