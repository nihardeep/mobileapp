import re

with open('index.html', 'r') as f:
    html = f.read()

new_card = """                            <!-- Upfront Upgrade Suggestions Section -->
                            <div class="upgrade-promo-card premium-dark" id="upgradePromoCard">
                                <div class="shimmer-overlay"></div>
                                <div class="premium-header-row">
                                    <div class="premium-tag">
                                        <svg viewBox="0 0 24 24" width="10" height="10" fill="currentColor" style="margin-right: 4px; vertical-align: middle;">
                                            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                                        </svg>VIP UPGRADE
                                    </div>
                                    <div class="premium-price">₹3499</div>
                                </div>
                                <div class="premium-promo-title">IndiGo <span style="font-weight: 800; color: #fff;">Upfront</span></div>
                                <div class="premium-promo-subtitle">Skip the lines. Get front row seats & curated meals.</div>
                                <div class="premium-benefits-row">
                                    <span class="premium-benefit-tag">
                                        <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px; vertical-align: middle;">
                                            <path d="M19 18v2M5 18v2M4 6v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6M8 3h8a1 1 0 0 1 1 1v2H7V4a1 1 0 0 1 1-1z"/>
                                        </svg>Front Row
                                    </span>
                                    <span class="premium-benefit-tag">
                                        <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px; vertical-align: middle;">
                                            <path d="M17 8h2a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2h-2M3 8h14v7a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3V8zM6 2v3M10 2v3M14 2v3"/>
                                        </svg>Free Meals
                                    </span>
                                </div>
                                <button class="premium-action-btn" onclick="triggerHaptic('heavy', 'Upgrade Purchased'); this.style.transform='scale(0.96)'; setTimeout(()=>this.style.transform='scale(1)', 150); setTimeout(() => alert('Upgraded to Front Row Seat 3C! Seat updated.'), 200);">
                                    Unlock Upgrade
                                </button>
                            </div>"""

# Replace old upgrade-promo-card block
start_idx = html.find('<!-- Upfront Upgrade Suggestions Section -->')
end_idx = html.find('<!-- PNR Card Wrapper containing Route + Dynamic State Subcard -->')

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_card + "\n\n                            " + html[end_idx:]
    with open('index.html', 'w') as f:
        f.write(html)
    print("HTML updated")
else:
    print("Could not find section to replace")
