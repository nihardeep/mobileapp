def make_card(city_code, city_name, price, flight, bg_url):
    return f"""                                    <div class="boarding-pass-card" id="passCard{city_code}" onclick="expandBoardingPass('{city_code}')">
                                        <div class="pass-header">
                                            <div class="pass-header-top">
                                                <div class="pass-logo-area">
                                                    <span class="pass-indigo-logo">goIndiGo</span>
                                                    <span class="pass-title">INDIGO DEALS</span>
                                                </div>
                                                <div class="pass-price-summary">Fares from <span class="pass-min-price">₹{price}</span></div>
                                            </div>
                                            <div class="pass-route-row">
                                                <div class="pass-city">
                                                    <span class="pass-airport-code">DEL</span>
                                                    <span class="pass-airport-name">Delhi</span>
                                                </div>
                                                <div class="pass-plane-icon">
                                                    <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L14 19v-5.5l7 2.5z"/></svg>
                                                </div>
                                                <div class="pass-city align-right">
                                                    <span class="pass-airport-code">{city_code}</span>
                                                    <span class="pass-airport-name">{city_name}</span>
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
                                                    <span class="pass-detail-val">{flight}</span>
                                                </div>
                                                <div class="pass-detail-col">
                                                    <span class="pass-detail-label">CLASS</span>
                                                    <span class="pass-detail-val">ECONOMY</span>
                                                </div>
                                                <div class="pass-detail-col">
                                                    <span class="pass-detail-label">FARE TYPE</span>
                                                    <span class="pass-detail-val">BAG LITE</span>
                                                </div>
                                                <div class="pass-detail-col align-right">
                                                    <span class="pass-detail-label">GATE</span>
                                                    <span class="pass-detail-val">T3</span>
                                                </div>
                                            </div>
                                            <div class="pass-calendar-section">
                                                <div class="pass-calendar-title">SELECT FARE DATE</div>
                                                <div class="pass-calendar-chips" id="passCalendar{city_code}">
                                                    <!-- Populated dynamically -->
                                                </div>
                                            </div>
                                            <div class="pass-footer" style="display: flex; justify-content: space-between; align-items: center; padding: 12px 16px;">
                                                <div class="pass-view-more-stub" style="margin: 0; text-align: left; text-decoration: underline; font-weight: 700; color: rgba(255, 255, 255, 0.9); cursor: pointer;" onclick="event.stopPropagation(); triggerHaptic('light', 'View Details'); navigateTo('results')">
                                                    View details
                                                </div>
                                                <div class="pass-book-cta" onclick="event.stopPropagation(); triggerHaptic('medium', 'Book CTA'); navigateTo('passenger')" style="background: #ffd15c; color: #000; padding: 8px 16px; border-radius: 20px; font-weight: 800; font-size: 14px; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
                                                    Book at ₹{price}
                                                </div>
                                            </div>
                                        </div>
                                    </div>"""

cards = [
    make_card('HJR', 'Khajuraho', '2,499', '6E 404', ''),
    make_card('KNU', 'Kanpur', '2,999', '6E 712', ''),
    make_card('DHM', 'Dharamsala', '3,999', '6E 550', ''),
    make_card('IXC', 'Chandigarh', '3,199', '6E 998', '')
]

new_stack = f"""                                <div class="boarding-passes-stack" id="boardingPassesStack">
{cards[0]}
{cards[1]}
{cards[2]}
{cards[3]}
                                </div>"""

print(new_stack)
