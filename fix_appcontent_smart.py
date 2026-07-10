with open('index.html', 'r') as f:
    lines = f.readlines()

# 1. Remove the extra </div> in screenTrips
# screenTrips ends around line 2282
# Let's find exactly the lines
for i in range(len(lines)):
    if 'id="screenTrips"' in lines[i]:
        start_idx = i
        break

# Find the end of screenTrips
# It's before "SCREEN 4: FLIGHT RESULTS"
for i in range(start_idx, len(lines)):
    if 'id="screenResults"' in lines[i]:
        end_idx = i
        break

# Inside screenTrips, there are two </div> at the end
# Let's delete the last </div> before screenResults
for i in range(end_idx - 1, start_idx, -1):
    if '</div>' in lines[i]:
        print(f"Removing extra </div> at line {i+1}")
        lines.pop(i)
        break

# 2. Add a </div> right before bottom-nav
for i in range(len(lines)):
    if 'class="bottom-nav"' in lines[i] or '<!-- Bottom Navigation Bar -->' in lines[i]:
        nav_idx = i
        if '<!-- Bottom Navigation Bar -->' in lines[nav_idx]:
            break
        elif 'class="bottom-nav"' in lines[nav_idx]:
            # if comment is not there, insert before bottom-nav
            break

print(f"Adding </div> before bottom-nav at line {nav_idx+1}")
lines.insert(nav_idx, "                </div> <!-- End appContent -->\n\n")

with open('index.html', 'w') as f:
    f.writelines(lines)
