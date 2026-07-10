with open('index.html', 'r') as f:
    content = f.read()

with open('game_html.txt', 'r') as f:
    game_html = f.read()

# I need to clean up game_html if it contains anything before or after the screen
# The output starts with "        </div>\n\n        <!-- =========================================="
# Let's find the start of <!-- PLAY & WIN GAME SCREEN -->
start_idx = game_html.find('<!-- PLAY & WIN GAME SCREEN -->')
# We want the <!-- === above it too
start_idx = game_html.rfind('<!-- ===', 0, start_idx)

# Find where it ends
end_idx = game_html.rfind('</div>') + 6 # Include the last </div>

if start_idx != -1 and end_idx != -1:
    clean_game_html = game_html[start_idx:end_idx]
    
    # insert into index.html
    # Find the closing tag of iphone-screen
    # iphone-screen is closed right before:
    # </div>
    # </div>
    # <script src="app.js?v=24"></script>
    
    script_idx = content.rfind('<script src="app.js')
    if script_idx != -1:
        insert_idx = content.rfind('</div>\n    </div>\n    \n    <script', 0, script_idx + 30)
        if insert_idx != -1:
            content = content[:insert_idx] + '\n' + clean_game_html + '\n' + content[insert_idx:]
            with open('index.html', 'w') as f:
                f.write(content)
            print("Successfully injected game HTML!")
        else:
            print("Could not find insert idx")
    else:
        print("Could not find script tag")
