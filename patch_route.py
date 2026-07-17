import re

# Patch index.html
with open('index.html', 'r') as f:
    html = f.read()

# Change PNR header route text
html = html.replace('<span class="pnr-route-txt">DEL - BOM</span>', '<span class="pnr-route-txt">LKO - LON (via DEL)</span>')

# Change route details
old_route = """                                <div class="pnr-route-details">
                                    <div class="pnr-route-point">
                                        <span class="pnr-time" id="routeDepTime">11:30</span>
                                        <span class="pnr-city-code">DEL <span class="terminal">T1</span></span>
                                        <span class="pnr-date">24 April</span>
                                    </div>
                                    <div class="pnr-route-line-box">
                                        <div class="pnr-arrow-line"></div>
                                        <span class="pnr-duration">2h 00m</span>
                                    </div>
                                    <div class="pnr-route-point right-aligned">
                                        <span class="pnr-time" id="routeArrTime">13:30</span>
                                        <span class="pnr-city-code">BOM <span class="terminal">T2</span></span>
                                        <span class="pnr-date">24 April</span>
                                    </div>
                                </div>"""

new_route = """                                <div class="pnr-route-details">
                                    <div class="pnr-route-point">
                                        <span class="pnr-time" id="routeDepTime">08:00</span>
                                        <span class="pnr-city-code">LKO <span class="terminal">T1</span></span>
                                        <span class="pnr-date">24 April</span>
                                    </div>
                                    <div class="pnr-route-line-box">
                                        <div class="pnr-arrow-line"></div>
                                        <span class="pnr-duration" style="color: var(--xairline-blue); font-weight: 700;">1 Stop (DEL)</span>
                                    </div>
                                    <div class="pnr-route-point right-aligned">
                                        <span class="pnr-time" id="routeArrTime">17:45</span>
                                        <span class="pnr-city-code">LON <span class="terminal">T3</span></span>
                                        <span class="pnr-date">24 April</span>
                                    </div>
                                </div>"""
html = html.replace(old_route, new_route)

with open('index.html', 'w') as f:
    f.write(html)

# Patch app.js
with open('app.js', 'r') as f:
    js = f.read()

# Connecting flight state text
js = js.replace("Layover in Mumbai", "Layover in Delhi")
js = js.replace("Your flight to Goa boards at Gate 22B.", "Your flight to London (LON) boards at Gate 22B.")
js = js.replace("Layover in BOM", "Layover in DEL")
js = js.replace("Next flight to GOI in 2h 15m", "Next flight to LON in 2h 15m")

# Missed flight state text
js = js.replace("You missed the boarding window for your flight to Mumbai.", "You missed the boarding window for your connecting flight to London.")

with open('app.js', 'w') as f:
    f.write(js)

print("Route updated to LKO-DEL-LON")
