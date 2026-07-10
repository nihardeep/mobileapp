import re

# 1. Update index.html
with open('index.html', 'r') as f:
    html = f.read()

old_search_panel_regex = r'<div class="search-widget-panel" id="searchWidgetSection">.*?(?=<!-- STUDENT HYPER-PERSONALIZED BANNER -->)'
match = re.search(old_search_panel_regex, html, re.DOTALL)

if match:
    old_panel = match.group(0)
    
    # We will wrap the old form inside manualSearchForm
    # We need to strip out the <div class="search-widget-panel" id="searchWidgetSection"> 
    # and the closing </div> from old_panel, but it's easier to just construct it.
    
    # Extract just the contents of search-widget-panel
    contents = old_panel.replace('<div class="search-widget-panel" id="searchWidgetSection">', '', 1)
    contents = contents.rsplit('</div>', 1)[0] # remove the last </div> which belongs to the panel
    
    # Remove the old mic icon from the inputGroupTo
    contents = re.sub(r'<div class="mic-icon-btn".*?</div>', '', contents, flags=re.DOTALL)
    
    new_panel = """<div class="search-widget-panel" id="searchWidgetSection" style="padding-bottom: 24px;">
    <!-- Intent Hero Section -->
    <div class="intent-hero-container">
        <div class="intent-input-wrapper">
            <input type="text" class="intent-text-input" placeholder="Where to next?" readonly onclick="toggleManualSearch()">
            <div class="intent-mic-btn" onclick="startVoiceSearch(event)">
                <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" fill="none" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                    <line x1="12" y1="19" x2="12" y2="22"/>
                </svg>
            </div>
        </div>
        <div class="intent-chips-container">
            <div class="intent-chip" onclick="simulateIntent('Relax at a beach 🏖️', 'GOI')">🏖️ Beach Holiday</div>
            <div class="intent-chip" onclick="simulateIntent('Quick business trip 💼', 'BOM')">💼 Quick Business Trip</div>
            <div class="intent-chip" onclick="simulateIntent('Visiting home 🏡', 'DEL')">🏡 Visiting Home</div>
            <div class="intent-chip" onclick="simulateIntent('Surprise me ✨', 'DXB')">✨ Surprise Me</div>
        </div>
    </div>

    <!-- Collapsible Manual Search Form -->
    <div id="manualSearchForm" class="manual-search-form" style="display: none; margin-top: 20px; border-top: 1px dashed rgba(0,0,0,0.1); padding-top: 20px;">
""" + contents + """
    </div>
</div>
"""
    
    html = html.replace(old_panel, new_panel)
    with open('index.html', 'w') as f:
        f.write(html)
    print("Updated index.html")
else:
    print("Could not find search-widget-panel in index.html")


# 2. Update style.css
with open('style.css', 'r') as f:
    css = f.read()

if ".intent-hero-container" not in css:
    intent_css = """
/* ==========================================================================
   INTENT HERO SECTION
   ========================================================================== */
.intent-hero-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.intent-input-wrapper {
    position: relative;
    width: 100%;
}

.intent-text-input {
    width: 100%;
    height: 64px;
    background: rgba(255, 255, 255, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.8);
    border-radius: 32px;
    padding: 0 70px 0 24px;
    font-size: 18px;
    font-weight: 700;
    color: var(--indigo-navy);
    box-shadow: inset 0 2px 4px rgba(255,255,255,0.5), 0 4px 12px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
    cursor: pointer;
}

.intent-text-input::placeholder {
    color: rgba(0, 31, 84, 0.5);
    font-weight: 600;
}

.intent-text-input:focus, .intent-text-input:active {
    outline: none;
    background: #fff;
    box-shadow: 0 8px 24px rgba(0, 31, 84, 0.1);
}

.intent-mic-btn {
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, var(--indigo-blue), #004d8a);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(0, 95, 169, 0.3);
    transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.intent-mic-btn:active {
    transform: translateY(-50%) scale(0.9);
}

.intent-chips-container {
    display: flex;
    gap: 10px;
    overflow-x: auto;
    padding-bottom: 4px;
    scrollbar-width: none; /* Firefox */
}
.intent-chips-container::-webkit-scrollbar {
    display: none;
}

.intent-chip {
    white-space: nowrap;
    padding: 10px 16px;
    background: rgba(255, 255, 255, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.8);
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    color: var(--indigo-navy);
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}

.intent-chip:hover, .intent-chip:active {
    background: rgba(255, 255, 255, 0.9);
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.manual-search-form {
    animation: fadeIn 0.4s ease;
}
"""
    css += intent_css
    with open('style.css', 'w') as f:
        f.write(css)
    print("Updated style.css")


# 3. Update app.js
with open('app.js', 'r') as f:
    js = f.read()

if "function toggleManualSearch()" not in js:
    js_append = """
// ==========================================================================
// INTENT SEARCH LOGIC
// ==========================================================================

function toggleManualSearch() {
    const form = document.getElementById('manualSearchForm');
    const input = document.querySelector('.intent-text-input');
    if (form.style.display === 'none') {
        form.style.display = 'block';
        input.placeholder = "Or search manually...";
        triggerHaptic('light', 'Manual search opened');
        
        // Ensure default values are populated if empty
        if (!appState.selectedFrom) {
            appState.selectedFrom = airports.find(ap => ap.code === 'DEL');
            document.getElementById('valFromCode').innerText = appState.selectedFrom.city;
        }
    } else {
        form.style.display = 'none';
        input.placeholder = "Where to next?";
    }
}

function simulateIntent(intentText, destinationCode) {
    const input = document.querySelector('.intent-text-input');
    input.value = intentText;
    triggerHaptic('success', 'Intent selected');
    
    // Simulate AI parsing intent
    setTimeout(() => {
        // Auto-fill some fields based on intent
        appState.selectedFrom = airports.find(ap => ap.code === 'DEL');
        appState.selectedTo = airports.find(ap => ap.code === destinationCode);
        
        if(appState.selectedTo) {
            document.getElementById('valFromCode').innerText = appState.selectedFrom.city;
            document.getElementById('valToCode').innerText = appState.selectedTo.city;
            
            // Open manual form to show the results of AI parsing
            const form = document.getElementById('manualSearchForm');
            form.style.display = 'block';
            
            // Auto search after a short delay
            setTimeout(() => {
                searchFlights();
            }, 800);
        }
    }, 600);
}
"""
    js += js_append
    with open('app.js', 'w') as f:
        f.write(js)
    print("Updated app.js")
