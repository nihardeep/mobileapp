import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find the closing div of iphone-screen
# We can find all elements with class="iphone-screen"
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
                return i + 1
        else:
            i += 1
    return -1

iphone_screen_start = html.find('<div class="iphone-screen">')
iphone_screen_end = get_matching_div(html, iphone_screen_start)

print("iphone-screen starts at:", iphone_screen_start)
print("iphone-screen ends at:", iphone_screen_end)

# Let's find where screenGame starts and ends
screen_game_start = html.find('<!-- PLAY & WIN GAME SCREEN -->')
# Find the matching closing div for screenGame, but wait! The code currently has gameWinOverlay immediately following screenGame.
# Let's just find the very last </div> before <script src="app.js?v=24"></script>
script_start = html.find('<script src="app.js?v=24"></script>')

# Are screenGame and gameWinOverlay OUTSIDE iphone-screen?
if screen_game_start > iphone_screen_end:
    print("Yes, screenGame is outside iphone-screen!")
    
    # We need to move everything from screen_game_start down to the end of the divs, INSIDE iphone-screen.
    # The end of the game elements is right before script_start, maybe skipping a few closing divs that belong to other things?
    # Wait, the end of iphone-screen is at iphone_screen_end. 
    # What if we just cut screenGame and gameWinOverlay and insert them right before the closing </div> of iphone-screen?
    
    # Let's extract the game HTML
    # We'll just grab from screen_game_start to script_start, and strip out any trailing closing divs that belong to the body/container.
    game_html_chunk = html[screen_game_start:script_start].strip()
    
    # The game chunk might contain closing divs for the main containers if the file was malformed.
    # But wait, looking at the tail output:
    # </div> <!-- End scrolling wrapper -->
    # <div floating footer... </div>
    # </div> 
    # </div> 
    # <!-- PLAY & WIN --> ...
    # </div> </div> <script>
    
    # Let's just manually print the exact context around iphone_screen_end
    print(html[iphone_screen_end-100:iphone_screen_end+500])
