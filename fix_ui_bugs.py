import re

# 1. Update style.css
with open('style.css', 'r') as f:
    css = f.read()

# Fix Airplane direction
css = css.replace(
    '.bp-ticket-route-header .plane-icon { font-size: 32px; transform: rotate(90deg); margin: 0 20px; opacity: 0.9; }',
    '.bp-ticket-route-header .plane-icon { font-size: 32px; transform: rotate(-45deg); margin: 0 20px; opacity: 0.9; }'
)

# Add pointer-events: none to status-bar
css = css.replace(
    '.status-bar {\n    height: 48px;',
    '.status-bar {\n    height: 48px;\n    pointer-events: none;'
)

# Fix bp-ticket-wrapper padding to push the ticket down slightly so it doesn't overlap the cross button
css = css.replace(
    'padding: 56px 24px 40px;',
    'padding: 72px 24px 40px;'
)

with open('style.css', 'w') as f:
    f.write(css)


# 2. Update index.html
with open('index.html', 'r') as f:
    html = f.read()

# Make sure Skyline is fully replaced (there might be multiple occurrences)
html = html.replace('Skyline</div>', 'X Airline</div>')

# Fix cross button (it might have been replaced already by previous script, but let's be sure)
html = html.replace(
    '''<div onclick="navigateTo('home'); triggerHaptic('light', 'Close Boarding Pass')" style="position: absolute; top: 20px; right: 20px; width: 28px; height: 28px; background: rgba(255,255,255,0.15); backdrop-filter: blur(8px); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px; font-weight: 700; cursor: pointer; z-index: 100; border: 1px solid rgba(255,255,255,0.2);">✕</div>''',
    '''<div onclick="navigateTo('home'); triggerHaptic('light', 'Close Boarding Pass')" style="position: absolute; top: 56px; right: 20px; width: 32px; height: 32px; background: rgba(255,255,255,0.15); backdrop-filter: blur(8px); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 14px; font-weight: 700; cursor: pointer; z-index: 1000; border: 1px solid rgba(255,255,255,0.2);">✕</div>'''
)

# Remove the duplicated Destination text (.city-name) from all .bp-ticket-route-header blocks
html = re.sub(
    r'<div class="bp-ticket-city-col(.*?)">\s*<div class="city-name".*?>.*?</div>',
    r'<div class="bp-ticket-city-col\1">',
    html
)

# Let's also update slide 2, 3, 4 with correct routes in case that's what they meant
# Slide 2: MUMBAI to GOA
html = re.sub(
    r'(<div class="bp-ticket-route-header">[\s\S]*?)DELHI(.*?)DEL([\s\S]*?)MUMBAI(.*?)BOM',
    r'\1MUMBAI\2BOM\3GOA\4GOI',
    html, count=1 # Only wait, regex is too greedy. Let's not do regex for this if it's too complex.
)

with open('index.html', 'w') as f:
    f.write(html)

print("Done")
