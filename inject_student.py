import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Inject Hyper-Personalized Banner
hyper_banner = """
                            <!-- STUDENT HYPER-PERSONALIZED BANNER -->
                            <div class="student-hyper-banner" onclick="activateStudentSearch()">
                                <div class="shb-icon">🎓</div>
                                <div class="shb-content">
                                    <div class="shb-title">Welcome back, Student!</div>
                                    <div class="shb-desc">10% Off • Free Date Change • +15Kg Extra Baggage</div>
                                </div>
                                <div class="shb-cta">Search ➔</div>
                            </div>
"""
# find the end of the search widget
search_end = '</div><!-- end search-widget-expanded-content -->\n                            </div>'
if search_end in html and "<!-- STUDENT HYPER-PERSONALIZED BANNER -->" not in html:
    html = html.replace(search_end, search_end + "\n" + hyper_banner)


# 2. Inject Exclusive Offer Slide
offer_slide = """
                                        <!-- Slide 0: Student Exclusive -->
                                        <div class="carousel-slide offers-slide-0" onclick="activateStudentSearch()">
                                            <div class="offer-overlay">
                                                <div class="offer-title">Student Exclusive</div>
                                                <div class="offer-subtitle">10% Off + Free Change + 15Kg Baggage</div>
                                            </div>
                                        </div>"""

slide_track_start = '<div class="carousel-3d-track" id="offersCarousel">'
if slide_track_start in html and "<!-- Slide 0: Student Exclusive -->" not in html:
    html = html.replace(slide_track_start, slide_track_start + "\n" + offer_slide)

with open('index.html', 'w') as f:
    f.write(html)


# 3. Update CSS
with open('style.css', 'r') as f:
    css = f.read()

student_css = """
/* ==========================================================================
   STUDENT FLOW CSS
   ========================================================================== */
.student-hyper-banner {
    margin: 16px 0;
    padding: 12px 16px;
    background: linear-gradient(135deg, rgba(96, 165, 250, 0.15) 0%, rgba(167, 139, 250, 0.15) 100%);
    border: 1px solid rgba(96, 165, 250, 0.3);
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    transition: transform 0.2s;
}
.student-hyper-banner:active {
    transform: scale(0.97);
}
.shb-icon {
    font-size: 24px;
}
.shb-content {
    flex: 1;
}
.shb-title {
    font-size: 14px;
    font-weight: 800;
    color: #60a5fa;
    margin-bottom: 2px;
}
.shb-desc {
    font-size: 11px;
    color: #cbd5e1;
}
.shb-cta {
    font-size: 12px;
    font-weight: 700;
    color: #fff;
    background: var(--indigo-blue);
    padding: 6px 10px;
    border-radius: 6px;
}

.offers-slide-0 {
    background: url('https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800&h=600&fit=crop') center center / cover no-repeat;
}

.student-fare-active {
    background: rgba(52, 211, 153, 0.08) !important;
    border: 1px solid rgba(52, 211, 153, 0.3) !important;
}

.student-benefits-tags {
    margin-top: 6px;
    font-size: 9px;
    color: #34d399;
    font-weight: 600;
    line-height: 1.2;
}
.price-strikethrough {
    text-decoration: line-through;
    color: #64748b;
    font-size: 11px;
    margin-right: 4px;
    font-weight: 500;
}
"""
if "STUDENT FLOW CSS" not in css:
    css += student_css
    with open('style.css', 'w') as f:
        f.write(css)


# 4. Update JS
with open('app.js', 'r') as f:
    js = f.read()

# Add global var and function
student_js = """
let isStudentMode = false;

function activateStudentSearch() {
    triggerHaptic('medium', 'Student Offer Clicked');
    isStudentMode = true;
    searchFlights();
}
"""
if "let isStudentMode = false;" not in js:
    js = student_js + "\n" + js

# Update renderFlights function
# Find where it maps over flights to generate cards
old_map = "const cardsHtml = flights.map((f, i) => {"
new_map = """const cardsHtml = flights.map((f, i) => {
        let ecoPriceHtml = `₹ ${f.price}`;
        let ecoColClass = "fc-price-col";
        let ecoTagHtml = "";
        
        if (isStudentMode) {
            ecoColClass = "fc-price-col student-fare-active";
            const originalPriceNum = parseInt(f.price.replace(',', ''));
            const discountedPriceNum = Math.floor(originalPriceNum * 0.9);
            const discountedStr = discountedPriceNum.toLocaleString('en-IN');
            
            ecoPriceHtml = `<span class="price-strikethrough">₹${f.price}</span> ₹${discountedStr}`;
            ecoTagHtml = `<div class="student-benefits-tags">✨ Free Date Change<br>🧳 +15kg Baggage</div>`;
        }
"""

if "if (isStudentMode) {" not in js:
    js = js.replace(old_map, new_map)
    
    # Also need to inject ecoPriceHtml, ecoColClass, and ecoTagHtml into the card HTML template inside the map
    # Look for the exact lines in app.js
    old_eco_col = """                <div class="fc-price-col">
                    <div class="fc-class-name eco">Economy</div>
                    <div class="fc-price-val">₹ ${f.price} <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></div>
                </div>"""
                
    new_eco_col = """                <div class="${ecoColClass}">
                    <div class="fc-class-name eco">Economy</div>
                    <div class="fc-price-val">${ecoPriceHtml} <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></div>
                    ${ecoTagHtml}
                </div>"""
                
    js = js.replace(old_eco_col, new_eco_col)

with open('app.js', 'w') as f:
    f.write(js)

print("Injected Student Flow!")
