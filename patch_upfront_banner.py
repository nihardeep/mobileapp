import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Hide the sticky banner and give it an ID, and add the onclick to "See Benefits"
old_banner = """    <!-- Premium Metallic UpFront Banner -->
    <div style="position: absolute; bottom: 85px; left: 16px; right: 16px; background: linear-gradient(135deg, #f8fafc, #e2e8f0); border: 1px solid #cbd5e1; border-radius: 12px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; z-index: 100; box-shadow: 0 -4px 20px rgba(0,0,0,0.05);">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: linear-gradient(135deg, #001b94, #2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; font-size: 16px; font-style: italic;">UpFront</div>
            <div id="upfront-status-text" style="font-size: 11px; font-weight: 700; color: #475569;">Upgrade @ ₹2,499</div>
        </div>
        <div style="font-size: 10px; font-weight: 800; color: var(--indigo-blue); text-transform: uppercase; letter-spacing: 0.5px;">See Benefits ➔</div>
    </div>"""

new_banner = """    <!-- Premium Metallic UpFront Banner -->
    <div id="upfront-sticky-banner" style="display: none; position: absolute; bottom: 85px; left: 16px; right: 16px; background: linear-gradient(135deg, #f8fafc, #e2e8f0); border: 1px solid #cbd5e1; border-radius: 12px; padding: 12px 16px; justify-content: space-between; align-items: center; z-index: 100; box-shadow: 0 -4px 20px rgba(0,0,0,0.05);">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: linear-gradient(135deg, #001b94, #2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; font-size: 16px; font-style: italic;">UpFront</div>
            <div id="upfront-status-text" style="font-size: 11px; font-weight: 700; color: #475569;">Upgrade @ ₹2,499</div>
        </div>
        <div id="upfront-see-benefits-btn" onclick="document.getElementById('addonBenefitsDrawer').classList.add('visible'); document.getElementById('bottomSheetBackdrop').classList.add('visible');" style="font-size: 10px; font-weight: 800; color: var(--indigo-blue); text-transform: uppercase; letter-spacing: 0.5px; cursor: pointer;">See Benefits ➔</div>
    </div>"""

if old_banner in html:
    html = html.replace(old_banner, new_banner)
else:
    print("Could not find the old banner. Maybe it's already modified?")

# 2. Modify the '✕' button on addonBenefitsDrawer to show the sticky banner
old_x_btn = """<div style="width: 32px; height: 32px; background: #f1f5f9; border-radius: 16px; display: flex; align-items: center; justify-content: center; color: #64748b; font-size: 14px; cursor: pointer;" onclick="closeAllDrawers()">✕</div>"""
new_x_btn = """<div style="width: 32px; height: 32px; background: #f1f5f9; border-radius: 16px; display: flex; align-items: center; justify-content: center; color: #64748b; font-size: 14px; cursor: pointer;" onclick="closeUpfrontDrawerAndShowBanner()">✕</div>"""

html = html.replace(old_x_btn, new_x_btn)

with open('index.html', 'w') as f:
    f.write(html)


with open('app.js', 'r') as f:
    js = f.read()

# Add closeUpfrontDrawerAndShowBanner function
new_js = """
window.closeUpfrontDrawerAndShowBanner = function() {
    closeAllDrawers();
    const banner = document.getElementById('upfront-sticky-banner');
    if (banner) {
        banner.style.display = 'flex';
    }
};
"""

js += new_js

with open('app.js', 'w') as f:
    f.write(js)

