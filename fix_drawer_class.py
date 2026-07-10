import re

with open('app.js', 'r') as f:
    js = f.read()

# Replace .active with .visible in openStudentBenefitsDrawer
if 'drawer.classList.add(\'active\');' in js:
    js = js.replace('drawer.classList.add(\'active\');', 'drawer.classList.add(\'visible\');')
    
if 'backdrop.classList.add(\'active\');' in js:
    js = js.replace('backdrop.classList.add(\'active\');', 'backdrop.classList.add(\'visible\');')

with open('app.js', 'w') as f:
    f.write(js)

print("Fixed drawer visibility class.")
