import re

with open('index.html', 'r') as f:
    html = f.read()

# Locate the input and the mic icon again
nlp_wrapper_regex = r'(<div class="nlp-mic-icon".*?</svg>\s*</div>)\s*(<input type="text" id="nlpSearchInput".*?>)'
match = re.search(nlp_wrapper_regex, html, re.DOTALL)

if match:
    mic_html = match.group(1)
    input_html = match.group(2)
    
    # Remove the extra margin we added to the mic
    mic_html = mic_html.replace('margin-right: 12px; ', '')
    
    # Construct the custom placeholder and place the mic on the right
    custom_placeholder = """
            <div id="customNlpPlaceholder" style="position: absolute; left: 16px; top: 50%; transform: translateY(-50%); pointer-events: none; color: var(--text-secondary); font-size: 14px; font-weight: 500; display: flex; align-items: center;">
                Ask 6eSkai about &nbsp;<span id="nlpAnimatedText" style="color: var(--indigo-navy); font-weight: 600; transition: opacity 0.3s ease;">'Coorg Homestays'</span>
            </div>
    """
    
    # Update input to have smaller font size and no placeholder attribute, and ensure relative positioning for the wrapper
    input_html = input_html.replace('placeholder="Ask 6eSkai about \'Coorg Homestays\'"', 'placeholder=""')
    input_html = input_html.replace('font-size: 16px;', 'font-size: 14px;')
    input_html = input_html.replace('style="', 'style="position: relative; z-index: 2; ')
    
    new_wrapper_content = f'{custom_placeholder}\n{input_html}\n{mic_html}'
    html = html.replace(match.group(0), new_wrapper_content)
    
    # Also fix the padding of the wrapper to make mic touch the edge
    html = html.replace('padding: 12px 20px;', 'padding: 8px 8px 8px 16px; position: relative;')
    
    with open('index.html', 'w') as f:
        f.write(html)
    print("Updated index.html layout!")
else:
    print("Could not find nlp-mic-icon and input in expected order.")
