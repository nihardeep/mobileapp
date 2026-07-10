import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the start of the newUserCard
new_user_start_marker = '<!-- STATE 2: NEW USER (Zero Balance) -->'
idx_new_user_start = html.find(new_user_start_marker)
if idx_new_user_start == -1:
    idx_new_user_start = html.find('<div class="bluchip-3d-wrapper" id="newUserCard"')

# We will just parse out the newUserCard by finding its matching closing div.
def get_matching_div(text, start_idx):
    depth = 0
    i = start_idx
    while i < len(text):
        if text.startswith('<div', i):
            depth += 1
            i += 4
        elif text.startswith('</div', i):
            depth -= 1
            i += 5
            if depth == 0:
                return i + 1 # include the >
        else:
            i += 1
    return -1

# The newUserCard div starts at:
new_user_div_start = html.find('<div class="bluchip-3d-wrapper" id="newUserCard"', idx_new_user_start)
new_user_div_end = get_matching_div(html, new_user_div_start)

new_user_card_html = html[idx_new_user_start:new_user_div_end]

# Also let's extract and remove the whole profileDrawer
drawer_start = html.find('<!-- Profile Drawer -->')
if drawer_start == -1:
    drawer_start = html.find('<div class="bottom-sheet-drawer" id="profileDrawer"')

drawer_div_start = html.find('<div class="bottom-sheet-drawer" id="profileDrawer"', drawer_start)
drawer_div_end = get_matching_div(html, drawer_div_start)

# We remove the profile drawer entirely from the html
html_without_drawer = html[:drawer_start] + html[drawer_div_end:]

# Set newUserCard to be hidden by default
new_user_card_html = new_user_card_html.replace('id="newUserCard" style="position: relative; perspective: 1500px;"', 'id="newUserCard" style="position: relative; perspective: 1500px; display: none;"')
# Wait, if there's any style already, it might be different. Let's just do a regex replace to add display: none;
new_user_card_html = re.sub(r'(id="newUserCard"[^>]*style="[^"]*)"', r'\1; display: none;"', new_user_card_html)


# Now, inject the new_user_card_html right after loyalUserCard in the loyaltySection
loyal_user_start = html_without_drawer.find('<div class="bluchip-3d-wrapper" id="loyalUserCard"')
loyal_user_end = get_matching_div(html_without_drawer, loyal_user_start)

html_final = html_without_drawer[:loyal_user_end] + '\n\n                                ' + new_user_card_html + '\n' + html_without_drawer[loyal_user_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_final)

print("HTML fixed successfully.")
