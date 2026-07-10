import re
import shutil

# 1. Read current broken index.html to extract our injected HTML blocks
with open('index.html', 'r') as f:
    broken_html = f.read()

# Extract Game HTML
game_start = broken_html.find('<!-- ========================================== -->\n        <!-- PLAY & WIN GAME SCREEN -->')
game_end = broken_html.find('<!-- Haptic audio simulation nodes -->')

if game_start != -1 and game_end != -1:
    # Need to find the exact end of game overlay
    overlay_end = broken_html.find('Claim & Return</button>\n        </div>', game_start)
    if overlay_end != -1:
        game_html_block = broken_html[game_start:overlay_end + len('Claim & Return</button>\n        </div>')]
    else:
        print("Could not find end of game overlay.")
        exit(1)
else:
    print("Could not find Game HTML.")
    exit(1)

# Extract Deals HTML
deals_start = broken_html.find('<!-- COMPANION CAB DEALS -->')
# Find end of deals HTML
deals_end_str = 'Book</button>\n                </div>\n            </div>\n        </div>'
deals_end = broken_html.find(deals_end_str, deals_start)
if deals_start != -1 and deals_end != -1:
    deals_html_block = broken_html[deals_start:deals_end + len(deals_end_str)]
    # Need to close the flex container that holds the hotel cards!
    # In original deals, there was a `</div>\n    </div>` to close flex container and #companionHotelDeals.
    deals_html_block += '\n    </div>\n</div>'
else:
    print("Could not find Deals HTML.")
    exit(1)


# 2. Reset to index_recovered.html
shutil.copy('index_recovered.html', 'index.html')
with open('index.html', 'r') as f:
    fresh_html = f.read()

# 3. Inject Game HTML INSIDE iphone-screen
# The iphone-screen ends with:
#                 <!-- Toggle switch -->
#                 <div class="custom-toggle" onclick="this.classList.toggle('active')">
#                     <div class="toggle-knob"></div>
#                 </div>
#             </div>
#         </div>
# 
#         </div>
# 
#     </div>
# </div>
# <script src="app.js?v=24"></script>
# Let's find `<script src="app.js?v=24"></script>` and inject right before the `</div>\n    </div>` above it.
script_idx = fresh_html.rfind('<script src="app.js?v=24"></script>')
# Find the exact two closing divs
insert_game_idx = fresh_html.rfind('</div>\n    </div>', 0, script_idx + 1)
if insert_game_idx != -1:
    fresh_html = fresh_html[:insert_game_idx] + '\n' + game_html_block + '\n\n' + fresh_html[insert_game_idx:]
else:
    print("Could not find game insertion point.")
    exit(1)


# 4. Inject Deals HTML into Home Screen Trip Companion
# The pnr-card is here:
# <div class="companion-subcard" id="flightCompanionCard">
#     <div class="subcard-content" id="companionSubcardContent">
#         <!-- Will load one of the 8 states -->
#     </div>
# </div>
pnr_marker = '<!-- Will load one of the 8 states -->\n                                    </div>\n                                </div>'
insert_deals_idx = fresh_html.find(pnr_marker)
if insert_deals_idx != -1:
    insert_deals_idx += len(pnr_marker)
    fresh_html = fresh_html[:insert_deals_idx] + '\n\n' + deals_html_block + '\n' + fresh_html[insert_deals_idx:]
else:
    print("Could not find deals insertion point.")
    exit(1)

# Write final fixed HTML
with open('index.html', 'w') as f:
    f.write(fresh_html)

print("Perfectly Restored and Re-injected!")
