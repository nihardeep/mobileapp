import re

with open('app.js', 'r') as f:
    js = f.read()

# Replace the previous SVG block
old_svg = """                    <div style="margin-right: 8px; position: relative;">
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

new_svg = """                    <div style="margin-right: 8px; position: relative; width: 48px; height: 48px;">
                        <!-- Fast Speed lines -->
                        <svg class="speed-lines-v2" viewBox="0 0 40 40" width="48" height="48" style="position: absolute; top:0; left: -15px; z-index: 0;">
                            <line x1="20" y1="10" x2="0" y2="10" stroke="#cbd5e1" stroke-width="2.5" stroke-linecap="round" class="line1" />
                            <line x1="15" y1="20" x2="-5" y2="20" stroke="#cbd5e1" stroke-width="2.5" stroke-linecap="round" class="line2" />
                            <line x1="25" y1="30" x2="5" y2="30" stroke="#cbd5e1" stroke-width="2.5" stroke-linecap="round" class="line3" />
                        </svg>
                        
                        <!-- Stylized Running Person (Matches Mockup) -->
                        <svg class="running-risk-v2" viewBox="0 0 40 40" width="48" height="48" style="position: relative; z-index: 1;">
                            <!-- Back Arm (Left) -->
                            <path d="M22 15 L14 18 L10 12" fill="none" stroke="#f43f5e" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"></path>
                            <!-- Back Leg (Left) -->
                            <path d="M20 24 L12 26 L8 22" fill="none" stroke="#0f172a" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"></path>
                            
                            <!-- Torso (Red Shirt) -->
                            <path d="M22 12 Q25 18, 20 25" fill="none" stroke="#f43f5e" stroke-width="8" stroke-linecap="round"></path>
                            
                            <!-- Head -->
                            <circle cx="25" cy="8" r="4.5" fill="#0f172a"></circle>
                            
                            <!-- Front Arm (Right) -->
                            <path d="M22 15 L28 17 L30 11" fill="none" stroke="#e11d48" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"></path>
                            
                            <!-- Front Leg (Right) -->
                            <path d="M20 24 L28 28 L23 36" fill="none" stroke="#0f172a" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"></path>
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

# Add new CSS for v2 animation
new_css = """
@keyframes sprintWiggle {
    0% { transform: translateY(0) rotate(-3deg); }
    100% { transform: translateY(-2px) rotate(3deg); }
}

.running-risk-v2 {
    animation: sprintWiggle 0.12s infinite alternate linear;
}

@keyframes speedLineV2 {
    0% { transform: translateX(0); opacity: 0; }
    50% { opacity: 1; }
    100% { transform: translateX(-20px); opacity: 0; }
}

.speed-lines-v2 .line1 { animation: speedLineV2 0.3s infinite linear; }
.speed-lines-v2 .line2 { animation: speedLineV2 0.4s infinite linear; animation-delay: 0.1s; }
.speed-lines-v2 .line3 { animation: speedLineV2 0.35s infinite linear; animation-delay: 0.2s; }
"""

css += "\n" + new_css
    
with open('style.css', 'w') as f:
    f.write(css)
print("Updated style.css")

