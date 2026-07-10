import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Extract the marquee
marquee_regex = r'<!-- Bank Offers Marquee -->.*?</div>\s*</div>'
match = re.search(marquee_regex, html, re.DOTALL)

if match:
    marquee_html = match.group(0)
    
    # Remove from original location
    html = html.replace(marquee_html, '')
    
    # Adjust marquee styles for the flight listing header
    # We will just inject it into the results-header
    
    insertion_target = """<div class="edit-search-icon">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="var(--indigo-blue)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                            </div>
                        </div>"""
    
    # We'll need to remove the margin-top from the marquee for this new location
    marquee_html_modified = marquee_html.replace('class="offers-marquee-wrapper"', 'class="offers-marquee-wrapper" style="margin-top: 0; background: #fff; border-top: none; padding: 4px 0;"')
    
    new_insertion = insertion_target + "\n" + marquee_html_modified
    
    html = html.replace(insertion_target, new_insertion)
    print("Moved marquee successfully.")
else:
    print("Could not find marquee in index.html")

with open('index.html', 'w') as f:
    f.write(html)


with open('style.css', 'r') as f:
    css = f.read()

# Increase the max height of the app container if needed to ensure full coverage
# The user said "Adjust the height of this page to cover the full ios screen"
# Let's ensure iphone-screen and app-content are perfectly 100% height
css = css.replace('.iphone-screen {\n    width: 375px;\n    height: 812px;', '.iphone-screen {\n    width: 375px;\n    height: 812px;\n    display: flex;\n    flex-direction: column;')
css = css.replace('.app-content {\n    padding: 16px;\n    padding-bottom: 85px; /* Space for bottom nav */', '.app-content {\n    padding: 16px;\n    padding-bottom: 85px; /* Space for bottom nav */\n    flex: 1;\n    overflow-y: auto;\n    display: flex;\n    flex-direction: column;')

# Fix results screen height
old_results_css = """#screenResults.active {
    display: flex;
    flex-direction: column;
    height: 100%;
    margin: -16px; /* Negate app-content padding so header touches edge */
    margin-bottom: -85px;
    padding-bottom: 85px;
}"""

new_results_css = """#screenResults.active {
    display: flex;
    flex-direction: column;
    flex: 1;
    margin: -16px; /* Negate app-content padding so header touches edge */
    margin-bottom: -85px;
    padding-bottom: 85px;
    background: #f0f4f8; /* Ensure full background coverage */
}"""

if '#screenResults.active {' in css:
    css = css.replace(old_results_css, new_results_css)

with open('style.css', 'w') as f:
    f.write(css)

print("Updated styles for full screen layout!")
