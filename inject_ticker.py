import re

with open('index.html', 'r') as f:
    html = f.read()

# Define the new bottom layout for newUserCard
new_bottom_layout = """                                    <div class="bluchip-bottom-layout" style="flex-direction: column; gap: 12px; align-items: stretch; padding-top: 8px;">
                                        
                                        <!-- Top part: Centered Flashing texts -->
                                        <div class="zero-balance-flash-container" style="position: relative; height: 20px; width: 100%; display: flex; justify-content: center;">
                                            <div class="zero-flash-frame z-frame-1" style="justify-content: center;">
                                                <span class="z-icon">🎮</span> Play & Win: Earn your first 50 points
                                            </div>
                                            <div class="zero-flash-frame z-frame-2" style="justify-content: center;">
                                                <span class="z-icon">✈️</span> Claim Past Flights: Add old PNRs
                                            </div>
                                            <div class="zero-flash-frame z-frame-3" style="justify-content: center;">
                                                <span class="z-icon">🤝</span> Link Partners: Connect Flipkart
                                            </div>
                                            <div class="zero-flash-frame z-frame-4" style="justify-content: center;">
                                                <span class="z-icon">🛫</span> Book a Flight: Get 2x points today
                                            </div>
                                        </div>

                                        <!-- Bottom part: Stock Ticker Marquee -->
                                        <div class="partner-stock-ticker-wrapper">
                                            <div class="partner-stock-ticker-track">
                                                <!-- Duplicate content for seamless loop -->
                                                <div class="ticker-item"><span class="ticker-logo" style="background:#00a9e0; color:#fff;">S</span>SBI: Earn 5%</div>
                                                <div class="ticker-item"><span class="ticker-logo" style="background:#ff9900; color:#000;">a</span>Amazon: Earn 2%</div>
                                                <div class="ticker-item"><span class="ticker-logo" style="background:#861f41; color:#fff;">A</span>Axis: Earn 3%</div>
                                                <div class="ticker-item"><span class="ticker-logo" style="background:#0a2240; color:#fff;">R</span>Reliance: Earn 4%</div>
                                                
                                                <div class="ticker-item"><span class="ticker-logo" style="background:#00a9e0; color:#fff;">S</span>SBI: Earn 5%</div>
                                                <div class="ticker-item"><span class="ticker-logo" style="background:#ff9900; color:#000;">a</span>Amazon: Earn 2%</div>
                                                <div class="ticker-item"><span class="ticker-logo" style="background:#861f41; color:#fff;">A</span>Axis: Earn 3%</div>
                                                <div class="ticker-item"><span class="ticker-logo" style="background:#0a2240; color:#fff;">R</span>Reliance: Earn 4%</div>
                                            </div>
                                        </div>
                                    </div>"""

# Find the start and end of the newUserCard's bottom layout
# Let's replace the whole bluchip-bottom-layout block inside newUserCard
start_str = '                                    <div class="bluchip-bottom-layout">'

parts = html.split('<div class="bluchip-card" id="newUserCard"')
if len(parts) == 2:
    new_user_section = parts[1]
    
    start_idx = new_user_section.find(start_str)
    end_idx = new_user_section.find('                                </div>\n                                \n                            </div>', start_idx)
    
    if start_idx != -1 and end_idx != -1:
        updated_new_user = new_user_section[:start_idx] + new_bottom_layout + '\n' + new_user_section[end_idx:]
        html = parts[0] + '<div class="bluchip-card" id="newUserCard"' + updated_new_user
        
        with open('index.html', 'w') as f:
            f.write(html)
        print("Successfully injected stock ticker HTML.")
    else:
        print("Could not find bottom layout bounds.")
else:
    print("Could not split by newUserCard.")


# 2. Append CSS for the ticker
with open('style.css', 'r') as f:
    css = f.read()

ticker_css = """
/* ==========================================================================
   PARTNER STOCK TICKER
   ========================================================================== */
.partner-stock-ticker-wrapper {
    width: 100%;
    overflow: hidden;
    position: relative;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 6px;
    padding: 6px 0;
    margin-top: 4px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

/* Gradient fades on the edges for a smooth entrance/exit */
.partner-stock-ticker-wrapper::before,
.partner-stock-ticker-wrapper::after {
    content: '';
    position: absolute;
    top: 0;
    width: 20px;
    height: 100%;
    z-index: 2;
}
.partner-stock-ticker-wrapper::before {
    left: 0;
    background: linear-gradient(to right, #0c0f12 0%, transparent 100%);
}
.partner-stock-ticker-wrapper::after {
    right: 0;
    background: linear-gradient(to left, #0c0f12 0%, transparent 100%);
}

.partner-stock-ticker-track {
    display: flex;
    white-space: nowrap;
    animation: tickerScroll 15s linear infinite;
    width: fit-content;
}

.ticker-item {
    display: flex;
    align-items: center;
    font-size: 11px;
    font-weight: 600;
    color: #a0aec0;
    padding: 0 16px;
}

.ticker-logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    font-size: 9px;
    font-weight: 900;
    margin-right: 6px;
}

@keyframes tickerScroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
"""

if "PARTNER STOCK TICKER" not in css:
    css += ticker_css
    with open('style.css', 'w') as f:
        f.write(css)
    print("Successfully added stock ticker CSS.")
else:
    print("Stock ticker CSS already exists.")
