import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace the onclick of the X button
old_x_btn = """<div style="width: 32px; height: 32px; background: #f1f5f9; border-radius: 16px; display: flex; align-items: center; justify-content: center; color: #64748b; font-size: 14px; cursor: pointer;" onclick="closeUpfrontDrawerAndShowBanner()">✕</div>"""
new_x_btn = """<div style="width: 32px; height: 32px; background: #f1f5f9; border-radius: 16px; display: flex; align-items: center; justify-content: center; color: #64748b; font-size: 14px; cursor: pointer;" onclick="closeAllDrawers(); var b = document.getElementById('upfront-sticky-banner'); if(b) b.style.display='flex';">✕</div>"""

if old_x_btn in html:
    html = html.replace(old_x_btn, new_x_btn)
else:
    print("WARNING: Could not find old_x_btn to replace.")

# Also update the backdrop just in case they click that!
old_backdrop = """<div class="bottom-sheet-backdrop" id="bottomSheetBackdrop" onclick="closeAllDrawers()"></div>"""
new_backdrop = """<div class="bottom-sheet-backdrop" id="bottomSheetBackdrop" onclick="closeAllDrawers(); var b = document.getElementById('upfront-sticky-banner'); if(b && window.hasAutoOpenedUpfront) b.style.display='flex';"></div>"""

if old_backdrop in html:
    html = html.replace(old_backdrop, new_backdrop)
else:
    print("WARNING: Could not find old_backdrop to replace.")

with open('index.html', 'w') as f:
    f.write(html)
