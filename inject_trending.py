import re

with open('index.html', 'r') as f:
    html = f.read()

injection = """
                        <!-- Trending Student Fares Preview -->
                        <div style="margin-top: 24px;">
                            <div style="font-size: 15px; font-weight: 800; margin-bottom: 12px; color: #1e293b;">Trending Student Fares</div>
                            
                            <!-- Sample Card 1 -->
                            <div class="flight-card" onclick="activateStudentModeAndSearch()" style="margin-bottom: 12px; cursor: pointer; position: relative;">
                                <div class="student-edge-badge">✨ Free Change • 🧳 15Kg Extra</div>
                                <div class="fc-header">
                                    <span>6E 1234</span>
                                    <span style="color: var(--indigo-blue); background: rgba(0, 95, 169, 0.05); padding: 2px 6px; border-radius: 4px;">Earn up to 400 BluChips</span>
                                </div>
                                <div class="fc-times-row">
                                    <div class="fc-time-block">
                                        <div class="fc-time">05:15</div>
                                        <div class="fc-code">DEL, T1</div>
                                    </div>
                                    <div class="fc-duration">
                                        <span class="fc-dur-text">2h 15m</span>
                                        <div class="fc-dur-line"></div>
                                        <span class="fc-dur-stop" style="color: #10b981">Non-stop</span>
                                    </div>
                                    <div class="fc-time-block">
                                        <div class="fc-time">07:30</div>
                                        <div class="fc-code">BOM, T2</div>
                                    </div>
                                </div>
                                <div class="fc-pricing-row">
                                    <div class="fc-price-col student-fare-active">
                                        <div class="fc-class-name eco">Economy</div>
                                        <div class="fc-price-val"><span class="price-strikethrough">₹4,800</span> ₹4,320 <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Sample Card 2 -->
                            <div class="flight-card" onclick="activateStudentModeAndSearch()" style="margin-bottom: 12px; cursor: pointer; position: relative;">
                                <div class="student-edge-badge">✨ Free Change • 🧳 15Kg Extra</div>
                                <div class="fc-header">
                                    <span>6E 5678</span>
                                    <span style="color: var(--indigo-blue); background: rgba(0, 95, 169, 0.05); padding: 2px 6px; border-radius: 4px;">Earn up to 400 BluChips</span>
                                </div>
                                <div class="fc-times-row">
                                    <div class="fc-time-block">
                                        <div class="fc-time">06:30</div>
                                        <div class="fc-code">DEL, T1</div>
                                    </div>
                                    <div class="fc-duration">
                                        <span class="fc-dur-text">4h 15m</span>
                                        <div class="fc-dur-line"></div>
                                        <span class="fc-dur-stop" style="color: var(--indigo-blue)">1 Stop</span>
                                    </div>
                                    <div class="fc-time-block">
                                        <div class="fc-time">10:45</div>
                                        <div class="fc-code">BOM, T2</div>
                                    </div>
                                </div>
                                <div class="fc-pricing-row">
                                    <div class="fc-price-col student-fare-active">
                                        <div class="fc-class-name eco">Economy</div>
                                        <div class="fc-price-val"><span class="price-strikethrough">₹5,500</span> ₹4,950 <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></div>
                                    </div>
                                </div>
                            </div>

                        </div>
"""

# The insertion point is right before `</div>\n                </div>\n\n<div class="screen" id="screenDestinationAI">`
target = "                    </div>\n                </div>\n\n<div class=\"screen\" id=\"screenDestinationAI\">"
replacement = injection + target

if "Trending Student Fares Preview" not in html:
    html = html.replace(target, replacement)
    with open('index.html', 'w') as f:
        f.write(html)
    print("Injected Trending Cards!")
else:
    print("Already injected.")
