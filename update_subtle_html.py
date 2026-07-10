import re

with open('index.html', 'r') as f:
    html = f.read()

new_card = """                            <!-- Upfront Upgrade Suggestions Section -->
                            <div class="upgrade-promo-card subtle-glass" id="upgradePromoCard">
                                <div class="animated-benefit-frame frame-1">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" style="margin-right: 8px; color: var(--indigo-blue);">
                                        <path d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14V4zM6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zm2.46-7.12l1.41-1.41L12 12.59l2.12-2.12 1.41 1.41L13.41 14l2.12 2.12-1.41 1.41L12 15.41l-2.12 2.12-1.41-1.41L10.59 14l-2.13-2.12z"/>
                                    </svg>
                                    <span>Skip the airport queues</span>
                                </div>
                                <div class="animated-benefit-frame frame-2">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" style="margin-right: 8px; color: var(--indigo-blue);">
                                        <path d="M11 9H9V2H7v7H5V2H3v7c0 2.12 1.66 3.84 3.75 3.97V22h2.5v-9.03C11.34 12.84 13 11.12 13 9V2h-2v7zm5-3v8h2.5v8H21V2c-2.76 0-5 2.24-5 4z"/>
                                    </svg>
                                    <span>Curated in-flight meals</span>
                                </div>
                                <div class="animated-benefit-frame frame-3">
                                    <span class="subtle-promo-title">IndiGo <strong>Upfront</strong></span>
                                    <button class="subtle-action-btn" onclick="triggerHaptic('medium', 'Upgrade'); this.style.transform='scale(0.95)'; setTimeout(()=>this.style.transform='scale(1)', 150); setTimeout(() => alert('Upgraded to Upfront!'), 200);">
                                        Upgrade for ₹3499
                                    </button>
                                </div>
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
