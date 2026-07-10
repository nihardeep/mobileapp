import re
import random

with open('index.html', 'r') as f:
    html = f.read()

# Define the flight data
flights = [
    {"id": "6E 1234", "from": "DEL", "to": "BOM", "dTime": "05:15", "aTime": "07:30", "dur": "2h 15m", "stops": "Non-stop", "stopsColor": "#10b981", "oldP": "4,800", "newP": "4,320"},
    {"id": "6E 5678", "from": "DEL", "to": "BOM", "dTime": "06:30", "aTime": "10:45", "dur": "4h 15m", "stops": "1 Stop", "stopsColor": "var(--indigo-blue)", "oldP": "5,500", "newP": "4,950"},
    {"id": "6E 2341", "from": "DEL", "to": "BOM", "dTime": "08:00", "aTime": "10:10", "dur": "2h 10m", "stops": "Non-stop", "stopsColor": "#10b981", "oldP": "4,200", "newP": "3,780"},
    {"id": "6E 7890", "from": "DEL", "to": "BOM", "dTime": "11:45", "aTime": "14:00", "dur": "2h 15m", "stops": "Non-stop", "stopsColor": "#10b981", "oldP": "5,100", "newP": "4,590"},
    {"id": "6E 3456", "from": "DEL", "to": "BOM", "dTime": "13:20", "aTime": "15:35", "dur": "2h 15m", "stops": "Non-stop", "stopsColor": "#10b981", "oldP": "4,900", "newP": "4,410"},
    {"id": "6E 8901", "from": "DEL", "to": "BOM", "dTime": "15:00", "aTime": "20:30", "dur": "5h 30m", "stops": "1 Stop", "stopsColor": "var(--indigo-blue)", "oldP": "6,200", "newP": "5,580"},
    {"id": "6E 4567", "from": "DEL", "to": "BOM", "dTime": "16:45", "aTime": "18:55", "dur": "2h 10m", "stops": "Non-stop", "stopsColor": "#10b981", "oldP": "4,500", "newP": "4,050"},
    {"id": "6E 9012", "from": "DEL", "to": "BOM", "dTime": "18:30", "aTime": "20:45", "dur": "2h 15m", "stops": "Non-stop", "stopsColor": "#10b981", "oldP": "5,800", "newP": "5,220"},
    {"id": "6E 5678", "from": "DEL", "to": "BOM", "dTime": "20:15", "aTime": "22:20", "dur": "2h 05m", "stops": "Non-stop", "stopsColor": "#10b981", "oldP": "4,100", "newP": "3,690"},
    {"id": "6E 1122", "from": "DEL", "to": "BOM", "dTime": "22:00", "aTime": "00:15", "dur": "2h 15m", "stops": "Non-stop", "stopsColor": "#10b981", "oldP": "3,900", "newP": "3,510"}
]

cards_html = ""
for i, f in enumerate(flights):
    cards_html += f"""
                            <!-- Sample Card {i+1} -->
                            <div class="flight-card" onclick="activateStudentModeAndSearch()" style="margin-bottom: 12px; cursor: pointer; position: relative;">
                                <div class="student-edge-badge">✨ Free Change • 🧳 15Kg Extra</div>
                                <div class="fc-header">
                                    <span>{f['id']}</span>
                                    <span style="color: var(--indigo-blue); background: rgba(0, 95, 169, 0.05); padding: 2px 6px; border-radius: 4px;">Earn up to 400 BluChips</span>
                                </div>
                                <div class="fc-times-row">
                                    <div class="fc-time-block">
                                        <div class="fc-time">{f['dTime']}</div>
                                        <div class="fc-code">{f['from']}, T1</div>
                                    </div>
                                    <div class="fc-duration">
                                        <span class="fc-dur-text">{f['dur']}</span>
                                        <div class="fc-dur-line"></div>
                                        <span class="fc-dur-stop" style="color: {f['stopsColor']}">{f['stops']}</span>
                                    </div>
                                    <div class="fc-time-block">
                                        <div class="fc-time">{f['aTime']}</div>
                                        <div class="fc-code">{f['to']}, T2</div>
                                    </div>
                                </div>
                                <div class="fc-pricing-row">
                                    <div class="fc-price-col student-fare-active">
                                        <div class="fc-class-name eco">Economy</div>
                                        <div class="fc-price-val"><span class="price-strikethrough">₹{f['oldP']}</span> ₹{f['newP']} <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></div>
                                    </div>
                                </div>
                            </div>
"""

new_trending_section = f"""<!-- Trending Student Fares Preview -->
                        <div style="margin-top: 24px; position: relative; z-index: 20; padding-bottom: 250px;">
                            <div style="font-size: 15px; font-weight: 800; margin-bottom: 12px; color: #1e293b;">Trending Student Fares</div>
{cards_html}
                        </div>"""

# Regex to find everything from <!-- Trending Student Fares Preview --> down to the closing </div> before screenDestinationAI
pattern = r"<!-- Trending Student Fares Preview -->.*?</div>\s*</div>\s*</div>\s*<div class=\"screen\" id=\"screenDestinationAI\">"

# We must keep the closing tags!
replacement = new_trending_section + '\n                    </div>\n                </div>\n\n<div class="screen" id="screenDestinationAI">'

new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(new_html)

print("Injected 10 cards!")
