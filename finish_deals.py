import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Find the deals block
deals_start = content.find('<!-- COMPANION CAB DEALS -->')
# Find the end of companionHotelDeals
# companionHotelDeals is opened, then its inner div is opened, then closed... 
# The easiest way is to use regex or string slicing up to the last </div> before SCREEN 4
screen4_start = content.find('<!-- ==========================================================\n                     SCREEN 4: FLIGHT RESULTS')

# The chunk from deals_start to screen4_start
chunk_raw = content[deals_start:screen4_start]

# We need to strip the closing </div> of screenTrips from the end of the chunk
# It usually ends with "</div>\n    \n\n                    </div>\n\n\n                "
# Let's find the last '</div>' in chunk_raw and remove it
last_div_idx = chunk_raw.rfind('</div>')
deals_block = chunk_raw[:last_div_idx].strip()

# Remove the deals block from screenTrips (leave screenTrips intact but empty except for header)
content = content[:deals_start] + '\n                    </div>\n\n\n                ' + content[screen4_start:]

# 2. Find insertion point in screenHome
# We want to insert it after:
# <div class="companion-subcard" id="flightCompanionCard">
#     <div class="subcard-content" id="companionSubcardContent">
#         <!-- Will load one of the 8 states -->
#     </div>
# </div>
insertion_marker = '<!-- Will load one of the 8 states -->\n                                    </div>\n                                </div>'
insert_idx = content.find(insertion_marker)
if insert_idx != -1:
    insert_idx += len(insertion_marker)
    content = content[:insert_idx] + '\n\n' + deals_block + '\n' + content[insert_idx:]
    with open('index.html', 'w') as f:
        f.write(content)
    print("Successfully moved deals!")
else:
    print("Cannot find insertion point for deals.")

