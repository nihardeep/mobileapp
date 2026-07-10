with open('index.html', 'r') as f:
    lines = f.readlines()

# 1. Remove the wrongly placed appContent closing tag
nav_idx = -1
for i, line in enumerate(lines):
    if '<div class="bottom-nav"' in line:
        nav_idx = i
        break

if nav_idx != -1 and '</div> <!-- End appContent -->' in lines[nav_idx - 2]:
    lines.pop(nav_idx - 2)
    print("Removed wrong appContent closing tag.")

# 2. Insert appContent closing tag after screenTrips
trips_end_idx = -1
for i, line in enumerate(lines):
    if '<div class="screen" id="screenResults">' in line:
        trips_end_idx = i
        break

if trips_end_idx != -1:
    lines.insert(trips_end_idx, '                </div> <!-- End appContent -->\n\n')
    print("Inserted correct appContent closing tag.")

# 3. Add script tag at the end
haptic_idx = -1
for i, line in enumerate(lines):
    if '<!-- Haptic audio simulation nodes -->' in line:
        haptic_idx = i
        break

if haptic_idx != -1:
    lines.insert(haptic_idx, '    <script src="app.js?v=17"></script>\n\n')
    print("Inserted app.js script tag.")

with open('index.html', 'w') as f:
    f.writelines(lines)
