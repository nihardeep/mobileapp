import re

# ==========================================
# 1. UPDATE INDEX.HTML
# ==========================================
with open('index.html', 'r') as f:
    html = f.read()

# Rebuild the loyalty section with BOTH cards
new_loyalty_html = """                            <!-- Loyalty Panel (IndiGo BluChip balance) -->
                            <div class="loyalty-section" id="loyaltySection">
                                
                                <!-- ========================================================= -->
                                <!-- STATE 1: LOYAL USER (Has Balance) -->
                                <!-- ========================================================= -->
                                <div class="bluchip-card" id="loyalUserCard" onclick="triggerHaptic('medium', 'Loyalty card clicked')">
                                    <div class="bluchip-top-row">
                                        <div class="bluchip-left-info">
                                            <span class="bluchip-title">IndiGo BluChip balance</span>
                                            <div class="bluchip-balance">
                                                <div class="bluchip-balance-reveal-wrapper">
                                                    <div class="bluchip-balance-text" id="bluchipBalanceText">
                                                        27,440 <span class="bluchip-sub-logo">Blu 3</span>
                                                    </div>
                                                    <div class="bluchip-plane-flyer" id="bluchipPlaneFlyer">
                                                        <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                                            <path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L14 19v-5.5l8 2.5z"/>
                                                        </svg>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="bluchip-right-info">
                                            <span class="bluchip-id">ID: 2582447 
                                                <span class="copy-icon" onclick="event.stopPropagation(); triggerHaptic('light', 'ID Copied'); alert('ID copied to clipboard!')">
                                                    <svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
                                                </span>
                                            </span>
                                            <span class="bluchip-action" onclick="event.stopPropagation(); triggerHaptic('light', 'Activity screen'); alert('Opening BluChip activity tracker...')">See Activity ➔</span>
                                        </div>
                                    </div>
                                    
                                    <div class="bluchip-divider"></div>
                                    
                                    <div class="bluchip-bottom-layout">
                                        <div class="partner-wallet-deck">
                                            <div class="partner-cards-container" id="partnerCardsContainer">
                                                <div class="partner-card card-cleartrip">
                                                    <div class="partner-logo-circle">
                                                        <svg viewBox="0 0 100 100" width="28" height="28">
                                                            <circle cx="50" cy="40" r="22" fill="#ff4f00" />
                                                            <path d="M40 40 l7 7 l14 -14" stroke="#ffffff" stroke-width="6" stroke-linecap="round" fill="none" />
                                                            <text x="50" y="82" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="12" font-weight="900" fill="#000000" text-anchor="middle">cleartrip</text>
                                                        </svg>
                                                    </div>
                                                </div>
                                                <div class="partner-card card-amazon">
                                                    <div class="partner-logo-circle">
                                                        <svg viewBox="0 0 100 100" width="28" height="28">
                                                            <text x="50" y="44" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="18" font-weight="900" fill="#000000" text-anchor="middle">amazon</text>
                                                            <path d="M25 54 Q50 72 75 54" stroke="#ff9900" stroke-width="7" fill="none" stroke-linecap="round" />
                                                            <path d="M70 51 l6 6 l-6 -1" fill="#ff9900" />
                                                        </svg>
                                                    </div>
                                                </div>
                                                <div class="partner-card card-sbi">
                                                    <div class="partner-logo-circle">
                                                        <svg viewBox="0 0 100 100" width="28" height="28">
                                                            <circle cx="50" cy="50" r="30" fill="#00a9e0" />
                                                            <circle cx="50" cy="50" r="10" fill="#ffffff" />
                                                            <rect x="46" y="50" width="8" height="30" fill="#ffffff" />
                                                        </svg>
                                                    </div>
                                                </div>
                                                <div class="partner-card card-reliance">
                                                    <div class="partner-logo-circle">
                                                        <svg viewBox="0 0 100 100" width="28" height="28">
                                                            <rect x="12" y="22" width="76" height="56" rx="6" fill="#0a2240" />
                                                            <text x="50" y="62" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="34" font-weight="900" fill="#ffffff" text-anchor="middle">R</text>
                                                        </svg>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        
                                        <div class="bluchip-rewards-info">
                                            <div class="rewards-title">Earn more with partners</div>
                                            <div class="rewards-subtitle" style="font-size: 10px; color: #b5c7ec; margin-top: 6px; line-height: 1.4;">
                                                ✦ You're 550 IndiGo BluChips away from a free flight to Goa!
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- ========================================================= -->
                                <!-- STATE 2: NEW USER (Zero Balance) -->
                                <!-- ========================================================= -->
                                <div class="bluchip-card" id="newUserCard" onclick="triggerHaptic('medium', 'Loyalty card clicked')" style="display: none;">
                                    <div class="bluchip-top-row">
                                        <div class="bluchip-left-info">
                                            <span class="bluchip-title">IndiGo BluChip balance</span>
                                            <div class="bluchip-balance">
                                                <div class="bluchip-balance-reveal-wrapper">
                                                    <div class="bluchip-balance-text">
                                                        0 <span class="bluchip-sub-logo">Blu 1</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="bluchip-right-info">
                                            <span class="bluchip-id" style="color: #60a5fa;">NEW MEMBER</span>
                                        </div>
                                    </div>
                                    
                                    <div class="bluchip-divider"></div>
                                    
                                    <div class="bluchip-bottom-layout">
                                        <div class="partner-wallet-deck">
                                            <div class="partner-cards-container">
                                                <div class="partner-card card-cleartrip" style="transform: translateY(0); filter: grayscale(100%); opacity: 0.5;">
                                                    <div class="partner-logo-circle"><svg viewBox="0 0 100 100" width="28" height="28"><circle cx="50" cy="40" r="22" fill="#ff4f00" /><path d="M40 40 l7 7 l14 -14" stroke="#ffffff" stroke-width="6" stroke-linecap="round" fill="none" /><text x="50" y="82" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="12" font-weight="900" fill="#000000" text-anchor="middle">cleartrip</text></svg></div>
                                                </div>
                                            </div>
                                        </div>
                                        
                                        <div class="zero-balance-flash-container">
                                            <div class="zero-flash-frame z-frame-1">
                                                <span class="z-icon">🎮</span> Play games to earn your first Points
                                            </div>
                                            <div class="zero-flash-frame z-frame-2">
                                                <span class="z-icon">✈️</span> Earn points from previous PNRs
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                            </div>"""

# Replace the existing loyalty section using exact string slices to avoid greedy regex
start_tag = '<!-- Loyalty Panel (IndiGo BluChip balance) -->'
end_tag = '<!-- Offers Carousel (Not business as usual slides) -->'
start_idx = html.find(start_tag)
end_idx = html.find(end_tag)

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_loyalty_html + "\n\n                            " + html[end_idx:]
    with open('index.html', 'w') as f:
        f.write(html)
    print("Injected Both Loyalty Cards Successfully!")
else:
    print(f"Error: Could not find tags. start={start_idx}, end={end_idx}")

EOF
