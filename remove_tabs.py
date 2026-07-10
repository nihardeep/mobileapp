import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove the search-mode-toggle completely
toggle_regex = r'<div class="search-mode-toggle">.*?</div>'
html = re.sub(toggle_regex, '', html, flags=re.DOTALL)

# 2. Add AI Mode button inside manualSearchView, and make it default
ai_mode_btn = """
    <div id="manualSearchView" class="search-view-container active-view" style="display: block;">
        <div style="display: flex; justify-content: flex-end; margin-bottom: 12px; margin-top: -8px;">
            <div class="ai-mode-btn" onclick="toggleSearchMode('nlp')" style="background: #dbeafe; color: #0f172a; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 13px; display: inline-flex; align-items: center; gap: 6px; cursor: pointer; border: 1px solid rgba(15,23,42,0.05);">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    <path d="M16 5l1.5 1.5L19 8l-1.5 1.5L16 11l-1.5-1.5L13 8l1.5-1.5z"></path>
                </svg> AI Mode
            </div>
        </div>
"""

# Replace manualSearchView definition
html = re.sub(r'<div id="manualSearchView".*?>', ai_mode_btn, html, count=1)

# 3. Make nlpSearchView hidden by default
html = html.replace('<div id="nlpSearchView" class="search-view-container" style="display: block;">', '<div id="nlpSearchView" class="search-view-container" style="display: none;">')

# 4. Add onClick to nlp-back-icon
html = html.replace('<div class="nlp-back-icon" style="color: var(--text-secondary); margin-right: 12px; cursor: pointer;">', '<div class="nlp-back-icon" onclick="toggleSearchMode(\'manual\')" style="color: var(--text-secondary); margin-right: 12px; cursor: pointer;">')

with open('index.html', 'w') as f:
    f.write(html)
print("Updated to remove tabs and add AI Mode pill!")
