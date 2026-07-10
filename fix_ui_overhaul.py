import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_html = """                                            <div class="pass-details-grid" style="grid-template-columns: 1.1fr 1.3fr 0.6fr 1fr;">
                                                <div class="pass-detail-col">
                                                    <span class="pass-detail-label">FLIGHT</span>
                                                    <span class="pass-detail-val">6E 2015</span>
                                                </div>
                                                <div class="pass-detail-col">
                                                    <span class="pass-detail-label">CLASS</span>
                                                    <span class="pass-detail-val" style="color: #ffffff;">STRETCH</span>
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
                                            
                                            <!-- Rewards & Savings Banner (Premium Glassmorphic) -->
                                            <div style="margin: 8px 16px; background: rgba(56, 189, 248, 0.2); border-radius: 10px; padding: 8px 12px; display: flex; flex-direction: column; gap: 4px; border: 1px solid rgba(255, 255, 255, 0.3); position: relative; overflow: hidden; box-shadow: inset 0 2px 10px rgba(255,255,255,0.2);">
                                                <div style="display: flex; align-items: center; justify-content: space-between; z-index: 1;">
                                                    <div style="display: flex; align-items: center; gap: 6px;">
                                                        <span style="background: linear-gradient(135deg, #f59e0b, #d97706); color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 9px; font-weight: 900; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(245, 158, 11, 0.4);">BLUCHIP</span>
                                                        <span style="font-size: 12px; font-weight: 800; color: #ffffff;">Earns 500 Points</span>
                                                    </div>
                                                </div>
                                                <div style="font-size: 11px; font-weight: 700; color: #ffffff; display: flex; align-items: center; gap: 4px; z-index: 1;">
                                                    <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1.41 16.09V20h-2.67v-1.93c-1.71-.36-3.16-1.46-3.27-3.4h1.96c.1 1.05.82 1.87 2.65 1.87 1.96 0 2.4-.98 2.4-1.59 0-.83-.44-1.61-2.67-2.14-2.48-.6-4.18-1.62-4.18-3.67 0-1.72 1.43-2.81 3.11-3.14V3.9h2.67v1.95c1.28.32 2.64 1.34 2.87 3.03h-1.95c-.2-1.04-.99-1.64-2.25-1.64-1.55 0-2.11.85-2.11 1.49 0 .91.56 1.45 2.83 2.01 2.8.68 4.02 1.87 4.02 3.73 0 2.06-1.56 3.06-3.41 3.42z"/></svg>
                                                    You save ₹500 on your usual add-ons!
                                                </div>
                                            </div>"""

new_html = """                                            <!-- Insta-Style Floating Benefits -->
                                            <div style="padding: 16px; display: flex; flex-direction: column; align-items: center; gap: 12px; position: relative;">
                                                <div style="position: relative; width: 140px; height: 80px; margin-bottom: 8px;">
                                                    <!-- Bubble 1: Meal -->
                                                    <div style="position: absolute; left: 0px; top: 10px; width: 50px; height: 50px; border-radius: 50%; background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%); border: 2px solid #0284c7; box-shadow: 0 6px 12px rgba(0,27,148,0.2); display: flex; align-items: center; justify-content: center; z-index: 1;">
                                                        <span style="font-size: 24px;">🥪</span>
                                                    </div>
                                                    <!-- Bubble 2: Seat -->
                                                    <div style="position: absolute; left: 35px; top: -5px; width: 66px; height: 66px; border-radius: 50%; background: linear-gradient(135deg, #ffffff 0%, #bae6fd 100%); border: 3px solid #0ea5e9; box-shadow: 0 8px 16px rgba(0,27,148,0.3); display: flex; align-items: center; justify-content: center; z-index: 2;">
                                                        <span style="font-size: 32px;">💺</span>
                                                    </div>
                                                    <!-- Bubble 3: Priority -->
                                                    <div style="position: absolute; left: 88px; top: 15px; width: 45px; height: 45px; border-radius: 50%; background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%); border: 2px solid #0284c7; box-shadow: 0 6px 12px rgba(0,27,148,0.2); display: flex; align-items: center; justify-content: center; z-index: 1;">
                                                        <span style="font-size: 20px;">⏱️</span>
                                                    </div>
                                                </div>
                                                <div style="text-align: center; color: rgba(255,255,255,0.95); font-size: 11px; line-height: 1.5; padding: 0 20px;">
                                                    <strong style="color: #ffffff; font-weight: 800;">Veg Club, Seat 12A, Fast Track</strong><br/>
                                                    and 3 of your other usuals are already included.
                                                </div>
                                            </div>
                                            
                                            <!-- Rewards & Savings Banner (Super Sexy Credit Card Style) -->
                                            <div class="bluchip-sexy-card" style="margin: 0px 16px 12px; position: relative; overflow: hidden; border-radius: 16px; background: linear-gradient(135deg, #0a0a0a 0%, #1e1b4b 50%, #000000 100%); padding: 14px 16px; box-shadow: 0 10px 24px rgba(0,0,0,0.4), inset 0 1px 1px rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.15);">
                                                <!-- Shimmer Animation Overlay -->
                                                <div class="shimmer-overlay" style="position: absolute; top: 0; left: -150%; width: 50%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent); transform: skewX(-20deg); animation: shimmer 3.5s infinite ease-in-out;"></div>
                                                <!-- Floating particles / background grid -->
                                                <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-image: radial-gradient(rgba(245, 158, 11, 0.15) 1px, transparent 1px); background-size: 12px 12px; opacity: 0.6;"></div>
                                                
                                                <div style="position: relative; z-index: 2; display: flex; align-items: center; justify-content: space-between;">
                                                    <div style="display: flex; align-items: center; gap: 14px;">
                                                        <!-- 3D Coin Icon -->
                                                        <div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #fbbf24 0%, #b45309 100%); display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.5), inset 0 -2px 4px rgba(0,0,0,0.5), inset 0 2px 4px rgba(255,255,255,0.8);">
                                                            <span style="color: #fff; font-weight: 900; font-size: 18px; letter-spacing: -1px; text-shadow: 0 1px 3px rgba(0,0,0,0.6);">B</span>
                                                        </div>
                                                        <div style="display: flex; flex-direction: column;">
                                                            <span style="font-size: 10px; font-weight: 800; color: #fbbf24; letter-spacing: 1.5px; text-transform: uppercase;">BluChip Rewards</span>
                                                            <span style="font-size: 16px; font-weight: 900; color: #ffffff; text-shadow: 0 2px 6px rgba(0,0,0,0.5); margin-top: 1px;">Earns 500 Points</span>
                                                        </div>
                                                    </div>
                                                </div>
                                                
                                                <!-- Glowing Savings Badge -->
                                                <div style="position: relative; z-index: 2; margin-top: 14px; display: inline-flex; align-items: center; gap: 6px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); padding: 5px 12px; border-radius: 20px; box-shadow: 0 0 12px rgba(16, 185, 129, 0.25);">
                                                    <span style="font-size: 12px; font-weight: 800; color: #34d399;">You save ₹500 on add-ons!</span>
                                                </div>
                                            </div>"""

content = content.replace(old_html, new_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Redesign HTML applied.")

with open('style.css', 'a', encoding='utf-8') as f:
    f.write('''
/* Shimmer animation for Sexy BluChip card */
@keyframes shimmer {
    0% { left: -150%; }
    50% { left: 150%; }
    100% { left: 150%; }
}
''')

print("CSS appended.")
