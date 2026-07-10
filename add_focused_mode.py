import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Add the back icon into the nlp-input-wrapper (hidden by default)
# We need to find the custom placeholder and insert it before it
custom_placeholder_regex = r'(<div id="customNlpPlaceholder".*?>.*?</div\s*>)'
match = re.search(custom_placeholder_regex, html, re.DOTALL)

if match:
    back_icon_html = """
            <div id="nlpBackIcon" onclick="exitNlpMode(event)" style="color: var(--indigo-blue); margin-right: 12px; cursor: pointer; display: none; align-items: center; justify-content: center; width: 32px; height: 32px; background: rgba(0,95,169,0.05); border-radius: 50%;">
                <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
            </div>
    """
    html = html.replace(match.group(1), back_icon_html + match.group(1))

with open('index.html', 'w') as f:
    f.write(html)


with open('style.css', 'a') as f:
    css = """
/* NLP Focused Mode Styles */
.search-widget-panel.nlp-focused-mode .route-row,
.search-widget-panel.nlp-focused-mode .search-details-row,
.search-widget-panel.nlp-focused-mode .search-btn-container {
    display: none;
}

.search-widget-panel.nlp-focused-mode .unified-nlp-container {
    margin-top: 0 !important;
}
"""
    f.write(css)


with open('app.js', 'r') as f:
    js = f.read()

# Add the focused mode logic to the DOMContentLoaded block
focused_mode_js = """
    // NLP Focused Mode Logic
    if (input) {
        input.addEventListener('focus', () => {
            document.getElementById('searchWidgetSection').classList.add('nlp-focused-mode');
            const backIcon = document.getElementById('nlpBackIcon');
            if (backIcon) backIcon.style.display = 'flex';
            if (customPlaceholder) {
                // Adjust placeholder position slightly since back icon appears
                customPlaceholder.style.left = '56px';
            }
        });
    }

    window.exitNlpMode = function(e) {
        if(e) e.stopPropagation();
        document.getElementById('searchWidgetSection').classList.remove('nlp-focused-mode');
        const backIcon = document.getElementById('nlpBackIcon');
        if (backIcon) backIcon.style.display = 'none';
        if (customPlaceholder) customPlaceholder.style.left = '16px';
        
        // Also hide trending prompts
        if (promptsSection) promptsSection.style.display = 'none';
        
        // Clear input
        if (input) {
            input.value = '';
            // Trigger input event to restore custom placeholder
            input.dispatchEvent(new Event('input'));
        }
    };
"""

# Inject before the end of the DOMContentLoaded block
js = js.replace('// Hide custom placeholder when typing', focused_mode_js + '\n        // Hide custom placeholder when typing')

with open('app.js', 'w') as f:
    f.write(js)

print("Added NLP Focused Mode!")
