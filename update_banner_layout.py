import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace the shb content
old_shb_html = """                                        <div class="shb-title">Welcome back, Student!</div>
                                        <div class="shb-desc">10% Off • Free Date Change • +15Kg Extra Baggage</div>
                                    </div>
                                    <div class="shb-cta">Search ➔</div>
                                    <div class="shb-close" onclick="event.stopPropagation(); toggleStudentPersona()">✖</div>"""

new_shb_html = """                                        <div class="shb-title">Welcome back, Student!</div>
                                        <div class="shb-desc-animated">
                                            <span class="shb-offer-pill">10% Off</span>
                                            <span class="shb-offer-pill">Free Date Change</span>
                                            <span class="shb-offer-pill">+15Kg Baggage</span>
                                        </div>
                                    </div>
                                    <div class="shb-close-corner" onclick="event.stopPropagation(); toggleStudentPersona()">
                                        <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                                    </div>"""

html = html.replace(old_shb_html, new_shb_html)

with open('index.html', 'w') as f:
    f.write(html)


with open('style.css', 'r') as f:
    css = f.read()

# Add new CSS styles
new_css = """
/* Updated Student Banner Styles */
.student-hyper-banner {
    position: relative; /* For absolute close button */
    align-items: flex-start !important;
}

.shb-close-corner {
    position: absolute;
    top: 10px;
    right: 12px;
    color: #5a6b82;
    cursor: pointer;
    opacity: 0.5;
    transition: opacity 0.2s;
    padding: 4px;
}
.shb-close-corner:hover {
    opacity: 1;
}

.shb-desc-animated {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 6px;
}

.shb-offer-pill {
    background: rgba(255, 255, 255, 0.6);
    border: 1px solid rgba(96, 165, 250, 0.3);
    color: #005FA9;
    font-size: 10px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 12px;
    animation: pulsePill 2s infinite ease-in-out alternate;
}

.shb-offer-pill:nth-child(2) {
    animation-delay: 0.5s;
}
.shb-offer-pill:nth-child(3) {
    animation-delay: 1s;
}

@keyframes pulsePill {
    0% { transform: scale(1); box-shadow: 0 0 0 rgba(96, 165, 250, 0); }
    100% { transform: scale(1.02); box-shadow: 0 2px 8px rgba(96, 165, 250, 0.2); }
}
"""

css += new_css

with open('style.css', 'w') as f:
    f.write(css)

print("Updated banner layout and added animation!")
