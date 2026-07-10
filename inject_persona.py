import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Add Dev Sidebar Button
btn_injection = """                    <button class="dev-trigger-btn" id="btnStateStudentPersona" onclick="toggleStudentPersona()">
                        🎓 Student Persona
                        <div class="dev-btn-indicator"></div>
                    </button>
                </div>"""

if "btnStateStudentPersona" not in html:
    html = html.replace('                </div>\n            </div>\n\n            <div class="dev-state-group">', btn_injection + '\n            </div>\n\n            <div class="dev-state-group">')

# 2. Wrap the banner
old_banner = """                            <!-- STUDENT HYPER-PERSONALIZED BANNER -->
                            <div class="student-hyper-banner" onclick="openStudentHub()">
                                <div class="shb-icon">🎓</div>
                                <div class="shb-content">
                                    <div class="shb-title">Welcome back, Student!</div>
                                    <div class="shb-desc">10% Off • Free Date Change • +15Kg Extra Baggage</div>
                                </div>
                                <div class="shb-cta">Search ➔</div>
                            </div>"""

new_banner = """                            <!-- STUDENT HYPER-PERSONALIZED BANNER -->
                            <div class="student-hyper-banner-wrapper" id="studentBannerWrapper">
                                <div class="student-hyper-banner" onclick="openStudentHub()">
                                    <div class="shb-icon">🎓</div>
                                    <div class="shb-content">
                                        <div class="shb-title">Welcome back, Student!</div>
                                        <div class="shb-desc">10% Off • Free Date Change • +15Kg Extra Baggage</div>
                                    </div>
                                    <div class="shb-cta">Search ➔</div>
                                </div>
                            </div>"""

if "studentBannerWrapper" not in html:
    html = html.replace(old_banner, new_banner)

# 3. Hide carousel slide 0 by default
old_slide = '<div class="carousel-slide offers-slide-0" onclick="openStudentHub()">'
new_slide = '<div class="carousel-slide offers-slide-0" id="studentCarouselSlide" onclick="openStudentHub()" style="display: none;">'

if 'id="studentCarouselSlide"' not in html:
    html = html.replace(old_slide, new_slide)

# Set search widget to z-index so banner slides under it
search_widget_old = '<div class="search-widget-container" id="searchWidgetMainContainer">'
search_widget_new = '<div class="search-widget-container" id="searchWidgetMainContainer" style="position: relative; z-index: 10;">'

if search_widget_new not in html:
    html = html.replace(search_widget_old, search_widget_new)

with open('index.html', 'w') as f:
    f.write(html)


# 4. Update CSS
with open('style.css', 'r') as f:
    css = f.read()

# Replace the old student-hyper-banner CSS
old_css_banner = """.student-hyper-banner {
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
}"""

new_css_banner = """.student-hyper-banner-wrapper {
    overflow: hidden;
    margin-top: -24px; /* Pull it up under the search widget */
    padding-top: 24px; /* Give it space to slide without getting cut off immediately */
    margin-bottom: 0;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    max-height: 0;
    opacity: 0;
}

.student-hyper-banner-wrapper.active {
    max-height: 120px;
    opacity: 1;
    margin-bottom: 16px;
}

.student-hyper-banner {
    padding: 12px 16px;
    background: linear-gradient(135deg, rgba(96, 165, 250, 0.15) 0%, rgba(167, 139, 250, 0.15) 100%);
    border: 1px solid rgba(96, 165, 250, 0.3);
    border-bottom-left-radius: 16px;
    border-bottom-right-radius: 16px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    transform: translateY(-100%);
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.student-hyper-banner-wrapper.active .student-hyper-banner {
    transform: translateY(0);
}"""

if ".student-hyper-banner-wrapper" not in css:
    css = css.replace(old_css_banner, new_css_banner)
    with open('style.css', 'w') as f:
        f.write(css)


# 5. Update JS
with open('app.js', 'r') as f:
    js = f.read()

new_js_logic = """
let isStudentPersonaActive = false;

function toggleStudentPersona() {
    isStudentPersonaActive = !isStudentPersonaActive;
    
    const btn = document.getElementById('btnStateStudentPersona');
    if (btn) {
        if (isStudentPersonaActive) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    }
    
    const wrapper = document.getElementById('studentBannerWrapper');
    if (wrapper) {
        if (isStudentPersonaActive) {
            wrapper.classList.add('active');
            triggerHaptic('medium', 'Student Persona On');
        } else {
            wrapper.classList.remove('active');
            triggerHaptic('light', 'Student Persona Off');
        }
    }
    
    const carouselSlide = document.getElementById('studentCarouselSlide');
    if (carouselSlide) {
        carouselSlide.style.display = isStudentPersonaActive ? 'block' : 'none';
    }
}
"""

if "toggleStudentPersona" not in js:
    # Just append it to the top after isStudentMode
    js = js.replace('let isStudentMode = false;', 'let isStudentMode = false;' + new_js_logic)
    with open('app.js', 'w') as f:
        f.write(js)

print("Injected Persona Toggle and Merge Animation!")
