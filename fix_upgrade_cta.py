import re

# Update HTML
with open('index.html', 'r') as f:
    html = f.read()

new_card = """                            <div class="upgrade-promo-card subtle-glass" id="upgradePromoCard">
                                <div class="animated-text-container">
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
                                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px; color: var(--indigo-blue);">
                                            <path d="M19 18v2M5 18v2M4 6v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6M8 3h8a1 1 0 0 1 1 1v2H7V4a1 1 0 0 1 1-1z"/>
                                        </svg>
                                        <span>Front row seats</span>
                                    </div>
                                </div>
                                <button class="subtle-action-btn" onclick="triggerHaptic('medium', 'Upgrade'); this.style.transform='scale(0.95)'; setTimeout(()=>this.style.transform='scale(1)', 150); setTimeout(() => alert('Upgraded to Upfront!'), 200);" style="flex-shrink: 0; margin-left: 12px;">
                                    Upgrade ₹3499
                                </button>
                            </div>"""

start_idx = html.find('<div class="upgrade-promo-card subtle-glass" id="upgradePromoCard">')
end_idx = html.find('<!-- PNR Card Wrapper containing Route + Dynamic State Subcard -->')

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_card + "\n\n                            " + html[end_idx:]
    with open('index.html', 'w') as f:
        f.write(html)
    print("HTML updated")
else:
    print("Could not find section to replace")

# Update CSS
with open('style.css', 'r') as f:
    css = f.read()

# Remove old frame-3 styles which were justify-content: space-between
css = css.replace('.animated-benefit-frame.frame-3 {\n    animation-delay: 4s;\n    justify-content: space-between; /* Space out title and button */\n}', '.animated-benefit-frame.frame-3 {\n    animation-delay: 4s;\n}')

css_addition = """
.animated-text-container {
    position: relative;
    flex: 1;
    height: 24px;
    overflow: hidden;
}
.animated-benefit-frame {
    padding: 0;
}
"""

if ".animated-text-container" not in css:
    css += css_addition
    with open('style.css', 'w') as f:
        f.write(css)
    print("CSS updated")

