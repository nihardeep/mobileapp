import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Extract marquee from results-header
marquee_regex = r'(<div class="offers-marquee-wrapper".*?</div>\s*</div>)'
match = re.search(marquee_regex, html, re.DOTALL)

if match:
    marquee_html = match.group(0)
    
    # Remove from flight listing page
    html = html.replace(marquee_html, '')
    
    # We need to restore it to the homepage
    # Originally it was just above <!-- Recent Searches -->
    target = '<!-- Recent Searches -->'
    
    # Revert the margin style change we made during the move
    marquee_html_original = marquee_html.replace('style="margin-top: 0; background: #fff; border-top: none; padding: 4px 0;"', '')
    
    html = html.replace(target, marquee_html_original + '\n                            ' + target)

with open('index.html', 'w') as f:
    f.write(html)

with open('style.css', 'r') as f:
    css = f.read()

# Revert #screenResults.active flex layout
new_results_css = """#screenResults.active {
    display: flex;
    flex-direction: column;
    flex: 1;
    margin: -16px; /* Negate app-content padding so header touches edge */
    margin-bottom: -85px;
    padding-bottom: 85px;
    background: #f0f4f8; /* Ensure full background coverage */
}"""

old_results_css = """#screenResults.active {
    display: flex;
    flex-direction: column;
    height: 100%;
    margin: -16px; /* Negate app-content padding so header touches edge */
    margin-bottom: -85px;
    padding-bottom: 85px;
}"""

css = css.replace(new_results_css, old_results_css)

with open('style.css', 'w') as f:
    f.write(css)

print("Reverted marquee and layout!")
