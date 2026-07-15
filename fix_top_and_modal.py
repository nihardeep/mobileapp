import re

# 1. Update style.css
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Fix top padding
css = css.replace('padding: 0 24px 40px;', 'padding: 56px 24px 40px;')

# Fix modal position
css = css.replace('position: fixed;\n    top: 0; left: 0; width: 100%; height: 100%;\n    background: rgba(255,255,255,0.98);\n    z-index: 9999;', 
                  'position: absolute;\n    top: 0; left: 0; width: 100%; height: 100%;\n    background: rgba(4, 16, 41, 0.95); /* dark theme modal */\n    z-index: 999999;\n    color: white;')

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make sure we move the modal outside of screenTrips and directly into iphone-screen if needed, 
# but position: absolute will work inside screenTrips as long as screenTrips is full height.
# Actually, screenTrips is full height. But wait, screenTrips has overflow-y: auto. 
# An absolute element inside a scrolling container will scroll with it!
# Let's move bpQrFullscreen out of screenTrips and put it just before the end of #appContent or #iphoneScreen.

modal_start = html.find('<!-- Full Screen QR Modal -->')
if modal_start != -1:
    modal_end = html.find('</div>', html.find('</div>', html.find('</div>', modal_start) + 1) + 1) + 6
    modal_html = html[modal_start:modal_end]
    
    # Remove from current location
    html = html[:modal_start] + html[modal_end:]
    
    # Insert right before closing #iphoneScreen or #appContent
    # Let's insert before <!-- Bottom Navigation -->
    insert_point = html.find('<!-- Bottom Navigation -->')
    if insert_point != -1:
        html = html[:insert_point] + modal_html + '\n' + html[insert_point:]
        
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Fixed top padding and modal location")
