import re

with open('index.html', 'r') as f:
    html = f.read()

old_shb_html = """                                    <div class="shb-icon">🎓</div>
                                    <div class="shb-content">
                                        <div class="shb-title">Welcome back, Student!</div>
                                        <div class="shb-desc-animated">
                                            <span class="shb-offer-pill">10% Off</span>
                                            <span class="shb-offer-pill">Free Date Change</span>
                                            <span class="shb-offer-pill">+15Kg Baggage</span>
                                        </div>
                                    </div>"""

new_shb_html = """                                    <div class="shb-content">
                                        <div class="shb-title">Welcome back, Nihar! <span style="font-size: 16px;">🎓</span></div>
                                        <div class="shb-desc-premium">
                                            <span style="color: #005FA9; margin-right: 4px;">✨</span> 
                                            Applying your perks: <strong>10% Off</strong>, <strong>Free Date Change</strong>, & <strong>+15Kg Baggage</strong>.
                                        </div>
                                    </div>"""

html = html.replace(old_shb_html, new_shb_html)

with open('index.html', 'w') as f:
    f.write(html)


with open('style.css', 'r') as f:
    css = f.read()

new_css = """
/* Premium Personalized Banner Styles */
.shb-title {
    color: var(--indigo-navy) !important;
    font-weight: 800 !important;
    font-size: 15px;
    margin-bottom: 4px;
}

.shb-desc-premium {
    color: #5a6b82;
    font-size: 12px;
    font-weight: 500;
    line-height: 1.4;
}

.shb-desc-premium strong {
    color: var(--indigo-navy);
    font-weight: 700;
}
"""

css += new_css

with open('style.css', 'w') as f:
    f.write(css)

print("Updated banner to premium personalized design!")
