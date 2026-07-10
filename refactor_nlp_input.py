import re

# 1. Update index.html
with open('index.html', 'r') as f:
    html = f.read()

# Replace tab text
html = html.replace('✨ Ask Myra', '✨ Ask 6eSkai')

# Replace the NLP Search View content
old_nlp_view_regex = r'<div id="nlpSearchView" class="search-view-container" style="display: none;">(.*?)</div>\s*</div>\s*<!-- end search-widget-expanded-content -->'
match = re.search(old_nlp_view_regex, html, re.DOTALL)

if match:
    # Build the new NLP search view inner HTML
    new_nlp_inner = """
        <div class="nlp-input-wrapper">
            <div class="nlp-back-icon">
                <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
            </div>
            <input type="text" class="nlp-placeholder" placeholder="Ask 6eSkai about 'Coorg Homestays'" onfocus="document.getElementById('trendingPromptsSection').style.display='block'">
            <div class="nlp-mic-icon" onclick="startVoiceSearch(event)">
                <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" fill="none" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                    <line x1="12" y1="19" x2="12" y2="22"/>
                </svg>
            </div>
        </div>
        
        <div class="trending-prompts-section" id="trendingPromptsSection" style="display: none;">
            <div class="trending-prompts-title">TRENDING PROMPTS</div>
            
            <div class="trending-prompt-card" onclick="simulateIntent('Cheapest flights to Goa', 'GOI')">
                <div class="tpc-icon" style="background: #e6f2ff;">✈️</div>
                <div class="tpc-content">
                    <div class="tpc-tag"><svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L14 19v-5.5l8 2.5z"/></svg> FLIGHTS</div>
                    <div class="tpc-text">Cheapest flights to Goa</div>
                </div>
            </div>

            <div class="trending-prompt-card" onclick="simulateIntent('Flights to Beach destinations', 'GOI')">
                <div class="tpc-icon" style="background: #e0f7fa;">🏖️</div>
                <div class="tpc-content">
                    <div class="tpc-tag"><svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L14 19v-5.5l8 2.5z"/></svg> FLIGHTS</div>
                    <div class="tpc-text">Flights to Beach destinations</div>
                </div>
            </div>

            <div class="trending-prompt-card" onclick="simulateIntent('Flight to Europe', 'CDG')">
                <div class="tpc-icon" style="background: #f3e5f5;">🌍</div>
                <div class="tpc-content">
                    <div class="tpc-tag"><svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L14 19v-5.5l8 2.5z"/></svg> FLIGHTS</div>
                    <div class="tpc-text">Flight to Europe</div>
                </div>
            </div>
        </div>
"""
    
    html = html.replace(match.group(1), new_nlp_inner)
    with open('index.html', 'w') as f:
        f.write(html)
    print("Updated index.html")
else:
    print("Could not find nlpSearchView in index.html")


# 2. Update CSS for input element
with open('style.css', 'r') as f:
    css = f.read()

# We need to make sure .nlp-placeholder looks right as an input
old_css = """.nlp-placeholder {
    flex: 1;
    color: var(--text-secondary);
    font-size: 15px;
    font-weight: 500;
}"""

new_css = """input.nlp-placeholder {
    flex: 1;
    color: var(--indigo-navy);
    font-size: 15px;
    font-weight: 600;
    border: none;
    background: transparent;
    outline: none;
    width: 100%;
}
input.nlp-placeholder::placeholder {
    color: var(--text-secondary);
    font-weight: 500;
}"""

css = css.replace(old_css, new_css)
with open('style.css', 'w') as f:
    f.write(css)
print("Updated style.css")
