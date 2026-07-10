import re

with open('index.html.bak', 'r') as f:
    html = f.read()

# 1. Apply replace_globe.py
with open('world_map.svg', 'r') as f:
    svg_content = f.read()

# Add styling directly to SVG
svg_content = svg_content.replace('<svg ', '<svg style="width: 100%; height: 100%; opacity: 0.8; transform: scale(1.1);" ')
svg_content = svg_content.replace('path {', 'path { fill: #ffffff; stroke: #005FA9; stroke-width: 0.5px; opacity: 0.6;')

new_map_html = f"""
                        <div class="flat-map-wrapper" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: #ffffff;">
                            {svg_content}
                        </div>
"""

# Extract globe sphere wrapper and replace
globe_regex = r'(<div class="globe-sphere-wrapper">.*?</div>\s*</div>\s*</div>\s*</div>)'
match = re.search(globe_regex, html, re.DOTALL)
if match:
    html = html.replace(match.group(0), new_map_html)


# 2. Apply premium_banner.py
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

# 3. Apply add_marquee.py
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
html = html.replace('<!-- Recent Searches -->', marquee_html + '\n                            <!-- Recent Searches -->')

with open('index.html', 'w') as f:
    f.write(html)

print("Restored index.html from backup and re-applied all safe modifications!")
