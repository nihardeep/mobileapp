import re

with open('app.js', 'r') as f:
    js = f.read()

# 1. Clear out pf-assistance in openPassengerForm
old_open_logic = """    document.getElementById('pf-fname').value = name;
    document.getElementById('pf-lname').value = '';
    document.getElementById('pf-dob').value = '';"""

new_open_logic = """    document.getElementById('pf-fname').value = name;
    document.getElementById('pf-lname').value = '';
    document.getElementById('pf-dob').value = '';
    document.getElementById('pf-assistance').value = '';"""

if old_open_logic in js:
    js = js.replace(old_open_logic, new_open_logic)

# 2. In savePassengerForm, read pf-assistance and update card HTML
old_save_logic = """        card.innerHTML = `
            <div style="display: flex; align-items: center; gap: 16px;">
                <div class="passenger-avatar" style="background: rgba(34, 197, 94, 0.1); color: #22c55e;">${fname.substring(0,2).toUpperCase()}</div>
                <div style="flex: 1;">
                    <div class="passenger-name" style="color: #22c55e;">${fname}</div>
                    <div class="passenger-type">${type}</div>
                </div>
                <div class="passenger-status" style="font-size: 12px; color: var(--indigo-blue); font-weight: 800;">Edit ✏️</div>
            </div>
        `;"""

new_save_logic = """        const assistance = document.getElementById('pf-assistance') ? document.getElementById('pf-assistance').value : '';
        const wheelchairHtml = assistance === 'Wheelchair' ? `<div style="font-size: 10px; color: #f59e0b; background: rgba(245, 158, 11, 0.1); padding: 2px 6px; border-radius: 4px; display: inline-block; margin-top: 4px; font-weight: 700;">♿ Wheelchair Requested</div>` : '';
        
        card.innerHTML = `
            <div style="display: flex; align-items: center; gap: 12px;">
                <div class="passenger-avatar" style="background: rgba(34, 197, 94, 0.1); color: #22c55e;">${fname.substring(0,2).toUpperCase()}</div>
                <div style="flex: 1;">
                    <div class="passenger-name" style="color: #22c55e;">${fname}</div>
                    <div class="passenger-type" style="margin-bottom: 2px;">${type}</div>
                    ${wheelchairHtml}
                </div>
                <div class="passenger-status" style="font-size: 10px; color: var(--indigo-blue); font-weight: 800; text-align: right; margin-left: auto;">Edit ✏️</div>
            </div>
        `;"""

if old_save_logic in js:
    js = js.replace(old_save_logic, new_save_logic)

with open('app.js', 'w') as f:
    f.write(js)
