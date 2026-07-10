import re

with open('style.css', 'r') as f:
    css = f.read()

new_badge_css = """
.fc-edge-badge {
    position: absolute;
    top: -8px;
    right: 16px;
    background: #FDF7E7;
    color: #D4AF37;
    border: 1px solid rgba(212, 175, 55, 0.3);
    font-size: 9px;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.05);
}
"""

if '.fc-edge-badge' not in css:
    css += '\n' + new_badge_css
    with open('style.css', 'w') as f:
        f.write(css)

with open('app.js', 'r') as f:
    js = f.read()

# Replace the edgeBadgeHtml logic in app.js
old_badge_logic = """        let edgeBadgeHtml = "";
        // Removed edge badge from search page as requested"""

new_badge_logic = """        let edgeBadgeHtml = "";
        if (i === 1) {
            edgeBadgeHtml = `<div class="fc-edge-badge">
                <svg viewBox="0 0 24 24" width="10" height="10" fill="currentColor"><path d="M12 2l2.4 7.6L22 12l-7.6 2.4L12 22l-2.4-7.6L2 12l7.6-2.4L12 2z"/></svg> RECOMMENDED FARE
            </div>`;
        }
"""

js = js.replace(old_badge_logic, new_badge_logic)

with open('app.js', 'w') as f:
    f.write(js)

print("Restored recommendation badge")
