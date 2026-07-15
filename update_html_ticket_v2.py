import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

track_start_marker = '<div class="bp-carousel-track" id="bpTrack">'
track_start = content.find(track_start_marker)

track_end_marker = '</div>\n                        \n                        \n                        <div class="bp-dots" id="bpDots">'
track_end = content.find(track_end_marker, track_start)

if track_start == -1 or track_end == -1:
    print("Could not find track markers")
    exit()

def get_slide(name, seat, seq, class_name):
    return f"""
                                <div class="bp-slide">
                                    <div class="bp-ticket-wrapper">
                                        <div class="bp-ticket-route-header">
                                            <div class="bp-ticket-city-col">
                                                <div class="city-name" id="tkCity1Name">LUCKNOW</div>
                                                <div class="city-code" id="tkCity1Code">LKO</div>
                                            </div>
                                            <div class="plane-icon">✈</div>
                                            <div class="bp-ticket-city-col right">
                                                <div class="city-name" id="tkCity2Name">NEW DELHI</div>
                                                <div class="city-code" id="tkCity2Code">DEL</div>
                                            </div>
                                        </div>
                                        <div class="bp-ticket-card">
                                            <div class="bp-ticket-top">
                                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                                                    <div>
                                                        <div class="bp-ticket-label">Passenger</div>
                                                        <div class="bp-ticket-value large">SHARMA / {name}</div>
                                                    </div>
                                                    <div class="bp-ticket-logo" style="text-align: right;">
                                                        <div style="font-weight: 800; font-size: 16px; font-style: italic; color: #001f54;">Skyline</div>
                                                    </div>
                                                </div>
                                                
                                                <div class="bp-ticket-grid-top" style="grid-template-columns: 1fr 1fr 1fr; gap: 16px;">
                                                    <div>
                                                        <div class="bp-ticket-label">Flight</div>
                                                        <div class="bp-ticket-value large" id="tkFlight">6E 2341</div>
                                                    </div>
                                                    <div>
                                                        <div class="bp-ticket-label">Seat</div>
                                                        <div class="bp-ticket-value large" id="tkSeat">{seat}</div>
                                                    </div>
                                                    <div>
                                                        <div class="bp-ticket-label">Class</div>
                                                        <div class="bp-ticket-value large" id="tkClass">{class_name}</div>
                                                    </div>
                                                    
                                                    <div>
                                                        <div class="bp-ticket-label">Boarding</div>
                                                        <div class="bp-ticket-value"><span class="time" id="tkBoardingTime">22:00</span></div>
                                                    </div>
                                                    <div>
                                                        <div class="bp-ticket-label">Gate / Door</div>
                                                        <div class="bp-ticket-value large" id="tkGate">5B / L1</div>
                                                    </div>
                                                    <div>
                                                        <div class="bp-ticket-label">Zone</div>
                                                        <div class="bp-ticket-value large" id="tkZone">02</div>
                                                    </div>
                                                    
                                                    <div>
                                                        <div class="bp-ticket-label">PNR</div>
                                                        <div class="bp-ticket-value">X3K9P2</div>
                                                    </div>
                                                    <div>
                                                        <div class="bp-ticket-label">Date</div>
                                                        <div class="bp-ticket-value" id="tkDate">25 MAR 2026</div>
                                                    </div>
                                                    <div>
                                                        <div class="bp-ticket-label">Seq</div>
                                                        <div class="bp-ticket-value" id="tkSeq">{seq}</div>
                                                    </div>
                                                </div>
                                            </div>
                                            
                                            <div class="bp-ticket-divider"></div>
                                            
                                            <div class="bp-ticket-bottom">
                                                <div class="bp-ticket-grid-bottom" style="display: flex; flex-direction: column; gap: 16px;">
                                                    <div>
                                                        <div class="bp-ticket-label">Baggage</div>
                                                        <div class="bp-ticket-value" style="font-size: 13px;" id="tkBaggage">15kg + 7kg cabin | 1 Piece</div>
                                                    </div>
                                                    <div>
                                                        <div class="bp-ticket-label">SSR</div>
                                                        <div class="bp-ticket-value" style="font-size: 13px;" id="tkSSR">WCHR, VGML</div>
                                                    </div>
                                                </div>
                                                <div class="bp-ticket-qr-block" onclick="openQRModal()" style="margin-left: 16px;">
                                                    <img src="qr_code.png" />
                                                </div>
                                            </div>
                                            <div class="bp-ticket-footer">
                                                Gate is subject to change. Boarding closes 25 min before departure.
                                            </div>
                                        </div>
                                        
                                        <div class="bp-leg-toggle multi-only" id="bpLegToggle" style="margin-top: 24px; display: flex; justify-content: center; gap: 16px;">
                                            <div class="bp-toggle-btn active" onclick="flipToLeg(1)" id="btnLeg1" style="color: white; border: 1px solid rgba(255,255,255,0.4); padding: 8px 16px; border-radius: 20px; font-size: 12px; font-weight: 600;">LKO ✈ DEL</div>
                                            <div class="bp-toggle-btn" onclick="flipToLeg(2)" id="btnLeg2" style="color: white; border: 1px solid rgba(255,255,255,0.4); padding: 8px 16px; border-radius: 20px; font-size: 12px; font-weight: 600;">DEL ✈ AMS</div>
                                        </div>
                                        
                                    </div>
                                </div>
    """

track_content = get_slide("RAVI", "12C", "001", "Economy (W)") + get_slide("ISHIKA", "12D", "002", "Economy (W)") + get_slide("ARYA", "12E", "003", "Economy (W)") + get_slide("ROHAN", "12F", "004", "Economy (W)")

content = content[:track_start + len(track_start_marker)] + "\n" + track_content + "                        " + content[track_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML Updated with new fields")
