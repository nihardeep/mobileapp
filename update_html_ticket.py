import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update screenTrips background
old_screen_style = 'id="screenTrips" style="background: #f4f6f8; overflow-y: auto; overflow-x: hidden;"'
new_screen_style = 'id="screenTrips" style="background: #041029 url(\'world_map_texture.png\') top center no-repeat; background-size: cover; overflow-y: auto; overflow-x: hidden;"'
content = content.replace(old_screen_style, new_screen_style)

# 2. Extract track section and replace it
track_start_marker = '<div class="bp-carousel-track" id="bpTrack">'
track_start = content.find(track_start_marker)

track_end_marker = '</div>\n                        \n                        \n                        <div class="bp-dots" id="bpDots">'
track_end = content.find(track_end_marker, track_start)

if track_start == -1 or track_end == -1:
    print("Could not find track markers")
    exit()

def get_slide(name, seat):
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
                                                <div class="bp-ticket-grid-top">
                                                    <div>
                                                        <div class="bp-ticket-label">Flight</div>
                                                        <div class="bp-ticket-value large" id="tkFlight">6E 2341</div>
                                                    </div>
                                                    <div class="bp-ticket-logo" style="text-align: right;">
                                                        <div style="font-weight: 800; font-size: 14px; font-style: italic; color: #001f54;">Skyline</div>
                                                    </div>
                                                </div>
                                                <div class="bp-ticket-grid-top">
                                                    <div>
                                                        <div class="bp-ticket-label">Passenger</div>
                                                        <div class="bp-ticket-value">SHARMA / {name}</div>
                                                    </div>
                                                    <div style="text-align: right;">
                                                        <div class="bp-ticket-label">Seat</div>
                                                        <div class="bp-ticket-value large" id="tkSeat">{seat}</div>
                                                    </div>
                                                </div>
                                                <div class="bp-ticket-grid-top">
                                                    <div>
                                                        <div class="bp-ticket-label">Boarding</div>
                                                        <div class="bp-ticket-value">
                                                            <span class="time" id="tkBoardingTime">22:00</span> <span class="sub">(IST)</span>
                                                            <span class="date-sub" id="tkBoardingDate">25 Mar 2026</span>
                                                        </div>
                                                    </div>
                                                    <div style="text-align: right;">
                                                        <div class="bp-ticket-label">Arrives</div>
                                                        <div class="bp-ticket-value">
                                                            <span class="time" id="tkArrivesTime">23:25</span> <span class="sub">(IST)</span>
                                                            <span class="date-sub" id="tkArrivesDate">25 Mar 2026</span>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            
                                            <div class="bp-ticket-divider"></div>
                                            
                                            <div class="bp-ticket-bottom">
                                                <div class="bp-ticket-grid-bottom">
                                                    <div>
                                                        <div class="bp-ticket-label">Gate</div>
                                                        <div class="bp-ticket-value large" id="tkGate">5B</div>
                                                    </div>
                                                    <div>
                                                        <div class="bp-ticket-label">Date</div>
                                                        <div class="bp-ticket-value" id="tkDate">25 Mar 2026</div>
                                                    </div>
                                                    <div>
                                                        <div class="bp-ticket-label">Terminal</div>
                                                        <div class="bp-ticket-value" id="tkTerminal">T2</div>
                                                    </div>
                                                    <div>
                                                        <div class="bp-ticket-label">Aircraft</div>
                                                        <div class="bp-ticket-value" id="tkAircraft">A320neo</div>
                                                    </div>
                                                </div>
                                                <div class="bp-ticket-qr-block" onclick="openQRModal()">
                                                    <img src="qr_code.png" />
                                                </div>
                                            </div>
                                            <div class="bp-ticket-footer">
                                                Gates closes 25 minutes before departure
                                            </div>
                                        </div>
                                        
                                        <div class="bp-leg-toggle multi-only" id="bpLegToggle" style="margin-top: 24px; background: rgba(255,255,255,0.1);">
                                            <div class="bp-toggle-btn active" onclick="flipToLeg(1)" id="btnLeg1" style="color: white;">LKO ✈ DEL</div>
                                            <div class="bp-toggle-btn" onclick="flipToLeg(2)" id="btnLeg2" style="color: white;">DEL ✈ AMS</div>
                                        </div>
                                        
                                    </div>
                                </div>
    """

track_content = get_slide("RAVI", "12C") + get_slide("ISHIKA", "12D") + get_slide("ARYA", "12E") + get_slide("ROHAN", "12F")

content = content[:track_start + len(track_start_marker)] + "\n" + track_content + "                        " + content[track_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML Updated")
