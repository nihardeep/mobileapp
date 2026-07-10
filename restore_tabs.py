import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove the AI Mode button
ai_mode_btn_regex = r'<div style="display: flex; justify-content: flex-end; margin-bottom: 12px; margin-top: -8px;">.*?</div>\s*</div>'
html = re.sub(ai_mode_btn_regex, '', html, flags=re.DOTALL)

# 2. Add the tabs back before manualSearchView
tabs_html = """
    <!-- Mode Toggle Header -->
    <div class="search-mode-toggle">
        <div class="search-mode-tab active" id="tabManual" onclick="toggleSearchMode('manual')">Manual Search</div>
        <div class="search-mode-tab" id="tabNLP" onclick="toggleSearchMode('nlp')">✨ Ask 6eSkai</div>
    </div>
"""
html = html.replace('<div id="manualSearchView" class="search-view-container active-view" style="display: block;">', tabs_html + '\n    <div id="manualSearchView" class="search-view-container active-view" style="display: block;">')

with open('index.html', 'w') as f:
    f.write(html)
print("Restored tabs!")
