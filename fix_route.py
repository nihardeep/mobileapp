import re

# 1. Revert index.html to default DEL-BOM
with open('index.html', 'r') as f:
    html = f.read()

# Revert route text
html = html.replace('<span class="pnr-route-txt">LKO - LON (via DEL)</span>', '<span class="pnr-route-txt" id="dynamicPnrRouteTxt">DEL - BOM</span>')

old_route = """                                <div class="pnr-route-details" id="dynamicPnrRouteDetails">"""
if "id=\"dynamicPnrRouteDetails\"" not in html:
    html = html.replace('<div class="pnr-route-details">', '<div class="pnr-route-details" id="dynamicPnrRouteDetails">')

html_to_replace = """                                <div class="pnr-route-details" id="dynamicPnrRouteDetails">
                                    <div class="pnr-route-point">
                                        <span class="pnr-time" id="routeDepTime">08:00</span>
                                        <span class="pnr-city-code">LKO <span class="terminal">T1</span></span>
                                        <span class="pnr-date">24 April</span>
                                    </div>
                                    <div class="pnr-route-line-box">
                                        <div class="pnr-arrow-line"></div>
                                        <span class="pnr-duration"><span class="pnr-city-code" style="color: var(--xairline-blue);">DEL</span> <span style="font-size: 11px; font-weight: 600; color: #64748b;">(1 Stop)</span></span>
                                    </div>
                                    <div class="pnr-route-point right-aligned">
                                        <span class="pnr-time" id="routeArrTime">17:45</span>
                                        <span class="pnr-city-code">LON <span class="terminal">T3</span></span>
                                        <span class="pnr-date">24 April</span>
                                    </div>
                                </div>"""

default_route = """                                <div class="pnr-route-details" id="dynamicPnrRouteDetails">
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

html = html.replace(html_to_replace, default_route)

with open('index.html', 'w') as f:
    f.write(html)


# 2. Update app.js to swap dynamic route
with open('app.js', 'r') as f:
    js = f.read()

# Find renderFlightStateCard
inject_js = """function renderFlightStateCard(state) {
    const container = document.getElementById('companionSubcardContent');
    if (!container) return;
    
    // Dynamic Route Header Logic
    const routeTxt = document.getElementById('dynamicPnrRouteTxt');
    const routeDetails = document.getElementById('dynamicPnrRouteDetails');
    if (routeTxt && routeDetails) {
        if (state === 'connecting' || state === 'missed_flight') {
            routeTxt.innerHTML = 'LKO - LON (via DEL)';
            routeDetails.innerHTML = `
                <div class="pnr-route-point">
                    <span class="pnr-time" id="routeDepTime">08:00</span>
                    <span class="pnr-city-code">LKO <span class="terminal">T1</span></span>
                    <span class="pnr-date">24 April</span>
                </div>
                <div class="pnr-route-line-box">
                    <div class="pnr-arrow-line"></div>
                    <span class="pnr-duration"><span class="pnr-city-code" style="color: var(--xairline-blue);">DEL</span> <span style="font-size: 11px; font-weight: 600; color: #64748b;">(1 Stop)</span></span>
                </div>
                <div class="pnr-route-point right-aligned">
                    <span class="pnr-time" id="routeArrTime">17:45</span>
                    <span class="pnr-city-code">LON <span class="terminal">T3</span></span>
                    <span class="pnr-date">24 April</span>
                </div>
            `;
        } else {
            routeTxt.innerHTML = 'DEL - BOM';
            routeDetails.innerHTML = `
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
            `;
        }
    }
"""

js = js.replace("""function renderFlightStateCard(state) {
    const container = document.getElementById('companionSubcardContent');
    if (!container) return;""", inject_js)

with open('app.js', 'w') as f:
    f.write(js)

print("Dynamic route logic applied")
