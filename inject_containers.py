import re

with open('app.js', 'r') as f:
    js = f.read()

# Replace the end of flight card to include the inline container
old_card_end = """            </div>
        </div>
        `;"""
        
new_card_end = """            </div>
            <div class="inline-fare-container" id="inline-fare-${i}"></div>
        </div>
        `;"""

js = js.replace(old_card_end, new_card_end)

# Also fix the recommended card
old_rec_end = """            </div>
        </div>
    `;"""

new_rec_end = """            </div>
            <div class="inline-fare-container" id="inline-fare-rec"></div>
        </div>
    `;"""

js = js.replace(old_rec_end, new_rec_end)

# And fix the onclick for recommended card to use 'rec'
js = js.replace("toggleInlineFare(event, '${i}', 'Economy', '${oldP}')", "toggleInlineFare(event, 'rec', 'Economy', '${oldP}')")

with open('app.js', 'w') as f:
    f.write(js)

print("Injected inline containers into app.js")

# For index.html, inject the inline-fare-container directly before the closing div of flight-card
with open('index.html', 'r') as f:
    html = f.read()

# We know the hardcoded flight cards end with:
#                                 </div>
#                             </div>
# And start with: <!-- Sample Card X -->
# Let's just find each <div class="fc-pricing-row"> and add the container after its closing div.
# But it's easier to use a regex that matches the end of the pricing row.
row_regex = re.compile(r'(<div class="fc-pricing-row">.*?</div>\n\s*</div>)', re.DOTALL)

def replacer(match):
    # We need a unique ID for each hardcoded card, we can just use a counter or random
    # Actually, we already modified the onclicks to be hc1, hc2, etc.
    return match.group(1)

# Wait, instead of regex, let's just find the exact onclicks we already inserted and inject the container at the end.
# In `index.html`:
# onclick="toggleInlineFare(event, 'hc1', 'Economy', '4800')"
for i in range(1, 11):
    search_str = f"toggleInlineFare(event, 'hc{i}'"
    if search_str in html:
        # Find the end of this flight-card.
        idx = html.find(search_str)
        end_idx = html.find('</div>\n                            </div>', idx)
        if end_idx != -1:
            # We want to insert <div class="inline-fare-container" id="inline-fare-hc1"></div>
            insert_str = f'\n                                <div class="inline-fare-container" id="inline-fare-hc{i}"></div>'
            # Check if it's already there
            if insert_str not in html[idx:end_idx+100]:
                html = html[:end_idx+6] + insert_str + html[end_idx+6:]

with open('index.html', 'w') as f:
    f.write(html)

print("Injected inline containers into index.html")
