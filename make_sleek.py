import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace the nlpSearchView with a much sleeker version
sleek_nlp_html = """
    <div id="nlpSearchView" class="search-view-container" style="display: block;">
        <div class="nlp-input-wrapper" style="background: #fff; border-radius: 32px; padding: 12px 20px; box-shadow: 0 4px 20px rgba(0,31,84,0.08); border: none; display: flex; align-items: center; margin-bottom: 16px;">
            <div class="nlp-back-icon" style="color: var(--text-secondary); margin-right: 12px; cursor: pointer;">
                <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
            </div>
            <input type="text" id="nlpSearchInput" class="nlp-placeholder" placeholder="Ask 6eSkai about 'Coorg Homestays'" style="flex: 1; color: var(--indigo-navy); font-size: 16px; font-weight: 500; border: none; background: transparent; outline: none; width: 100%;">
            <div class="nlp-mic-icon" onclick="startVoiceSearch(event)" style="background: #fff; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 0 2px rgba(0,95,169,0.2), 0 0 0 6px rgba(0,95,169,0.05); color: var(--indigo-blue); cursor: pointer; transition: all 0.3s ease;">
                <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" fill="none" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                    <line x1="12" y1="19" x2="12" y2="22"/>
                </svg>
            </div>
        </div>
        
        <div class="trending-prompts-section" id="trendingPromptsSection" style="display: none; background: #fafcff; border-radius: 24px; padding: 24px; box-shadow: 0 8px 30px rgba(0,31,84,0.06); border: 1px solid #eef2f6; animation: slideDown 0.3s ease;">
            <div class="trending-prompts-title" style="font-size: 13px; font-weight: 800; color: #5a6b82; letter-spacing: 0.5px; margin-bottom: 20px; text-transform: uppercase;">TRENDING PROMPTS</div>
            
            <div class="trending-prompt-card" onclick="simulateIntent('Cheapest flights to Goa', 'GOI')" style="display: flex; align-items: center; gap: 16px; padding: 12px 0; border-bottom: 1px solid rgba(0,0,0,0.03); cursor: pointer;">
                <div class="tpc-icon" style="width: 56px; height: 56px; background: #e8f4fc; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 28px; flex-shrink: 0; box-shadow: inset 0 2px 4px rgba(255,255,255,0.5);">✈️</div>
                <div class="tpc-content" style="flex: 1;">
                    <div class="tpc-tag" style="display: inline-flex; align-items: center; gap: 4px; color: var(--indigo-blue); border: 1px solid rgba(0,95,169,0.2); font-size: 10px; font-weight: 700; padding: 4px 8px; border-radius: 6px; margin-bottom: 6px; text-transform: uppercase;"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L14 19v-5.5l8 2.5z"/></svg> FLIGHTS</div>
                    <div class="tpc-text" style="font-size: 15px; font-weight: 500; color: var(--indigo-navy); line-height: 1.3;">Cheapest flights to Goa</div>
                </div>
            </div>

            <div class="trending-prompt-card" onclick="simulateIntent('Flights to Beach destinations', 'GOI')" style="display: flex; align-items: center; gap: 16px; padding: 12px 0; border-bottom: 1px solid rgba(0,0,0,0.03); cursor: pointer;">
                <div class="tpc-icon" style="width: 56px; height: 56px; background: #e0f7fa; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 28px; flex-shrink: 0; box-shadow: inset 0 2px 4px rgba(255,255,255,0.5);">🏖️</div>
                <div class="tpc-content" style="flex: 1;">
                    <div class="tpc-tag" style="display: inline-flex; align-items: center; gap: 4px; color: var(--indigo-blue); border: 1px solid rgba(0,95,169,0.2); font-size: 10px; font-weight: 700; padding: 4px 8px; border-radius: 6px; margin-bottom: 6px; text-transform: uppercase;"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L14 19v-5.5l8 2.5z"/></svg> FLIGHTS</div>
                    <div class="tpc-text" style="font-size: 15px; font-weight: 500; color: var(--indigo-navy); line-height: 1.3;">Flights to Beach destinations</div>
                </div>
            </div>

            <div class="trending-prompt-card" onclick="simulateIntent('Flight to Europe', 'CDG')" style="display: flex; align-items: center; gap: 16px; padding: 12px 0; cursor: pointer;">
                <div class="tpc-icon" style="width: 56px; height: 56px; background: #f3e5f5; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 28px; flex-shrink: 0; box-shadow: inset 0 2px 4px rgba(255,255,255,0.5);">🌍</div>
                <div class="tpc-content" style="flex: 1;">
                    <div class="tpc-tag" style="display: inline-flex; align-items: center; gap: 4px; color: var(--indigo-blue); border: 1px solid rgba(0,95,169,0.2); font-size: 10px; font-weight: 700; padding: 4px 8px; border-radius: 6px; margin-bottom: 6px; text-transform: uppercase;"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L14 19v-5.5l8 2.5z"/></svg> FLIGHTS</div>
                    <div class="tpc-text" style="font-size: 15px; font-weight: 500; color: var(--indigo-navy); line-height: 1.3;">Flight to Europe</div>
                </div>
            </div>
        </div>
"""

old_nlp_view_regex = r'<div id="nlpSearchView" class="search-view-container" style="display: block;">(.*?)</div>\s*</div>\s*<!-- end search-widget-expanded-content -->'
match = re.search(old_nlp_view_regex, html, re.DOTALL)

if match:
    # Safely replace the nlpSearchView content
    html = html.replace(match.group(0), sleek_nlp_html + '\n</div>\n<!-- end search-widget-expanded-content -->')
else:
    print("Failed to find nlpSearchView using regex!")

# Add click event listener to window in app.js to hide the trending prompts when clicking outside
js_snippet = """
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('nlpSearchInput');
    const promptsSection = document.getElementById('trendingPromptsSection');
    
    if (searchInput) {
        searchInput.addEventListener('click', (e) => {
            e.stopPropagation();
            if (promptsSection) promptsSection.style.display = 'block';
        });
    }

    document.addEventListener('click', (e) => {
        if (promptsSection && !promptsSection.contains(e.target) && e.target !== searchInput) {
            promptsSection.style.display = 'none';
        }
    });
});
"""

with open('app.js', 'a') as f:
    f.write(js_snippet)

# Ensure the search input no longer has the inline onfocus that might trigger aggressively
html = html.replace('onfocus="document.getElementById(\'trendingPromptsSection\').style.display=\'block\'"', '')

with open('index.html', 'w') as f:
    f.write(html)
print("Updated design and interaction!")
