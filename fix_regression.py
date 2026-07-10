import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace all occurrences back to navigateTo('home') first
html = html.replace('onclick="openFlightSearchDrawer()"', 'onclick="navigateTo(\'home\')"')

# Now carefully replace only the correct ones
target_student = '<div class="student-hub-search-context" onclick="navigateTo(\'home\')"'
repl_student = '<div class="student-hub-search-context" onclick="openFlightSearchDrawer()"'
html = html.replace(target_student, repl_student)

target_ai = '<div class="ai-dest-edit-icon" onclick="navigateTo(\'home\')">'
repl_ai = '<div class="ai-dest-edit-icon" onclick="openFlightSearchDrawer()">'
html = html.replace(target_ai, repl_ai)

with open('index.html', 'w') as f:
    f.write(html)
