import re

# 1. Update index.html
with open('index.html', 'r') as f:
    html = f.read()

# Find the whole search-widget-panel block
old_panel_regex = r'<div class="search-widget-panel" id="searchWidgetSection".*?<!-- end search-widget-expanded-content -->\s*</div>'
match = re.search(old_panel_regex, html, re.DOTALL)

if match:
    old_panel = match.group(0)
    
    # Extract the manual search form part (route-row, date/pax, search btn)
    # We can pull out everything inside <div id="manualSearchForm"...>
    manual_form_regex = r'<div id="manualSearchForm" class="manual-search-form".*?>(.*)</div><!-- end search-widget-expanded-content -->'
    manual_match = re.search(manual_form_regex, old_panel, re.DOTALL)
    
    if manual_match:
        manual_html = manual_match.group(1)
        
        # Build the new search widget panel
        new_panel = """<div class="search-widget-panel" id="searchWidgetSection" style="padding-bottom: 24px;">
    
    <!-- Mode Toggle Header -->
    <div class="search-mode-toggle">
        <div class="search-mode-tab active" id="tabManual" onclick="toggleSearchMode('manual')">Manual Search</div>
        <div class="search-mode-tab" id="tabNLP" onclick="toggleSearchMode('nlp')">✨ Ask Myra</div>
    </div>

    <!-- Manual Search View (Default) -->
    <div id="manualSearchView" class="search-view-container active-view">
""" + manual_html + """
    </div>

    <!-- AI NLP Search View (Hidden) -->
    <div id="nlpSearchView" class="search-view-container" style="display: none;">
        <div class="nlp-input-wrapper" onclick="startVoiceSearch(event)">
            <div class="nlp-back-icon">
                <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
            </div>
            <div class="nlp-placeholder">Ask Myra about 'Coorg Homestays'</div>
            <div class="nlp-mic-icon">
                <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" fill="none" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                    <line x1="12" y1="19" x2="12" y2="22"/>
                </svg>
            </div>
        </div>
        
        <div class="trending-prompts-section">
            <div class="trending-prompts-title">TRENDING PROMPTS</div>
            
            <div class="trending-prompt-card" onclick="simulateIntent('Cheapest flights to Goa', 'GOI')">
                <div class="tpc-icon" style="background: #e6f2ff;">✈️</div>
                <div class="tpc-content">
                    <div class="tpc-tag"><svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L14 19v-5.5l8 2.5z"/></svg> FLIGHTS</div>
                    <div class="tpc-text">Cheapest flights to Goa</div>
                </div>
            </div>

            <div class="trending-prompt-card" onclick="simulateIntent('Find me a weekend getaway under ₹5,000', 'JAI')">
                <div class="tpc-icon" style="background: #e0f7fa;">💸</div>
                <div class="tpc-content">
                    <div class="tpc-tag"><svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L14 19v-5.5l8 2.5z"/></svg> FLIGHTS</div>
                    <div class="tpc-text">Find me a weekend getaway under ₹5,000</div>
                </div>
            </div>

            <div class="trending-prompt-card" onclick="simulateIntent('Next flight to Delhi this evening', 'DEL')">
                <div class="tpc-icon" style="background: #f3e5f5;">⏱️</div>
                <div class="tpc-content">
                    <div class="tpc-tag"><svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L14 19v-5.5l8 2.5z"/></svg> FLIGHTS</div>
                    <div class="tpc-text">Next flight to Delhi this evening</div>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- end search-widget-expanded-content -->"""
        
        # Replace the old panel
        html = html.replace(old_panel, new_panel)
        with open('index.html', 'w') as f:
            f.write(html)
        print("Updated index.html")
    else:
        print("Could not extract manual form.")
else:
    print("Could not find old panel.")


# 2. Update CSS
with open('style.css', 'r') as f:
    css = f.read()

if ".search-mode-toggle" not in css:
    new_css = """
/* ==========================================================================
   SEARCH MODE TOGGLE & NLP UI
   ========================================================================== */
.search-mode-toggle {
    display: flex;
    background: rgba(0, 31, 84, 0.04);
    border-radius: 12px;
    padding: 4px;
    margin-bottom: 16px;
}

.search-mode-tab {
    flex: 1;
    text-align: center;
    padding: 10px 0;
    font-size: 13px;
    font-weight: 700;
    color: var(--text-secondary);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.search-mode-tab.active {
    background: #fff;
    color: var(--indigo-blue);
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.search-view-container {
    animation: fadeIn 0.4s ease;
}

/* NLP Search Input */
.nlp-input-wrapper {
    display: flex;
    align-items: center;
    background: #fff;
    border-radius: 32px;
    padding: 12px 16px;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.02), 0 2px 8px rgba(0,0,0,0.04);
    border: 1px solid rgba(0,31,84,0.05);
    margin-bottom: 24px;
    cursor: pointer;
}

.nlp-back-icon {
    color: var(--text-secondary);
    margin-right: 12px;
    display: flex;
}

.nlp-placeholder {
    flex: 1;
    color: var(--text-secondary);
    font-size: 15px;
    font-weight: 500;
}

.nlp-mic-icon {
    color: #fff;
    background: linear-gradient(135deg, var(--indigo-blue), #004d8a);
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 6px rgba(0, 95, 169, 0.3);
}

/* Trending Prompts Section */
.trending-prompts-title {
    font-size: 11px;
    font-weight: 800;
    color: var(--text-secondary);
    letter-spacing: 0.5px;
    margin-bottom: 12px;
    margin-left: 4px;
}

.trending-prompt-card {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 16px;
    cursor: pointer;
    padding: 8px 4px;
    transition: transform 0.2s ease;
}

.trending-prompt-card:active {
    transform: scale(0.98);
}

.tpc-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    flex-shrink: 0;
}

.tpc-content {
    flex: 1;
}

.tpc-tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    color: var(--indigo-blue);
    background: rgba(0, 95, 169, 0.05);
    border: 1px solid rgba(0, 95, 169, 0.15);
    font-size: 9px;
    font-weight: 700;
    padding: 3px 6px;
    border-radius: 4px;
    margin-bottom: 6px;
    text-transform: uppercase;
}

.tpc-text {
    font-size: 14px;
    font-weight: 500;
    color: var(--indigo-navy);
    line-height: 1.4;
}
"""
    css += new_css
    with open('style.css', 'w') as f:
        f.write(css)
    print("Updated style.css")


# 3. Update app.js
with open('app.js', 'r') as f:
    js = f.read()

if "function toggleSearchMode" not in js:
    js_append = """
function toggleSearchMode(mode) {
    const tabManual = document.getElementById('tabManual');
    const tabNLP = document.getElementById('tabNLP');
    const viewManual = document.getElementById('manualSearchView');
    const viewNLP = document.getElementById('nlpSearchView');
    
    if (mode === 'manual') {
        tabManual.classList.add('active');
        tabNLP.classList.remove('active');
        viewManual.style.display = 'block';
        viewNLP.style.display = 'none';
        triggerHaptic('light', 'Manual Mode');
    } else {
        tabNLP.classList.add('active');
        tabManual.classList.remove('active');
        viewNLP.style.display = 'block';
        viewManual.style.display = 'none';
        triggerHaptic('light', 'NLP Mode');
    }
}
"""
    js += js_append
    with open('app.js', 'w') as f:
        f.write(js)
    print("Updated app.js")

