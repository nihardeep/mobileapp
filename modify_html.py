import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Extract the flight-state-wrapper exactly
# Using regex to capture from <div class="flight-state-wrapper"> to its matching closing div.
# Because regex is tricky with nested divs, I'll use a simple string search.

start_str = '<div class="flight-state-wrapper">'
end_str = '<!-- ==========================================================\n                         SCREEN 4: FLIGHT RESULTS'

wrapper_start_idx = content.find(start_str)
end_idx = content.find(end_str)

# We need to find the exact closing div of screenTrips before SCREEN 4
wrapper_chunk = content[wrapper_start_idx:end_idx]
# The chunk ends with:
#                         </div>
#                     </div>
#
#                 </div>
#                 <!-- == SCREEN 4

# Let's cleanly remove it from screenTrips.
# screenTrips should now just be:
# <div class="screen" id="screenTrips">
#     <div class="trips-header">
#         <div class="trips-title">Upcoming Trip</div>
#     </div>
# </div>

screen_trips_start = content.find('<div class="screen" id="screenTrips">')
screen_trips_html = """<div class="screen" id="screenTrips">
                        <div class="trips-header">
                            <div class="trips-title">Upcoming Trip</div>
                        </div>
                    </div>"""

# Replace the whole screenTrips chunk with the simplified one.
new_content = content[:screen_trips_start] + screen_trips_html + "\n\n                " + content[end_idx:]

# Now we need the flight-state-wrapper text.
# We'll extract it from the original content:
wrapper_only = content[wrapper_start_idx:end_idx].strip()
# remove the trailing closing divs that belonged to screenTrips and appContent (wait, appContent?)
# The original ended with:
# 980: 
# 981:                         </div>
# 982:                     </div>
# 983: 
# 984:                 </div>
# 985: 
# 986:                 <!-- ==========================================================
# 987:                      SCREEN 4: FLIGHT RESULTS
wrapper_only = wrapper_only.rsplit('</div>', 2)[0].strip() # removes the last two </div> which belonged to screenTrips and maybe app-content?
# Actually, it's safer to just take the exact flight-state-wrapper block from the original content.

