import re

with open('index.html', 'r') as f:
    html = f.read()

target_html = """                    <div style="padding: 0 24px 32px 24px;">
                        <h2 id="bankOfferSheetTitle" style="font-size: 22px; font-weight: 800; color: #000; margin: 0 0 12px 0;">SBIFLIGHT</h2>
                        <p id="bankOfferSheetDesc" style="font-size: 14px; color: #333; margin: 0 0 24px 0; line-height: 1.4;">Get upto 15% off on flight booking</p>

                        <div style="display: flex; align-items: center; justify-content: space-between; background: #F8FAFC; border-radius: 12px; padding: 12px 16px;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="width: 32px; height: 32px; background: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(0,0,0,0.05); color: #8A2B60; font-weight: bold; border: 1px solid #eee;">₹</div>
                                <div id="bankOfferSheetCode" style="font-size: 16px; font-weight: 600; color: #000; letter-spacing: 0.5px;">SBIFLIGHT</div>
                            </div>
                            <button onclick="copyBankOffer()" style="background: #fff; border: 1px solid #E2E8F0; border-radius: 6px; padding: 6px 12px; color: #0EA5E9; font-size: 12px; font-weight: 600; display: flex; align-items: center; gap: 6px; cursor: pointer;">
                                copy code
                                <svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" fill="none" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                            </button>
                        </div>

                        <div style="display: flex; flex-direction: column; align-items: center; margin-top: 24px;">
                            <div style="display: flex; gap: 6px; margin-bottom: 8px;">
                                <div style="width: 20px; height: 6px; border-radius: 3px; background: #888;"></div>
                                <div style="width: 6px; height: 6px; border-radius: 3px; background: #D1D5DB;"></div>
                                <div style="width: 6px; height: 6px; border-radius: 3px; background: #D1D5DB;"></div>
                                <div style="width: 6px; height: 6px; border-radius: 3px; background: #D1D5DB;"></div>
                                <div style="width: 6px; height: 6px; border-radius: 3px; background: #D1D5DB;"></div>
                            </div>
                            <div style="font-size: 12px; color: #000; font-weight: 500;">1/5</div>
                        </div>
                    </div>"""

def create_slide(code, desc):
    return f"""
        <div class="bank-offer-slide" style="flex: 0 0 100%; width: 100%; scroll-snap-align: start; padding: 0 24px; box-sizing: border-box;" data-code="{code}">
            <h2 style="font-size: 22px; font-weight: 800; color: #000; margin: 0 0 12px 0;">{code}</h2>
            <p style="font-size: 14px; color: #333; margin: 0 0 24px 0; line-height: 1.4;">{desc}</p>
            <div style="display: flex; align-items: center; justify-content: space-between; background: #F8FAFC; border-radius: 12px; padding: 12px 16px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 32px; height: 32px; background: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(0,0,0,0.05); color: #8A2B60; font-weight: bold; border: 1px solid #eee;">₹</div>
                    <div style="font-size: 16px; font-weight: 600; color: #000; letter-spacing: 0.5px;">{code}</div>
                </div>
                <button onclick="copyBankOffer('{code}')" style="background: #fff; border: 1px solid #E2E8F0; border-radius: 6px; padding: 6px 12px; color: #0EA5E9; font-size: 12px; font-weight: 600; display: flex; align-items: center; gap: 6px; cursor: pointer;">
                    copy code
                    <svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" fill="none" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                </button>
            </div>
        </div>"""

slides = (
    create_slide('AXIS20', 'AXIS BANK Debit card: Get upto 20% off on flight booking') +
    create_slide('SBIFLIGHT', 'SBI Bank: Get upto 15% off on flight booking') +
    create_slide('MOBI10', 'MobiKwik: Get upto 10% cashback') +
    create_slide('HDFC10', 'HDFC Bank Credit card: Get 10% instant discount') +
    create_slide('ICICIEMI', 'ICICI Bank EMI: No cost EMI for 3 & 6 months')
)

new_html_content = f"""                    <div id="bankOfferScrollContainer" style="display: flex; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; padding-bottom: 24px; -webkit-overflow-scrolling: touch; scroll-behavior: smooth;" onscroll="updateBankOfferDots()">
                        <style>#bankOfferScrollContainer::-webkit-scrollbar {{ display: none; }}</style>
                        {slides}
                    </div>

                    <div style="display: flex; flex-direction: column; align-items: center; padding-bottom: 32px;">
                        <div id="bankOfferDots" style="display: flex; gap: 6px; margin-bottom: 8px;">
                            <div class="dot active" style="width: 20px; height: 6px; border-radius: 3px; background: #888; transition: width 0.3s, background 0.3s;"></div>
                            <div class="dot" style="width: 6px; height: 6px; border-radius: 3px; background: #D1D5DB; transition: width 0.3s, background 0.3s;"></div>
                            <div class="dot" style="width: 6px; height: 6px; border-radius: 3px; background: #D1D5DB; transition: width 0.3s, background 0.3s;"></div>
                            <div class="dot" style="width: 6px; height: 6px; border-radius: 3px; background: #D1D5DB; transition: width 0.3s, background 0.3s;"></div>
                            <div class="dot" style="width: 6px; height: 6px; border-radius: 3px; background: #D1D5DB; transition: width 0.3s, background 0.3s;"></div>
                        </div>
                        <div id="bankOfferCount" style="font-size: 12px; color: #000; font-weight: 500;">1/5</div>
                    </div>"""

html = html.replace(target_html, new_html_content)

with open('index.html', 'w') as f:
    f.write(html)

with open('app.js', 'r') as f:
    js = f.read()

target_js = """function openBankOffer(code, desc) {
    triggerHaptic('medium', 'Open Bank Offer');
    
    // Update contents
    document.getElementById('bankOfferSheetTitle').innerText = code;
    document.getElementById('bankOfferSheetDesc').innerText = desc;
    document.getElementById('bankOfferSheetCode').innerText = code;
    
    // Open drawer
    const backdrop = document.getElementById('bottomSheetBackdrop');
    const drawer = document.getElementById('bankOfferDrawer');
    if (backdrop && drawer) {
        backdrop.classList.add('visible');
        drawer.classList.add('visible');
    }
}

function copyBankOffer() {
    triggerHaptic('success', 'Copied Bank Offer');
    
    // Attempt copy (navigator.clipboard) or fallback
    const code = document.getElementById('bankOfferSheetCode').innerText;
    if (navigator.clipboard) {
        navigator.clipboard.writeText(code);
    }
    
    // Show toast
    showToast("Copied and apply at checkout");
    
    // Close drawer
    setTimeout(() => {
        closeAllDrawers();
    }, 400); // slight delay for better UX
}"""

replacement_js = """function openBankOffer(code, desc) {
    triggerHaptic('medium', 'Open Bank Offer');
    
    // Open drawer
    const backdrop = document.getElementById('bottomSheetBackdrop');
    const drawer = document.getElementById('bankOfferDrawer');
    if (backdrop && drawer) {
        backdrop.classList.add('visible');
        drawer.classList.add('visible');
    }
    
    // Scroll to the correct slide
    const container = document.getElementById('bankOfferScrollContainer');
    const slides = container.querySelectorAll('.bank-offer-slide');
    let targetIndex = 0;
    slides.forEach((slide, idx) => {
        if (slide.getAttribute('data-code') === code) {
            targetIndex = idx;
        }
    });
    
    // Timeout to allow drawer to be visible before scrolling
    setTimeout(() => {
        container.scrollTo({ left: targetIndex * container.clientWidth, behavior: 'instant' });
        updateBankOfferDots();
    }, 10);
}

function updateBankOfferDots() {
    const container = document.getElementById('bankOfferScrollContainer');
    const dotsContainer = document.getElementById('bankOfferDots');
    const countDisplay = document.getElementById('bankOfferCount');
    if (!container || !dotsContainer) return;
    
    const index = Math.round(container.scrollLeft / container.clientWidth);
    const dots = dotsContainer.querySelectorAll('.dot');
    
    dots.forEach((dot, i) => {
        if (i === index) {
            dot.style.width = '20px';
            dot.style.background = '#888';
        } else {
            dot.style.width = '6px';
            dot.style.background = '#D1D5DB';
        }
    });
    
    if (countDisplay) {
        countDisplay.innerText = `${index + 1}/5`;
    }
}

function copyBankOffer(code) {
    triggerHaptic('success', 'Copied Bank Offer');
    
    if (navigator.clipboard && code) {
        navigator.clipboard.writeText(code);
    }
    
    // Show toast
    showToast("Copied and apply at checkout");
    
    // Close drawer
    setTimeout(() => {
        closeAllDrawers();
    }, 400); // slight delay for better UX
}"""

js = js.replace(target_js, replacement_js)

with open('app.js', 'w') as f:
    f.write(js)
