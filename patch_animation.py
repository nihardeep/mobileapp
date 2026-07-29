import re

with open('app.js', 'r') as f:
    js = f.read()

old_svg = """                    <div style="margin-right: 8px;">
                        <svg class="running-risk" style="animation: runningUrgency 0.6s infinite alternate;" viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="#ea580c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="5" r="2" fill="#1e293b" stroke="#1e293b"></circle>
                            <path d="M12 7 L12 13" stroke="#ea580c" stroke-width="4"></path>
                            <path d="M12 9 L8 11 L6 8" stroke="#ea580c" stroke-width="3"></path>
                            <path d="M12 9 L15 11 L18 10" stroke="#ea580c" stroke-width="3"></path>
                            <path d="M12 13 L10 18 L12 21" stroke="#1e293b" stroke-width="3"></path>
                            <path d="M12 13 L15 16 L17 14" stroke="#1e293b" stroke-width="3"></path>
                        </svg>
                    </div>"""

new_svg = """                    <div style="margin-right: 8px; position: relative;">
                        <!-- Speed lines -->
                        <svg class="speed-lines" viewBox="0 0 24 24" width="48" height="48" style="position: absolute; top:0; left: -10px; z-index: 0; opacity: 0.5;">
                            <line x1="12" y1="8" x2="2" y2="8" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round" class="line1" />
                            <line x1="10" y1="14" x2="0" y2="14" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round" class="line2" />
                            <line x1="14" y1="19" x2="4" y2="19" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round" class="line3" />
                        </svg>
                        
                        <svg class="running-risk-body" viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="#ea580c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="position: relative; z-index: 1;">
                            <circle cx="12" cy="5" r="2" fill="#1e293b" stroke="#1e293b"></circle>
                            <!-- Torso -->
                            <path d="M12 7 L14 13" stroke="#ea580c" stroke-width="4"></path>
                            <!-- Left Arm (Back) -->
                            <path class="run-arm-left" d="M12 8 L8 9 L6 6" stroke="#ea580c" stroke-width="3" style="transform-origin: 12px 8px;"></path>
                            <!-- Right Arm (Front) -->
                            <path class="run-arm-right" d="M12 8 L17 10 L20 7" stroke="#ea580c" stroke-width="3" style="transform-origin: 12px 8px;"></path>
                            <!-- Left Leg (Back) -->
                            <path class="run-leg-left" d="M14 13 L11 17 L8 17" stroke="#1e293b" stroke-width="3.5" style="transform-origin: 14px 13px;"></path>
                            <!-- Right Leg (Front) -->
                            <path class="run-leg-right" d="M14 13 L17 18 L19 22" stroke="#1e293b" stroke-width="3.5" style="transform-origin: 14px 13px;"></path>
                        </svg>
                    </div>"""

if old_svg in js:
    js = js.replace(old_svg, new_svg)
    with open('app.js', 'w') as f:
        f.write(js)
    print("Replaced SVG in app.js")
else:
    print("SVG block not found in app.js!")

with open('style.css', 'r') as f:
    css = f.read()

old_css = """@keyframes runningUrgency {
    0% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-3px) rotate(8deg); }
    100% { transform: translateY(0) rotate(0deg); }
}

.timeline-node.running-risk svg {
    animation: runningUrgency 0.6s infinite alternate;
}"""

new_css = """@keyframes bodyBobbing {
    0% { transform: translateY(0) rotate(5deg); }
    100% { transform: translateY(-3px) rotate(8deg); }
}

@keyframes limbSwingFront {
    0% { transform: rotate(-35deg); }
    100% { transform: rotate(45deg); }
}

@keyframes limbSwingBack {
    0% { transform: rotate(45deg); }
    100% { transform: rotate(-35deg); }
}

@keyframes speedLine {
    0% { transform: translateX(0); opacity: 0; }
    50% { opacity: 0.8; }
    100% { transform: translateX(-15px); opacity: 0; }
}

.running-risk-body {
    animation: bodyBobbing 0.25s infinite alternate ease-in-out;
}

.run-arm-left, .run-leg-right {
    animation: limbSwingBack 0.25s infinite alternate ease-in-out;
}

.run-arm-right, .run-leg-left {
    animation: limbSwingFront 0.25s infinite alternate ease-in-out;
}

.speed-lines .line1 { animation: speedLine 0.5s infinite linear; }
.speed-lines .line2 { animation: speedLine 0.7s infinite linear; animation-delay: 0.2s; }
.speed-lines .line3 { animation: speedLine 0.6s infinite linear; animation-delay: 0.1s; }
"""

if old_css in css:
    css = css.replace(old_css, new_css)
else:
    css += "\n" + new_css
    
with open('style.css', 'w') as f:
    f.write(css)
print("Updated style.css")

