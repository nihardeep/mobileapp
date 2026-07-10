import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Find the game chunk
start_marker = '<!-- PLAY & WIN GAME SCREEN -->'
idx_start = html.find(start_marker)

# Find the end marker
end_marker = '<script src="app.js?v=24"></script>'
idx_end = html.find(end_marker)

# We want to extract everything from start_marker to the </div></div> just before end_marker
# Let's just find the last </div> before end_marker
chunk_end = html.rfind('</div>', idx_start, idx_end)
# Wait, let's just grab the game screen and gameWinOverlay manually using depth counting.
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

screen_game_div_start = html.find('<div class="screen" id="screenGame"', idx_start)
screen_game_div_end = get_matching_div(html, screen_game_div_start)

win_overlay_div_start = html.find('<div id="gameWinOverlay"', screen_game_div_end)
win_overlay_div_end = get_matching_div(html, win_overlay_div_start)

# Extract the two components completely
part1 = html[idx_start:win_overlay_div_end]

# Remove them from the original location
html_without_game = html[:idx_start] + html[win_overlay_div_end:]

# 2. Inject right after <div class="iphone-screen">
iphone_start = html_without_game.find('<div class="iphone-screen">')
insert_pos = iphone_start + len('<div class="iphone-screen">')

final_html = html_without_game[:insert_pos] + '\n\n' + part1 + '\n\n' + html_without_game[insert_pos:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Game structure fixed.")
