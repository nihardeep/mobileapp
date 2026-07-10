import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_html = """                                            <!-- Insta-Style Floating Benefits -->
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

new_html = """                                            <!-- Flight & Class Header Row -->
                                            <div style="display: flex; justify-content: space-between; padding: 12px 16px 4px; align-items: center;">
                                                <div style="display: flex; flex-direction: column;">
                                                    <span style="font-size: 10px; color: rgba(255,255,255,0.7); font-weight: 800; letter-spacing: 1px;">FLIGHT</span>
                                                    <span style="font-size: 15px; font-weight: 800; color: #ffffff; margin-top: 2px;">6E 2015</span>
                                                </div>
                                                <div style="display: flex; flex-direction: column; align-items: flex-end;">
                                                    <span style="font-size: 10px; color: rgba(255,255,255,0.7); font-weight: 800; letter-spacing: 1px;">CLASS</span>
                                                    <span style="font-size: 15px; font-weight: 900; color: #f59e0b; margin-top: 2px;">STRETCH</span>
                                                </div>
                                            </div>

                                            <!-- Insta-Style Floating Benefits (Add-ons only) -->
                                            <div style="padding: 10px 16px 12px; display: flex; flex-direction: column; align-items: center; gap: 10px; position: relative;">
                                                <div style="position: relative; width: 130px; height: 60px; margin-bottom: 2px;">
                                                    <!-- Bubble 1: Meal -->
                                                    <div style="position: absolute; left: 0px; top: 10px; width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%); border: 2px solid #0284c7; box-shadow: 0 4px 10px rgba(0,27,148,0.2); display: flex; align-items: center; justify-content: center; z-index: 1;">
                                                        <span style="font-size: 20px;">🥪</span>
                                                    </div>
                                                    <!-- Bubble 2: Seat -->
                                                    <div style="position: absolute; left: 35px; top: -2px; width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #ffffff 0%, #bae6fd 100%); border: 3px solid #0ea5e9; box-shadow: 0 6px 12px rgba(0,27,148,0.3); display: flex; align-items: center; justify-content: center; z-index: 2;">
                                                        <span style="font-size: 28px;">💺</span>
                                                    </div>
                                                    <!-- Bubble 3: Priority -->
                                                    <div style="position: absolute; left: 82px; top: 10px; width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%); border: 2px solid #0284c7; box-shadow: 0 4px 10px rgba(0,27,148,0.2); display: flex; align-items: center; justify-content: center; z-index: 1;">
                                                        <span style="font-size: 20px;">⏱️</span>
                                                    </div>
                                                </div>
                                                <div style="text-align: center; color: rgba(255,255,255,0.95); font-size: 11px; line-height: 1.4; padding: 0 20px;">
                                                    <strong style="color: #ffffff; font-weight: 800;">Veg Club, Seat 12A, Fast Track</strong><br/>
                                                    are already included.
                                                </div>
                                            </div>
                                            
                                            <!-- Striking Benefits Panel -->
                                            <div style="margin: 0px 16px 10px; background: rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 12px; border: 1px solid rgba(255, 255, 255, 0.2); box-shadow: 0 4px 12px rgba(0,0,0,0.1); display: flex; flex-direction: column; gap: 8px;">
                                                <div style="display: flex; align-items: center; gap: 10px;">
                                                    <div style="background: rgba(16, 185, 129, 0.2); border-radius: 50%; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center;">
                                                        <span style="font-size: 13px;">💰</span>
                                                    </div>
                                                    <span style="font-size: 12px; font-weight: 700; color: #34d399;">Saves you ₹500 on add-ons</span>
                                                </div>
                                                <div style="display: flex; align-items: center; gap: 10px;">
                                                    <div style="background: rgba(56, 189, 248, 0.2); border-radius: 50%; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center;">
                                                        <span style="font-size: 13px;">⚡</span>
                                                    </div>
                                                    <span style="font-size: 12px; font-weight: 700; color: #ffffff;">Seamless journey with pre-selected usuals</span>
                                                </div>
                                                <div style="display: flex; align-items: center; gap: 10px;">
                                                    <div style="background: rgba(245, 158, 11, 0.2); border-radius: 50%; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 0 4px rgba(245,158,11,0.5);">
                                                        <span style="font-size: 12px; color: #fbbf24; font-weight: 900; text-shadow: 0 1px 2px rgba(0,0,0,0.5);">B</span>
                                                    </div>
                                                    <span style="font-size: 12px; font-weight: 700; color: #fcd34d;">Earns 500 BluChip Points</span>
                                                </div>
                                            </div>"""

content = content.replace(old_html, new_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Redesign HTML applied.")
