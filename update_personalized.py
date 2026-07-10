import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_card = """                                    <!-- Nihar's Personalized Card -->
                                    <div class="boarding-pass-card" id="passCardPersonalized" onclick="expandBoardingPass('Personalized')" style="display: none; border: 2px solid #005fa9; box-shadow: 0 0 20px rgba(0, 95, 169, 0.4);">
                                        <div class="pass-header" style="background: linear-gradient(135deg, #001f54 0%, #005fa9 100%);">
                                            <div class="pass-header-top">
                                                <div class="pass-logo-area">
                                                    <span class="pass-indigo-logo" style="color: #fff;">goIndiGo</span>
                                                    <span class="pass-title" style="color: #f59e0b; font-weight: 900;">NIHAR'S USUAL</span>
                                                </div>
                                                <div class="pass-price-summary" style="color: #fff;">Fares from <span class="pass-min-price" style="color: #fff;">₹4,999</span></div>
                                            </div>
                                            <div class="pass-route-row" style="color: #fff;">
                                                <div class="pass-city">
                                                    <span class="pass-airport-code" style="color: #fff;">DEL</span>
                                                    <span class="pass-airport-name" style="color: rgba(255,255,255,0.8);">Delhi</span>
                                                </div>
                                                <div class="pass-plane-icon">
                                                    <svg viewBox="0 0 24 24" width="14" height="14" fill="#f59e0b"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L14 19v-5.5l7 2.5z"/></svg>
                                                </div>
                                                <div class="pass-city align-right">
                                                    <span class="pass-airport-code" style="color: #fff;">BOM</span>
                                                    <span class="pass-airport-name" style="color: rgba(255,255,255,0.8);">Mumbai</span>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="pass-body">
                                            <div class="pass-divider">
                                                <div class="pass-notch notch-left"></div>
                                                <div class="pass-dashed-line"></div>
                                                <div class="pass-notch notch-right"></div>
                                            </div>
                                            <div class="pass-details-grid">
                                                <div class="pass-detail-col">
                                                    <span class="pass-detail-label">FLIGHT</span>
                                                    <span class="pass-detail-val">6E 2015</span>
                                                </div>
                                                <div class="pass-detail-col">
                                                    <span class="pass-detail-label">CLASS</span>
                                                    <span class="pass-detail-val">STRETCH</span>
                                                </div>
                                                <div class="pass-detail-col">
                                                    <span class="pass-detail-label">SEAT</span>
                                                    <span class="pass-detail-val">12A</span>
                                                </div>
                                                <div class="pass-detail-col align-right">
                                                    <span class="pass-detail-label">MEAL</span>
                                                    <span class="pass-detail-val">Veg Club</span>
                                                </div>
                                            </div>
                                            
                                            <!-- Rewards & Savings Banner -->
                                            <div style="margin: 12px 16px; background: rgba(0, 95, 169, 0.05); border-radius: 12px; padding: 10px; display: flex; flex-direction: column; gap: 6px; border: 1px solid rgba(0, 95, 169, 0.1);">
                                                <div style="display: flex; align-items: center; justify-content: space-between;">
                                                    <div style="display: flex; align-items: center; gap: 6px;">
                                                        <span style="background: #005fa9; color: #fff; padding: 2px 6px; border-radius: 6px; font-size: 10px; font-weight: 800;">BLUCHIP</span>
                                                        <span style="font-size: 12px; font-weight: 700; color: #001f54;">Earns 500 Points</span>
                                                    </div>
                                                </div>
                                                <div style="font-size: 11px; font-weight: 600; color: #16a34a; background: #dcfce7; padding: 4px 8px; border-radius: 6px; display: inline-flex; align-items: center; gap: 4px; width: fit-content;">
                                                    <span>💰</span> You save ₹500 on your usual add-ons!
                                                </div>
                                            </div>

                                            <div class="pass-calendar-section">
                                                <div class="pass-calendar-title">SELECT FARE DATE</div>
                                                <div class="pass-calendar-chips" id="passCalendarPersonalized">
                                                    <!-- Populated dynamically or static for this mock -->
                                                    <div class="calendar-chip">
                                                        <div class="cal-date">23 Apr</div>
                                                        <div class="cal-price">₹5,499</div>
                                                    </div>
                                                    <div class="calendar-chip active">
                                                        <div class="cal-date">24 Apr</div>
                                                        <div class="cal-price">₹4,999</div>
                                                    </div>
                                                    <div class="calendar-chip">
                                                        <div class="cal-date">25 Apr</div>
                                                        <div class="cal-price">₹5,299</div>
                                                    </div>
                                                    <div class="calendar-chip">
                                                        <div class="cal-date">26 Apr</div>
                                                        <div class="cal-price">₹6,199</div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="pass-footer" style="display: flex; justify-content: space-between; align-items: center; padding: 12px 16px;">
                                                <div class="pass-view-more-stub" style="margin: 0; text-align: left; text-decoration: underline; font-weight: 700; color: #005fa9; cursor: pointer;" onclick="event.stopPropagation(); triggerHaptic('light', 'View Details'); navigateTo('results')">
                                                    View details
                                                </div>
                                                <div class="pass-book-cta" onclick="event.stopPropagation(); triggerHaptic('medium', 'Book CTA'); navigateTo('passenger')" style="background: #005fa9; color: #fff; padding: 8px 16px; border-radius: 20px; font-weight: 800; font-size: 14px; cursor: pointer; box-shadow: 0 4px 10px rgba(0, 95, 169, 0.3);">
                                                    Book at ₹4,999
                                                </div>
                                            </div>
                                        </div>
                                    </div>"""


new_card = """                                    <!-- Nihar's Personalized Card (Premium Redesign) -->
                                    <div class="boarding-pass-card" id="passCardPersonalized" onclick="expandBoardingPass('Personalized')" style="display: none; border: 1px solid rgba(245, 158, 11, 0.4); box-shadow: 0 12px 32px rgba(30, 27, 75, 0.25);">
                                        <div class="pass-header" style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);">
                                            <div class="pass-header-top">
                                                <div class="pass-logo-area">
                                                    <span class="pass-indigo-logo" style="color: #fff;">goIndiGo</span>
                                                    <span class="pass-title" style="color: #fff; background: rgba(245, 158, 11, 0.2); padding: 2px 8px; border-radius: 12px; border: 1px solid rgba(245, 158, 11, 0.4); font-weight: 800; font-size: 11px;">NIHAR'S USUAL</span>
                                                </div>
                                                <div class="pass-price-summary" style="color: rgba(255,255,255,0.8);">Fares from <span class="pass-min-price" style="color: #fcd34d;">₹4,999</span></div>
                                            </div>
                                            <div class="pass-route-row" style="color: #fff;">
                                                <div class="pass-city">
                                                    <span class="pass-airport-code" style="color: #fff;">DEL</span>
                                                    <span class="pass-airport-name" style="color: rgba(255,255,255,0.7);">Delhi</span>
                                                </div>
                                                <div class="pass-plane-icon">
                                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="#fcd34d" style="filter: drop-shadow(0 0 4px rgba(252, 211, 77, 0.6));"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L14 19v-5.5l7 2.5z"/></svg>
                                                </div>
                                                <div class="pass-city align-right">
                                                    <span class="pass-airport-code" style="color: #fff;">BOM</span>
                                                    <span class="pass-airport-name" style="color: rgba(255,255,255,0.7);">Mumbai</span>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="pass-body">
                                            <div class="pass-divider">
                                                <div class="pass-notch notch-left"></div>
                                                <div class="pass-dashed-line"></div>
                                                <div class="pass-notch notch-right"></div>
                                            </div>
                                            <div class="pass-details-grid">
                                                <div class="pass-detail-col">
                                                    <span class="pass-detail-label">FLIGHT</span>
                                                    <span class="pass-detail-val">6E 2015</span>
                                                </div>
                                                <div class="pass-detail-col">
                                                    <span class="pass-detail-label">CLASS</span>
                                                    <span class="pass-detail-val" style="color: #005fa9;">STRETCH</span>
                                                </div>
                                                <div class="pass-detail-col">
                                                    <span class="pass-detail-label">SEAT</span>
                                                    <span class="pass-detail-val">12A</span>
                                                </div>
                                                <div class="pass-detail-col align-right">
                                                    <span class="pass-detail-label">MEAL</span>
                                                    <span class="pass-detail-val">Veg Club</span>
                                                </div>
                                            </div>
                                            
                                            <!-- Rewards & Savings Banner (Premium Glassmorphic) -->
                                            <div style="margin: 12px 16px; background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(245, 158, 11, 0.02) 100%); border-radius: 12px; padding: 12px; display: flex; flex-direction: column; gap: 8px; border: 1px solid rgba(245, 158, 11, 0.3); position: relative; overflow: hidden; box-shadow: inset 0 2px 10px rgba(255,255,255,0.5);">
                                                <div style="position: absolute; top: -20px; right: -20px; width: 80px; height: 80px; background: rgba(245, 158, 11, 0.15); filter: blur(24px); border-radius: 50%;"></div>
                                                <div style="display: flex; align-items: center; justify-content: space-between; z-index: 1;">
                                                    <div style="display: flex; align-items: center; gap: 8px;">
                                                        <span style="background: linear-gradient(135deg, #f59e0b, #d97706); color: #fff; padding: 3px 8px; border-radius: 6px; font-size: 10px; font-weight: 900; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(245, 158, 11, 0.4);">BLUCHIP</span>
                                                        <span style="font-size: 13px; font-weight: 800; color: #78350f;">Earns 500 Points</span>
                                                    </div>
                                                </div>
                                                <div style="font-size: 12px; font-weight: 700; color: #047857; display: flex; align-items: center; gap: 6px; z-index: 1;">
                                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1.41 16.09V20h-2.67v-1.93c-1.71-.36-3.16-1.46-3.27-3.4h1.96c.1 1.05.82 1.87 2.65 1.87 1.96 0 2.4-.98 2.4-1.59 0-.83-.44-1.61-2.67-2.14-2.48-.6-4.18-1.62-4.18-3.67 0-1.72 1.43-2.81 3.11-3.14V3.9h2.67v1.95c1.28.32 2.64 1.34 2.87 3.03h-1.95c-.2-1.04-.99-1.64-2.25-1.64-1.55 0-2.11.85-2.11 1.49 0 .91.56 1.45 2.83 2.01 2.8.68 4.02 1.87 4.02 3.73 0 2.06-1.56 3.06-3.41 3.42z"/></svg>
                                                    You save ₹500 on your usual add-ons!
                                                </div>
                                            </div>

                                            <div class="pass-calendar-section">
                                                <div class="pass-calendar-title">SELECT FARE DATE</div>
                                                <!-- Correct pass-chip structure for calendar -->
                                                <div class="pass-calendar-chips" id="passCalendarPersonalized">
                                                    <div class="pass-chip">
                                                        <span class="pass-chip-date">23 Apr</span>
                                                        <span class="pass-chip-price-strikethrough">₹5,999</span>
                                                        <span class="pass-chip-price">₹5,499</span>
                                                    </div>
                                                    <div class="pass-chip selected-fare lowest-fare">
                                                        <span class="pass-chip-date">24 Apr</span>
                                                        <span class="pass-chip-price-strikethrough">₹5,499</span>
                                                        <span class="pass-chip-price">₹4,999</span>
                                                    </div>
                                                    <div class="pass-chip">
                                                        <span class="pass-chip-date">25 Apr</span>
                                                        <span class="pass-chip-price-strikethrough">₹5,799</span>
                                                        <span class="pass-chip-price">₹5,299</span>
                                                    </div>
                                                    <div class="pass-chip">
                                                        <span class="pass-chip-date">26 Apr</span>
                                                        <span class="pass-chip-price-strikethrough">₹6,699</span>
                                                        <span class="pass-chip-price">₹6,199</span>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="pass-footer" style="display: flex; justify-content: space-between; align-items: center; padding: 12px 16px;">
                                                <div class="pass-view-more-stub" style="margin: 0; text-align: left; text-decoration: underline; font-weight: 700; color: #0f172a; cursor: pointer;" onclick="event.stopPropagation(); triggerHaptic('light', 'View Details'); navigateTo('results')">
                                                    View details
                                                </div>
                                                <div class="pass-book-cta" onclick="event.stopPropagation(); triggerHaptic('medium', 'Book CTA'); navigateTo('passenger')" style="background: linear-gradient(135deg, #fde047 0%, #f59e0b 100%); color: #451a03; padding: 10px 24px; border-radius: 24px; font-weight: 900; font-size: 15px; cursor: pointer; box-shadow: 0 6px 16px rgba(245, 158, 11, 0.4);">
                                                    Book at ₹4,999
                                                </div>
                                            </div>
                                        </div>
                                    </div>"""

if old_card in content:
    content = content.replace(old_card, new_card)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated successfully.")
else:
    print("Could not find the old card exactly.")
