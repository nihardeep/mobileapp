import re

with open('app.js', 'r') as f:
    js = f.read()

# Fix Edit styling in applyBulkAdd and toggleSavedPassengerChip
old_edit_bulk = """<div class="passenger-status" style="font-size: 12px; color: var(--indigo-blue); font-weight: 800;">Edit ✏️</div>"""
new_edit_bulk = """<div class="passenger-status" style="font-size: 10px; color: var(--indigo-blue); font-weight: 800; text-align: right; margin-left: auto;">Edit ✏️</div>"""

js = js.replace(old_edit_bulk, new_edit_bulk)

# Also fix the generated empty card in toggleSavedPassengerChip when UNCHECKING
old_add_bulk = """<div class="passenger-add-btn">Add details ></div>"""
new_add_bulk = """<div class="passenger-add-btn" style="font-size: 10px; color: var(--indigo-blue); font-weight: 800; text-align: right; margin-left: auto;">Add details ></div>"""

js = js.replace(old_add_bulk, new_add_bulk)

with open('app.js', 'w') as f:
    f.write(js)
