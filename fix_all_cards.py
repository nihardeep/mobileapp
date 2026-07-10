with open('index.html', 'r') as f:
    html = f.read()

start_idx = html.find('<div class="bluchip-card" id="loyalUserCard"')
end_idx = html.find('<!-- Offers Carousel (Not business as usual slides) -->')

new_cards = """<div class="bluchip-card" id="loyalUserCard" onclick="triggerHaptic('medium', 'Loyalty card clicked')">
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

                                    <div class="bluchip-bottom-layout" style="display: block; padding-top: 8px;">
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                            <span style="font-size: 12px; font-weight: 500; color: #fff; letter-spacing: 0.5px; opacity: 0.9;">Earn more with our popular partners</span>
                                            <span style="font-size: 12px; font-weight: 600; color: #facc15; cursor: pointer;" onclick="event.stopPropagation(); alert('View all partners')">View more <svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-left: 2px;"><polyline points="9 18 15 12 9 6"></polyline></svg></span>
                                        </div>
                                        
                                        <div class="partners-scroll-track" style="display: flex; overflow-x: auto; gap: 8px; padding-bottom: 4px; scroll-snap-type: x mandatory; -webkit-overflow-scrolling: touch;">
                                            
                                            <!-- SBI Card -->
                                            <div class="partner-box" style="flex: 0 0 auto; width: 110px; height: 50px; background: #000; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; display: flex; align-items: center; justify-content: center; scroll-snap-align: start;" onclick="event.stopPropagation(); triggerHaptic('light', 'Partner clicked');">
                                                <div style="display: flex; align-items: center; gap: 4px;">
                                                    <svg width="18" height="18" viewBox="0 0 100 100">
                                                        <circle cx="50" cy="50" r="48" fill="#00A1E4" />
                                                        <circle cx="50" cy="50" r="18" fill="#000" />
                                                        <rect x="42" y="50" width="16" height="35" fill="#000" />
                                                    </svg>
                                                    <span style="font-family: sans-serif; font-size: 14px; font-weight: 700;">
                                                        <span style="color: #fff; letter-spacing: -0.5px;">SBI</span> <span style="color: #00A1E4; font-weight: 400; letter-spacing: -0.5px;">card</span>
                                                    </span>
                                                </div>
                                            </div>

                                            <!-- Swiggy -->
                                            <div class="partner-box" style="flex: 0 0 auto; width: 90px; height: 50px; background: #000; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; display: flex; flex-direction: column; align-items: center; justify-content: center; scroll-snap-align: start;" onclick="event.stopPropagation(); triggerHaptic('light', 'Partner clicked');">
                                                <div style="background: #FC8019; width: 22px; height: 22px; border-radius: 6px; display: flex; align-items: center; justify-content: center; margin-bottom: 2px;">
                                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="#fff">
                                                        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm-1 9c-1.1 0-2-.9-2-2s.9-2 2-2h2c.55 0 1 .45 1 1v1c0 .55-.45 1-1 1h-1v1h2v1h-3z"/>
                                                    </svg>
                                                </div>
                                                <span style="color: #FC8019; font-weight: 700; font-size: 11px; letter-spacing: -0.5px;">Swiggy</span>
                                            </div>

                                            <!-- Kotak -->
                                            <div class="partner-box" style="flex: 0 0 auto; width: 110px; height: 50px; background: #000; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; display: flex; flex-direction: column; align-items: center; justify-content: center; scroll-snap-align: start;" onclick="event.stopPropagation(); triggerHaptic('light', 'Partner clicked');">
                                                <div style="display: flex; align-items: center; gap: 4px; margin-bottom: 1px;">
                                                    <div style="width: 18px; height: 18px; background: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; position: relative;">
                                                         <svg width="14" height="8" viewBox="0 0 30 14" fill="none" stroke="#000" stroke-width="3">
                                                            <circle cx="8" cy="7" r="5" />
                                                            <circle cx="22" cy="7" r="5" />
                                                         </svg>
                                                         <div style="position: absolute; left: 7px; top: 5px; width: 2px; height: 9px; background: #000; transform: rotate(45deg);"></div>
                                                    </div>
                                                    <span style="color: #fff; font-weight: 700; font-size: 14px; letter-spacing: -0.5px;">kotak</span>
                                                </div>
                                                <span style="color: #ccc; font-size: 8px;">Kotak Mahindra B...</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- STATE 2: NEW USER (Zero Balance) -->
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

                                    <div class="bluchip-bottom-layout" style="flex-direction: column; gap: 12px; align-items: stretch; padding-top: 8px;">
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

                                        <div class="partner-stock-ticker-wrapper">
                                            <div class="partner-stock-ticker-track">
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
                                    </div>
                                </div>
                            </div>
                            
                            """
new_html = html[:start_idx] + new_cards + html[end_idx:]
with open('index.html', 'w') as f:
    f.write(new_html)
