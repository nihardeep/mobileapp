with open('index.html', 'r') as f:
    content = f.read()

game_start = content.find('<!-- ========================================== -->\n        <!-- PLAY & WIN GAME SCREEN -->')
if game_start == -1:
    print("Cannot find game start")
else:
    # the game ends at </div> right before </div>\n    </div>\n    \n    <script src="app.js?v=24"></script>
    script_tag = content.find('<script src="app.js?v=24"></script>')
    if script_tag != -1:
        # the game chunk is from game_start to the </div> before script_tag
        # Let's extract exactly what's between game_start and script_tag minus the closing divs
        game_end = content.rfind('</div>\n    </div>\n    \n    <script src="app.js?v=24"></script>')
        if game_end != -1:
            game_html = content[game_start:game_end]
            
            # Remove game from its current position
            content = content[:game_start] + content[game_end:]
            
            # Find the end of screenBaggageTracking
            # We want to insert the game INSIDE iphone-screen
            # So right before the last closing </div> of iphone-screen
            # There is:
            # </div> (end of baggage tracking)
            # </div> (end of iphone-screen)
            # We can just insert the game right BEFORE the closing of iphone-screen
            # Or just right after screenBaggageTracking's closing tag
            # But the easiest way is to insert it right before the </div> that closes iphone-screen.
            # In our current content, right above game_start is:
            # </div>
            # </div>
            
            # We can use the marker:
            #                     <div class="toggle-knob"></div>
            #                 </div>
            #             </div>
            #         </div>
            marker = '                    <div class="toggle-knob"></div>\n                </div>\n            </div>\n        </div>'
            idx = content.find(marker)
            if idx != -1:
                insert_idx = idx + len(marker)
                # insert it here
                content = content[:insert_idx] + '\n' + game_html + '\n' + content[insert_idx:]
                with open('index.html', 'w') as f:
                    f.write(content)
                print("Moved game inside iphone-screen!")
            else:
                print("Cannot find insertion point")
