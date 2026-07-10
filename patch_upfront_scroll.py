import re

with open('index.html', 'r') as f:
    html = f.read()

old_header = """<div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 24px;">
                            <h2 style="font-size: 20px; font-weight: 900; color: #001B94; font-style: italic; margin: 0;">UpFront Benefits</h2>
                        </div>"""
                        
new_header = """<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                            <h2 style="font-size: 20px; font-weight: 900; color: #001B94; font-style: italic; margin: 0;">UpFront Benefits</h2>
                            <div style="width: 32px; height: 32px; background: #f1f5f9; border-radius: 16px; display: flex; align-items: center; justify-content: center; color: #64748b; font-size: 14px; cursor: pointer;" onclick="closeAllDrawers()">✕</div>
                        </div>"""

html = html.replace(old_header, new_header)

with open('index.html', 'w') as f:
    f.write(html)


with open('app.js', 'r') as f:
    js = f.read()

# Add scroll listener to initAddonsScreen
# Find where initAddonsScreen starts
init_marker = "function initAddonsScreen() {"
init_pos = js.find(init_marker)

if init_pos != -1:
    scroll_logic = """
    window.hasAutoOpenedUpfront = false;
    const feed = document.getElementById('addonsMainFeed');
    if (feed) {
        // Remove any old listener just in case
        feed.onscroll = function() {
            if (!window.hasAutoOpenedUpfront && feed.scrollTop > 120) {
                // Check if already upgraded
                const statusText = document.getElementById('upfront-status-text');
                if (statusText && statusText.innerText.includes('Upgraded')) return;
                
                window.hasAutoOpenedUpfront = true;
                const drawer = document.getElementById('addonBenefitsDrawer');
                const backdrop = document.getElementById('bottomSheetBackdrop');
                if (drawer && backdrop) {
                    drawer.classList.add('visible');
                    backdrop.classList.add('visible');
                }
            }
        };
    }
"""
    js = js[:init_pos + len(init_marker)] + scroll_logic + js[init_pos + len(init_marker):]

with open('app.js', 'w') as f:
    f.write(js)
