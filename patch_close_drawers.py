import re

with open('app.js', 'r') as f:
    js = f.read()

# Add closeAllDrawers() to initAddonsScreen
js = js.replace('function initAddonsScreen() {\\n    // 1. Populate Passenger Cart Headers', 'function initAddonsScreen() {\\n    closeAllDrawers();\\n    // 1. Populate Passenger Cart Headers')

with open('app.js', 'w') as f:
    f.write(js)
