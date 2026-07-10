import re

with open('app.js', 'r') as f:
    js = f.read()

old_tag = """ecoTagHtml = '<span style="font-size: 9px; background: rgba(14, 165, 233, 0.08); color: var(--indigo-blue); padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(14, 165, 233, 0.2);">Extra benefits</span>';"""
new_tag = """ecoTagHtml = '<span onclick="openStudentBenefitsDrawer(event)" style="font-size: 9px; background: rgba(14, 165, 233, 0.08); color: var(--indigo-blue); padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(14, 165, 233, 0.2); cursor: pointer; display: inline-flex; align-items: center; gap: 4px;">Extra benefits <svg viewBox="0 0 24 24" width="10" height="10" fill="currentColor"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 16v-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M12 8h.01" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg></span>';"""

js = js.replace(old_tag, new_tag)

if 'function openStudentBenefitsDrawer' not in js:
    js += """
window.openStudentBenefitsDrawer = function(event) {
    if (event) {
        event.stopPropagation();
    }
    const drawer = document.getElementById('studentBenefitsDrawer');
    const backdrop = document.getElementById('bottomSheetBackdrop');
    if (drawer && backdrop) {
        drawer.classList.add('active');
        backdrop.classList.add('active');
        if (typeof triggerHaptic === 'function') triggerHaptic('medium', 'Student Benefits Opened');
    }
};
"""

with open('app.js', 'w') as f:
    f.write(js)

with open('index.html', 'r') as f:
    html = f.read()

drawer_html = """
                <!-- Student Benefits Drawer -->
                <div class="bottom-sheet-drawer" id="studentBenefitsDrawer">
                    <div class="drawer-drag-handle" style="width: 36px; height: 4px; background: #E0E0E0; border-radius: 2px; margin: 12px auto 20px auto;"></div>
                    
                    <div style="padding: 0 24px 32px 24px;">
                        <h2 style="font-size: 20px; font-weight: 800; color: #000; margin: 0 0 16px 0;">Student Perks</h2>
                        <div style="display: flex; flex-direction: column; gap: 12px;">
                            <div style="font-size: 15px; color: #333; display: flex; align-items: center; gap: 8px;"><span>✨</span> <strong>perks: 10% Off</strong></div>
                            <div style="font-size: 15px; color: #333; display: flex; align-items: center; gap: 8px;"><span>✨</span> <strong>Free Date Change</strong></div>
                            <div style="font-size: 15px; color: #333; display: flex; align-items: center; gap: 8px;"><span>✨</span> <strong>+15 Kg extra Baggage included in fare</strong></div>
                        </div>
                    </div>
                </div>
"""

if 'id="studentBenefitsDrawer"' not in html:
    html = html.replace('<!-- Bank Offer Sheet -->', drawer_html + '\n                <!-- Bank Offer Sheet -->')

with open('index.html', 'w') as f:
    f.write(html)

print("Applied extra benefits drawer logic successfully.")
