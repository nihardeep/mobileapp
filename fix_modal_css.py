import re

with open('style.css', 'r') as f:
    css = f.read()

# Fix centered-popup-overlay
css = css.replace('.centered-popup-overlay {\n    position: fixed;', '.centered-popup-overlay {\n    position: absolute;')

# Fix compare-modal-overlay
css = css.replace('.compare-modal-overlay {\n    position: fixed;', '.compare-modal-overlay {\n    position: absolute;')

# Reduce modal size
css = css.replace('max-width: 400px;', 'max-width: 320px;')

# Reduce card size
css = css.replace('.cp-3d-card {\n    flex: 0 0 200px;', '.cp-3d-card {\n    flex: 0 0 170px;')

# Adjust padder for 170px card width
css = css.replace('flex: 0 0 calc(50% - 100px); /* Assuming card width ~200px */', 'flex: 0 0 calc(50% - 85px); /* Assuming card width ~170px */')

# Make the card features scrollable to prevent height overflow
if 'overflow-y: auto;' not in css:
    css = css.replace('.cp-card-features {\n    padding: 12px;\n    flex-grow: 1;', '.cp-card-features {\n    padding: 12px;\n    flex-grow: 1;\n    overflow-y: auto;\n    max-height: 200px;')

with open('style.css', 'w') as f:
    f.write(css)

print("Fixed CSS bounds and sizes")
