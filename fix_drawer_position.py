import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Extract the bankOfferDrawer
drawer_regex = r'(<!-- Bank Offer Sheet -->\s*<div class="bottom-sheet-drawer" id="bankOfferDrawer">.*?</div>\s*</div>\s*</div>)'
match = re.search(drawer_regex, html, re.DOTALL)

if match:
    drawer_html = match.group(0)
    
    # 2. Remove it from its current location
    html = html.replace(drawer_html, '')
    
    # 3. Find the travelersSheetDrawer and append it right after that drawer closes
    travelers_regex = r'(<div class="bottom-sheet-drawer" id="travelersSheetDrawer">.*?</div>\s*</div>\s*</div>)'
    match2 = re.search(travelers_regex, html, re.DOTALL)
    
    if match2:
        travelers_html = match2.group(0)
        # Append bankOfferDrawer right after travelersSheetDrawer
        html = html.replace(travelers_html, travelers_html + '\n\n' + drawer_html)
        print("Moved bankOfferDrawer perfectly inside iphone-screen!")
    else:
        print("Could not find travelersSheetDrawer to append after!")
        
    with open('index.html', 'w') as f:
        f.write(html)
else:
    print("Could not find bankOfferDrawer to move!")
