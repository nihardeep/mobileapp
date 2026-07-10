with open('index.html', 'r') as f:
    html = f.read()

# Find the injected drawers
start_comment = '<!-- ALL BOTTOM SHEET DRAWERS -->'
end_comment = '<!-- Haptic audio simulation nodes -->'

start_idx = html.find(start_comment)
end_idx = html.find(end_comment)

drawers_block = html[start_idx:end_idx]

# Remove from current location
html = html[:start_idx] + html[end_idx:]

# Insert right after <div class="iphone-screen">
insert_target = '<div class="iphone-screen">'
target_idx = html.find(insert_target) + len(insert_target)

html = html[:target_idx] + '\n' + drawers_block + html[target_idx:]

with open('index.html', 'w') as f:
    f.write(html)
print("Moved drawers successfully!")
