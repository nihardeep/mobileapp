import re
with open('index.html', 'r') as f:
    html = f.read()

start_str = '<div class="bottom-sheet-backdrop" id="bottomSheetBackdrop"'
start = html.find(start_str)
end = html.find('<!-- Haptic audio simulation nodes -->')

print(html[start:end])
