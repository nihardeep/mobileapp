with open('index.html', 'r') as f:
    html = f.read()

# Locate the exact block to replace
start_str = '<div class="bluchip-bottom-layout" style="display: block; padding-top: 8px;">'
# The block ends right before the closing div of loyalUserCard, so we find loyalUserCard, then find its inner content.
# Since we know the layout is perfectly balanced now, we can just find the end of bluchip-bottom-layout safely.

start_idx = html.find(start_str)
# find the next "<!-- STATE 2: NEW USER (Zero Balance) -->"
end_idx_state2 = html.find('<!-- STATE 2: NEW USER (Zero Balance) -->')

# Let's extract the current loyalUserCard up to the end of bluchip-bottom-layout
block = html[start_idx:end_idx_state2]

# Actually, it's safer to just replace the inner contents of bluchip-bottom-layout
inner_start_idx = start_idx + len(start_str)
# Let's find the closing tag of bluchip-bottom-layout by counting divs
depth = 1
i = inner_start_idx
while depth > 0 and i < len(html):
    if html.startswith('<div', i):
        depth += 1
    elif html.startswith('</div', i):
        depth -= 1
    i += 1
    
end_of_bottom_layout = i - 6 # points to the '<' of '</div>'

old_inner = html[inner_start_idx:end_of_bottom_layout]

adani_logo = """
                                            <!-- Adani -->
                                            <div class="partner-box" style="flex: 0 0 auto; width: 110px; height: 60px; background: #000; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; display: flex; align-items: center; justify-content: center;" onclick="event.stopPropagation(); triggerHaptic('light', 'Partner clicked');">
                                                <span style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 24px; font-weight: 800; letter-spacing: -1px; background: linear-gradient(to right, #00A1E4, #9B51E0, #E1306C); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">adani</span>
                                            </div>"""

sbi_logo = """
                                            <!-- SBI Card -->
                                            <div class="partner-box" style="flex: 0 0 auto; width: 125px; height: 60px; background: #000; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; display: flex; align-items: center; justify-content: center;" onclick="event.stopPropagation(); triggerHaptic('light', 'Partner clicked');">
                                                <div style="display: flex; align-items: center; gap: 6px;">
                                                    <svg width="22" height="22" viewBox="0 0 100 100">
                                                        <circle cx="50" cy="50" r="48" fill="#00A1E4" />
                                                        <circle cx="50" cy="50" r="18" fill="#000" />
                                                        <rect x="42" y="50" width="16" height="35" fill="#000" />
                                                    </svg>
                                                    <span style="font-family: sans-serif; font-size: 16px; font-weight: 700;">
                                                        <span style="color: #fff; letter-spacing: -0.5px;">SBI</span> <span style="color: #00A1E4; font-weight: 400; letter-spacing: -0.5px;">card</span>
                                                    </span>
                                                </div>
                                            </div>"""

swiggy_logo = """
                                            <!-- Swiggy -->
                                            <div class="partner-box" style="flex: 0 0 auto; width: 100px; height: 60px; background: #000; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center;" onclick="event.stopPropagation(); triggerHaptic('light', 'Partner clicked');">
                                                <div style="background: #FC8019; width: 24px; height: 24px; border-radius: 6px; display: flex; align-items: center; justify-content: center; margin-bottom: 2px;">
                                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="#fff">
                                                        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm-1 9c-1.1 0-2-.9-2-2s.9-2 2-2h2c.55 0 1 .45 1 1v1c0 .55-.45 1-1 1h-1v1h2v1h-3z"/>
                                                    </svg>
                                                </div>
                                                <span style="color: #FC8019; font-weight: 700; font-size: 12px; letter-spacing: -0.5px;">Swiggy</span>
                                            </div>"""

kotak_logo = """
                                            <!-- Kotak -->
                                            <div class="partner-box" style="flex: 0 0 auto; width: 125px; height: 60px; background: #000; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center;" onclick="event.stopPropagation(); triggerHaptic('light', 'Partner clicked');">
                                                <div style="display: flex; align-items: center; gap: 4px; margin-bottom: 2px;">
                                                    <div style="width: 20px; height: 20px; background: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; position: relative;">
                                                         <svg width="14" height="8" viewBox="0 0 30 14" fill="none" stroke="#000" stroke-width="3">
                                                            <circle cx="8" cy="7" r="5" />
                                                            <circle cx="22" cy="7" r="5" />
                                                         </svg>
                                                         <div style="position: absolute; left: 8.5px; top: 6px; width: 2.5px; height: 10px; background: #000; transform: rotate(45deg);"></div>
                                                    </div>
                                                    <span style="color: #fff; font-weight: 700; font-size: 16px; letter-spacing: -0.5px;">kotak</span>
                                                </div>
                                                <span style="color: #ccc; font-size: 9px;">Kotak Mahindra B...</span>
                                            </div>"""

cards = sbi_logo + swiggy_logo + kotak_logo + adani_logo

new_inner = f"""
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                            <span style="font-size: 12px; font-weight: 500; color: #fff; letter-spacing: 0.5px; opacity: 0.9;">Earn more with our popular partners</span>
                                            <span style="font-size: 12px; font-weight: 600; color: #facc15; cursor: pointer;" onclick="event.stopPropagation(); alert('View all partners')">View more <svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-left: 2px;"><polyline points="9 18 15 12 9 6"></polyline></svg></span>
                                        </div>
                                        
                                        <div class="partner-stock-ticker-wrapper" style="background: transparent; border: none; padding: 0; margin-top: 0; position: relative;">
                                            <!-- Masking gradients to fade out left/right edges -->
                                            <div style="position: absolute; top: 0; left: 0; width: 24px; height: 100%; background: linear-gradient(to right, #0a0f18 0%, transparent 100%); z-index: 2; pointer-events: none;"></div>
                                            <div style="position: absolute; top: 0; right: 0; width: 24px; height: 100%; background: linear-gradient(to left, #0a0f18 0%, transparent 100%); z-index: 2; pointer-events: none;"></div>
                                            
                                            <div class="partner-stock-ticker-track" style="gap: 8px;">
                                                <!-- First Set -->
                                                {cards}
                                                <!-- Duplicate Set for infinite scroll -->
                                                {cards}
                                            </div>
                                        </div>
"""

# Let's count div balance of new_inner
def count_balance(s):
    return s.count('<div') - s.count('</div')

print(f"Old inner balance: {count_balance(old_inner)}")
print(f"New inner balance: {count_balance(new_inner)}")

if count_balance(old_inner) == count_balance(new_inner):
    final_html = html[:inner_start_idx] + new_inner + html[end_of_bottom_layout:]
    with open('index.html', 'w') as f:
        f.write(final_html)
    print("Replaced successfully!")
else:
    print("ERROR: Balances do not match! Aborting.")

