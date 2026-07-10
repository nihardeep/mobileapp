import re

with open('index.html', 'r') as f:
    html = f.read()

# Add the autoSuggestionsSection right after trendingPromptsSection
auto_suggestions_html = """
        <div class="auto-suggestions-section" id="autoSuggestionsSection" style="display: none; background: #fafcff; border-radius: 24px; padding: 16px; box-shadow: 0 8px 30px rgba(0,31,84,0.06); border: 1px solid #eef2f6; animation: slideDown 0.2s ease;">
            <div class="auto-suggestion-item" onclick="simulateIntent('Help me find flight to goa', 'GOI')" style="padding: 12px; border-bottom: 1px solid rgba(0,0,0,0.03); cursor: pointer; color: var(--indigo-navy); font-size: 14px; font-weight: 500;">
                <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" fill="none" stroke-width="2" style="margin-right: 8px; vertical-align: text-bottom; color: var(--indigo-blue);"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                Help me find flight to goa
            </div>
            <div class="auto-suggestion-item" onclick="simulateIntent('Help me find flight to delhi', 'DEL')" style="padding: 12px; border-bottom: 1px solid rgba(0,0,0,0.03); cursor: pointer; color: var(--indigo-navy); font-size: 14px; font-weight: 500;">
                <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" fill="none" stroke-width="2" style="margin-right: 8px; vertical-align: text-bottom; color: var(--indigo-blue);"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                Help me find flight to delhi
            </div>
            <div class="auto-suggestion-item" onclick="simulateIntent('Help me find flight to beach destination', 'GOI')" style="padding: 12px; cursor: pointer; color: var(--indigo-navy); font-size: 14px; font-weight: 500;">
                <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" fill="none" stroke-width="2" style="margin-right: 8px; vertical-align: text-bottom; color: var(--indigo-blue);"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                Help me find flight to beach destination
            </div>
        </div>
"""

trending_regex = r'(<div class="trending-prompts-section" id="trendingPromptsSection".*?<!-- end search-widget-expanded-content -->)'
html = re.sub(r'</div>\s*</div>\s*<!-- end search-widget-expanded-content -->', '</div>\n' + auto_suggestions_html + '</div>\n<!-- end search-widget-expanded-content -->', html, count=1)

with open('index.html', 'w') as f:
    f.write(html)


with open('app.js', 'r') as f:
    js = f.read()

# Fix the exitNlpMode to properly hide prompts using document.getElementById
exit_nlp_regex = r'// Also hide trending prompts\s*if \(promptsSection\) promptsSection.style.display = \'none\';'
fixed_exit_nlp = """
        // Also hide trending prompts and auto suggestions
        const trendingSection = document.getElementById('trendingPromptsSection');
        const autoSection = document.getElementById('autoSuggestionsSection');
        if (trendingSection) trendingSection.style.display = 'none';
        if (autoSection) autoSection.style.display = 'none';
"""
js = re.sub(exit_nlp_regex, fixed_exit_nlp, js)


# Add input listener for auto suggestions
input_typing_logic = """
        input.addEventListener('input', (e) => {
            const val = e.target.value.toLowerCase();
            const trendingSection = document.getElementById('trendingPromptsSection');
            const autoSection = document.getElementById('autoSuggestionsSection');
            
            if (val.length === 0) {
                // If empty, show trending, hide auto
                if (trendingSection) trendingSection.style.display = 'block';
                if (autoSection) autoSection.style.display = 'none';
            } else if (val.includes('help me')) {
                // If they type help me, hide trending, show auto
                if (trendingSection) trendingSection.style.display = 'none';
                if (autoSection) autoSection.style.display = 'block';
            } else {
                // For now, if they type anything else, just hide both to be clean
                if (trendingSection) trendingSection.style.display = 'none';
                if (autoSection) autoSection.style.display = 'none';
            }
        });
"""

# Inject after input.addEventListener('focus', ...) block
focus_block_regex = r'input\.addEventListener\(\'focus\', \(\) => \{.*?\n        \}\);'
match = re.search(focus_block_regex, js, re.DOTALL)
if match:
    js = js.replace(match.group(0), match.group(0) + '\n' + input_typing_logic)

with open('app.js', 'w') as f:
    f.write(js)

print("Added auto suggestions logic!")
