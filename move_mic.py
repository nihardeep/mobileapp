import re

with open('index.html', 'r') as f:
    html = f.read()

# Locate the input and the mic icon
nlp_wrapper_regex = r'(<input type="text" id="nlpSearchInput".*?>)\s*(<div class="nlp-mic-icon".*?</svg>\s*</div>)'
match = re.search(nlp_wrapper_regex, html, re.DOTALL)

if match:
    input_html = match.group(1)
    mic_html = match.group(2)
    
    # We want to place the mic_html BEFORE the input_html
    # Let's also add a small right margin to the mic icon so it pushes the text slightly away
    # Check if margin-right already exists, if not, add it
    if 'margin-right:' not in mic_html:
        mic_html = mic_html.replace('style="', 'style="margin-right: 12px; ')
        
    new_wrapper_content = f'{mic_html}\n{input_html}'
    
    html = html.replace(match.group(0), new_wrapper_content)
    
    with open('index.html', 'w') as f:
        f.write(html)
    print("Moved mic to the left!")
else:
    print("Could not find nlp-mic-icon next to input.")
