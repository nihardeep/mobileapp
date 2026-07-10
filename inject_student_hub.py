import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update onclick handlers on homepage banners to open Student Hub instead of searching immediately
html = html.replace('onclick="activateStudentSearch()"', 'onclick="openStudentHub()"')

# 2. Inject screenStudentHub
student_hub_html = """
                <!-- ==========================================================
                     SCREEN: STUDENT HUB
                     ========================================================== -->
                <div class="screen" id="screenStudentHub">
                    <div class="student-hub-header">
                        <div class="sh-nav-bar">
                            <div class="back-btn-chevron" onclick="navigateTo('home')">
                                <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="15 18 9 12 15 6"></polyline>
                                </svg>
                            </div>
                            <div class="sh-nav-title">Student Exclusive</div>
                        </div>
                        
                        <div class="sh-hero-content">
                            <h1 class="sh-hero-title">Travel Smarter,<br>Study Harder 🎓</h1>
                            <p class="sh-hero-subtitle">Unlock your exclusive student benefits and save big on your next journey home or away.</p>
                            
                            <div class="sh-benefits-row">
                                <div class="sh-benefit-item">
                                    <div class="sh-benefit-icon">💸</div>
                                    <span>10% Off Fares</span>
                                </div>
                                <div class="sh-benefit-item">
                                    <div class="sh-benefit-icon">🧳</div>
                                    <span>+15Kg Extra Baggage</span>
                                </div>
                                <div class="sh-benefit-item">
                                    <div class="sh-benefit-icon">📅</div>
                                    <span>Free Date Change</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="student-hub-body">
                        <!-- Embedded Flight Search Widget Replica -->
                        <div class="search-widget-container" style="margin-top: -30px; position: relative; z-index: 10; border: 1px solid rgba(255, 255, 255, 0.1);">
                            <div class="search-widget-header">
                                <div class="tab active">Flights</div>
                            </div>
                            <div class="search-widget-content" style="padding: 16px;">
                                <div class="search-route-row" style="margin-bottom: 12px; display: flex; gap: 8px;">
                                    <div class="input-group" style="flex: 1;">
                                        <div class="input-label">From</div>
                                        <div class="input-value" style="font-size: 16px;">Delhi (DEL)</div>
                                    </div>
                                    <div class="input-group" style="flex: 1;">
                                        <div class="input-label">To</div>
                                        <div class="input-value" style="font-size: 16px;">Mumbai (BOM)</div>
                                    </div>
                                </div>
                                <div class="search-details-row" style="margin-bottom: 16px; display: flex; gap: 8px;">
                                    <div class="input-group" style="flex: 1;">
                                        <div class="input-label">Departure</div>
                                        <div class="input-value">22 Jan 2026</div>
                                    </div>
                                    <div class="input-group" style="flex: 1;">
                                        <div class="input-label">Travelers</div>
                                        <div class="input-value">1 Student</div>
                                    </div>
                                </div>
                                <button class="riyadh-search-btn" style="width: 100%;" onclick="activateStudentModeAndSearch()">
                                    Search Student Fares ➔
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
"""

dest_ai_start = '<div class="screen" id="screenDestinationAI">'
if dest_ai_start in html and "SCREEN: STUDENT HUB" not in html:
    html = html.replace(dest_ai_start, student_hub_html + "\n" + dest_ai_start)

with open('index.html', 'w') as f:
    f.write(html)


# 3. Update CSS
with open('style.css', 'r') as f:
    css = f.read()

student_hub_css = """
/* ==========================================================================
   STUDENT HUB SCREEN
   ========================================================================== */
.student-hub-header {
    background: linear-gradient(135deg, #FF9900 0%, #FF5E00 100%);
    padding: 60px 20px 40px 20px;
    border-bottom-left-radius: 24px;
    border-bottom-right-radius: 24px;
    color: white;
    position: relative;
    overflow: hidden;
}

/* Add a subtle map/texture overlay to the gradient */
.student-hub-header::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: url('world_map_texture.png') center/cover;
    opacity: 0.1;
    mix-blend-mode: overlay;
    pointer-events: none;
}

.sh-nav-bar {
    display: flex;
    align-items: center;
    margin-bottom: 24px;
    position: relative;
    z-index: 2;
}

.sh-nav-title {
    font-size: 16px;
    font-weight: 700;
    margin-left: 12px;
}

.sh-hero-title {
    font-size: 28px;
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 8px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    position: relative;
    z-index: 2;
}

.sh-hero-subtitle {
    font-size: 13px;
    font-weight: 500;
    opacity: 0.9;
    margin-bottom: 24px;
    line-height: 1.4;
    position: relative;
    z-index: 2;
}

.sh-benefits-row {
    display: flex;
    gap: 8px;
    position: relative;
    z-index: 2;
}

.sh-benefit-item {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 8px 6px;
    border-radius: 12px;
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 6px;
}

.sh-benefit-icon {
    font-size: 20px;
    background: white;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.sh-benefit-item span {
    font-size: 10px;
    font-weight: 700;
    line-height: 1.2;
}

.student-hub-body {
    padding: 0 20px 40px 20px;
}

/* Subtle flight card badge */
.flight-card {
    position: relative;
    overflow: visible; /* To allow the badge to stick out slightly if needed, or we can keep it inside */
}

.student-edge-badge {
    position: absolute;
    top: -8px;
    right: 12px;
    background: linear-gradient(90deg, #34d399 0%, #10b981 100%);
    color: white;
    font-size: 9px;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(16, 185, 129, 0.3);
    z-index: 5;
    letter-spacing: 0.2px;
    border: 1px solid rgba(255,255,255,0.2);
}
"""
if "STUDENT HUB SCREEN" not in css:
    css += student_hub_css
    with open('style.css', 'w') as f:
        f.write(css)


# 4. Update JS logic
with open('app.js', 'r') as f:
    js = f.read()

# Replace activateStudentSearch with the new logic
old_js_student = """function activateStudentSearch() {
    triggerHaptic('medium', 'Student Offer Clicked');
    isStudentMode = true;
    searchFlights();
}"""

new_js_student = """function openStudentHub() {
    triggerHaptic('medium', 'Student Offer Clicked');
    navigateTo('studentHub');
}

function activateStudentModeAndSearch() {
    triggerHaptic('heavy', 'Search Student Fares');
    isStudentMode = true;
    searchFlights();
}"""

if "function openStudentHub()" not in js:
    js = js.replace(old_js_student, new_js_student)
    
# Add navigateTo case for studentHub
# Need to inject into switch(screenId) { ... } inside navigateTo(screenId)
# I'll just rely on the existing hideAllScreens and screen element display logic in navigateTo.
# `navigateTo(screenId)` uses `document.getElementById('screen' + screenId.charAt(0).toUpperCase() + screenId.slice(1))`.
# So `navigateTo('studentHub')` looks for `screenStudentHub`. This automatically works!

# Update renderFlights to use edge badge instead of tag inside the column
old_map = """            ecoPriceHtml = `<span class="price-strikethrough">₹${f.price}</span> ₹${discountedStr}`;
            ecoTagHtml = `<div class="student-benefits-tags">✨ Free Date Change<br>🧳 +15kg Baggage</div>`;"""

new_map = """            ecoPriceHtml = `<span class="price-strikethrough">₹${f.price}</span> ₹${discountedStr}`;
            // Moved to the top edge of the card, so we don't need ecoTagHtml here anymore
            ecoTagHtml = "";"""

js = js.replace(old_map, new_map)

# Inject the edge badge into the flight-card template
old_card_html = """        return `
        <div class="flight-card" id="flightCard-${i}">
            <div class="fc-header">"""

new_card_html = """        let edgeBadgeHtml = "";
        if (isStudentMode) {
            edgeBadgeHtml = `<div class="student-edge-badge">✨ Free Change • 🧳 15Kg Extra</div>`;
        }

        return `
        <div class="flight-card" id="flightCard-${i}">
            ${edgeBadgeHtml}
            <div class="fc-header">"""

if "edgeBadgeHtml" not in js:
    js = js.replace(old_card_html, new_card_html)

with open('app.js', 'w') as f:
    f.write(js)

print("Injected Student Hub and Subtle UI")
