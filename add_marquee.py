import re

with open('index.html', 'r') as f:
    html = f.read()

# The marquee HTML block
marquee_html = """
                            <!-- Bank Offers Marquee -->
                            <div class="offers-marquee-wrapper">
                                <div class="offers-marquee-track">
                                    <div class="marquee-item"><span class="m-icon">🏦</span> <strong>SBI Bank:</strong> Get upto 15% off on flight booking</div>
                                    <div class="marquee-dot">•</div>
                                    <div class="marquee-item"><span class="m-icon">💳</span> <strong>AXIS BANK Debit card:</strong> Get upto 20% off on flight booking</div>
                                    <div class="marquee-dot">•</div>
                                    <div class="marquee-item"><span class="m-icon">📱</span> <strong>MobiKwik:</strong> Get upto 10% cashback</div>
                                    <div class="marquee-dot">•</div>
                                    
                                    <!-- Duplicated for seamless loop -->
                                    <div class="marquee-item"><span class="m-icon">🏦</span> <strong>SBI Bank:</strong> Get upto 15% off on flight booking</div>
                                    <div class="marquee-dot">•</div>
                                    <div class="marquee-item"><span class="m-icon">💳</span> <strong>AXIS BANK Debit card:</strong> Get upto 20% off on flight booking</div>
                                    <div class="marquee-dot">•</div>
                                    <div class="marquee-item"><span class="m-icon">📱</span> <strong>MobiKwik:</strong> Get upto 10% cashback</div>
                                    <div class="marquee-dot">•</div>
                                </div>
                            </div>
"""

# Insert right before recent searches
html = html.replace('<!-- Recent Searches -->', marquee_html + '\n                            <!-- Recent Searches -->')

with open('index.html', 'w') as f:
    f.write(html)

# Now add CSS
with open('style.css', 'r') as f:
    css = f.read()

marquee_css = """
/* Bank Offers Marquee */
.offers-marquee-wrapper {
    overflow: hidden;
    width: 100%;
    padding: 10px 0;
    margin-top: 16px;
    background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(240, 244, 248, 0.6) 15%, rgba(240, 244, 248, 0.6) 85%, rgba(255,255,255,0) 100%);
    border-top: 1px dashed rgba(0, 95, 169, 0.1);
    border-bottom: 1px dashed rgba(0, 95, 169, 0.1);
    display: flex;
    white-space: nowrap;
    position: relative;
}

.offers-marquee-track {
    display: flex;
    align-items: center;
    gap: 16px;
    /* User asked for left to right movement */
    animation: marqueeLtoR 25s linear infinite;
    width: max-content;
}

@keyframes marqueeLtoR {
    0% { transform: translateX(-50%); }
    100% { transform: translateX(0%); }
}

.marquee-item {
    font-size: 11px;
    color: #5a6b82;
    display: flex;
    align-items: center;
    gap: 6px;
}

.marquee-item strong {
    color: var(--indigo-navy);
    font-weight: 700;
}

.marquee-dot {
    color: #cbd5e1;
    font-size: 8px;
}

.m-icon {
    font-size: 14px;
}
"""

css += marquee_css

with open('style.css', 'w') as f:
    f.write(css)

print("Marquee added!")
