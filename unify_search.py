import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove the search-mode-toggle
toggle_regex = r'<div class="search-mode-toggle">.*?</div>'
html = re.sub(toggle_regex, '', html, flags=re.DOTALL)

# 2. Extract nlpSearchView inner content
nlp_regex = r'<div id="nlpSearchView" class="search-view-container" style="display: none;">(.*?)</div>\s*<!-- end search-widget-expanded-content -->'
match = re.search(nlp_regex, html, re.DOTALL)

if match:
    nlp_content = match.group(1).strip()
    # Remove the entire nlpSearchView block
    html = html.replace(match.group(0), '')
    
    # Also remove `<div id="nlpSearchView" class="search-view-container" style="display: none;">` which might be left over if regex was slightly off
    html = re.sub(r'<div id="nlpSearchView"[^>]*>.*?</div>\s*<!-- end search-widget-expanded-content -->', '', html, flags=re.DOTALL)
    
    # Now, find the search button container in manualSearchView
    btn_regex = r'<div class="search-btn-container" id="searchBtnContainer">'
    
    # We will inject the nlp_content right before the search button container, adding a little separator or just margin
    injected_nlp = f"""
        <div class="unified-nlp-container" style="margin-top: 16px; margin-bottom: 16px;">
            {nlp_content}
        </div>
        <div class="search-btn-container" id="searchBtnContainer">
    """
    html = html.replace('<div class="search-btn-container" id="searchBtnContainer">', injected_nlp)
    
    # We don't need the back icon inside the NLP wrapper anymore since there's no tab to go back to!
    html = re.sub(r'<div class="nlp-back-icon"[^>]*>.*?</div>', '', html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
print("Unified layout created!")
