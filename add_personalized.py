import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Developer Toggle Button
dev_btn_html = """                    <button class="dev-trigger-btn" id="btnTogglePersonalized" onclick="togglePersonalizedBooking()">
                        🧑‍💼 Personalized Booking
                        <div class="dev-btn-indicator"></div>
                    </button>"""
# Add it right after the Student Persona button or Free Perks
if '<button class="dev-trigger-btn" id="btnToggleComplimentary" onclick="toggleComplimentaryPerks()">' in content:
    content = content.replace(
        '<button class="dev-trigger-btn" id="btnToggleComplimentary" onclick="toggleComplimentaryPerks()">',
        dev_btn_html + '\n                    <button class="dev-trigger-btn" id="btnToggleComplimentary" onclick="toggleComplimentaryPerks()">'
    )

# 2. Add Personalized Card
card_html = """                                    <!-- Nihar's Personalized Card -->
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
                                    </div>
"""
# Insert card into stack
if '<div class="boarding-passes-stack" id="boardingPassesStack">' in content:
    content = content.replace(
        '<div class="boarding-passes-stack" id="boardingPassesStack">',
        '<div class="boarding-passes-stack" id="boardingPassesStack">\n' + card_html
    )

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html")
