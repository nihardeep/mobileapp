import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# EXTRACT Cab Deals
cab_start_marker = '<!-- COMPANION CAB DEALS -->'
cab_start = html.find(cab_start_marker)
# Find the closing </div> of Cab Deals. Cab deals ends right before Hotel Deals.
hotel_start_marker = '<!-- COMPANION HOTEL DEALS -->'
hotel_start = html.find(hotel_start_marker)
cab_html = html[cab_start:hotel_start].strip()

# EXTRACT Hotel Deals
# Hotel Deals ends at line 1001: </div>\n\n                            </div>
hotel_end_marker = '                            </div>\n\n                        </div>\n\n<div class="recent-searches-section" id="recentSearchesSection">'
hotel_end = html.find(hotel_end_marker)
if hotel_end == -1:
    hotel_end = html.find('<div class="recent-searches-section" id="recentSearchesSection">')
    
# Find the exact end of Hotel Deals by looking for the last </div> before hotel_end
hotel_html_raw = html[hotel_start:hotel_end].strip()

# Let's cleanly just find where to cut.
# The cut should be from `cab_start` to `hotel_end` (excluding `hotel_end` marker).
# So we remove both sections from homeFlightStateWrapper.
html_new = html[:cab_start] + html[hotel_end:]

# Now apply design fixes to cab_html
# 1. Cab Deals padding: margin-top: 24px -> margin-top: 16px; display: none;
cab_html = cab_html.replace('margin-top: 24px;', 'margin-top: 16px; display: none;')
# 2. Font sizes:
cab_html = cab_html.replace('<div style="font-size: 16px; font-weight: 800; color: #0f172a;">Cab Deals</div>', '<span class="section-title">Cab Deals</span>')
# 3. Car overlapping / Arrow:
# Remove the arrow div completely
arrow_div_regex = r'<div style="position: absolute; right: 12px; top: 12px; z-index: 3; background: #fff; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba\(0,0,0,0\.1\);">.*?</div>'
cab_html = re.sub(arrow_div_regex, '', cab_html, flags=re.DOTALL)
# Make car smaller and move to right edge:
cab_html = cab_html.replace('right: 40px; bottom: -10px; width: 140px;', 'right: 10px; bottom: -10px; width: 110px;')

# Apply design fixes to hotel_html
# 1. Hide by default
hotel_html_raw = hotel_html_raw.replace('margin-top: 32px;', 'margin-top: 16px; display: none;')
# 2. Font sizes:
hotel_html_raw = hotel_html_raw.replace('<span style="font-size: 16px; font-weight: 800; color: #0f172a;">Hotel Deals</span>', '<span class="section-title">Hotel Deals</span>')
# 3. Make hotel cards a little smaller:
hotel_html_raw = hotel_html_raw.replace('flex: 0 0 82%;', 'flex: 0 0 75%;')
hotel_html_raw = hotel_html_raw.replace('height: 120px;', 'height: 100px;')

# Insert Cab Deals before recentSearchesSection
insert_cab_marker = '<div class="recent-searches-section" id="recentSearchesSection">'
idx_cab = html_new.find(insert_cab_marker)
html_new = html_new[:idx_cab] + cab_html + '\n\n' + html_new[idx_cab:]

# Insert Hotel Deals before loyaltySection
insert_hotel_marker = '                            <!-- Loyalty Panel (IndiGo BluChip balance) -->'
idx_hotel = html_new.find(insert_hotel_marker)
html_new = html_new[:idx_hotel] + hotel_html_raw + '\n\n' + html_new[idx_hotel:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_new)
print("Updated index.html")
