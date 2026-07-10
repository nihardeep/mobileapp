import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_html = """                                            <!-- Insta-Style Floating Benefits (Add-ons only) -->
                                            <div style="padding: 10px 16px 12px; display: flex; flex-direction: column; align-items: center; gap: 10px; position: relative;">
                                                <div style="position: relative; width: 130px; height: 60px; margin-bottom: 2px;">
                                                    <!-- Bubble 1: Meal -->
                                                    <div style="position: absolute; left: 0px; top: 10px; width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%); border: 2px solid #0284c7; box-shadow: 0 4px 10px rgba(0,27,148,0.2); display: flex; align-items: center; justify-content: center; z-index: 1;">
                                                        <img src="sandwich.png" style="width: 38px; height: 38px; border-radius: 50%; object-fit: cover;" alt="Sandwich"/>
                                                    </div>
                                                    <!-- Bubble 2: Seat -->
                                                    <div style="position: absolute; left: 35px; top: -2px; width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #ffffff 0%, #bae6fd 100%); border: 3px solid #0ea5e9; box-shadow: 0 6px 12px rgba(0,27,148,0.3); display: flex; align-items: center; justify-content: center; z-index: 2;">
                                                        <img src="seat.png" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" alt="Seat"/>
                                                    </div>
                                                    <!-- Bubble 3: Priority -->
                                                    <div style="position: absolute; left: 82px; top: 10px; width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%); border: 2px solid #0284c7; box-shadow: 0 4px 10px rgba(0,27,148,0.2); display: flex; align-items: center; justify-content: center; z-index: 1;">
                                                        <span style="font-size: 20px;">⏱️</span>
                                                    </div>
                                                    
                                                    <!-- SAVE 500 Promo Badge -->
                                                    <div style="position: absolute; right: -30px; top: -10px; width: 42px; height: 42px; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 10; transform: rotate(10deg);">
                                                        <svg style="position: absolute; width: 100%; height: 100%; z-index: -1; drop-shadow: 0 2px 4px rgba(0,0,0,0.2);" viewBox="0 0 100 100">
                                                            <path fill="#14b8a6" d="M50 0 L61 11 L77 8 L82 23 L98 28 L91 42 L100 55 L88 65 L90 81 L75 82 L65 95 L50 88 L35 95 L25 82 L10 81 L12 65 L0 55 L9 42 L2 28 L18 23 L23 8 L39 11 Z"/>
                                                        </svg>
                                                        <span style="font-size: 9px; font-weight: 900; color: #ffffff; line-height: 1; margin-top: 2px;">SAVE</span>
                                                        <span style="font-size: 11px; font-weight: 900; color: #ffffff; line-height: 1;">₹500</span>
                                                    </div>
                                                </div>"""

new_html = """                                            <!-- Insta-Style Floating Benefits (Add-ons only) -->
                                            <div style="padding: 10px 16px 16px; display: flex; flex-direction: column; align-items: center; gap: 14px; position: relative;">
                                                <div style="position: relative; width: 170px; height: 60px; margin-bottom: 6px;">
                                                    <!-- Bubble 1: Meal -->
                                                    <div style="position: absolute; left: 0px; top: 10px; width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%); border: 2px solid #0284c7; box-shadow: 0 4px 10px rgba(0,27,148,0.2); display: flex; align-items: center; justify-content: center; z-index: 1;">
                                                        <img src="sandwich.png" style="width: 38px; height: 38px; border-radius: 50%; object-fit: cover;" alt="Sandwich"/>
                                                        <div style="position: absolute; bottom: -10px; left: 50%; transform: translateX(-50%); background: #1e1b4b; color: white; font-size: 8px; font-weight: 800; padding: 2px 6px; border-radius: 8px; white-space: nowrap; box-shadow: 0 2px 4px rgba(0,0,0,0.3); z-index: 10; border: 1px solid rgba(255,255,255,0.2);">Veg Club</div>
                                                    </div>
                                                    <!-- Bubble 2: Seat -->
                                                    <div style="position: absolute; left: 55px; top: -2px; width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #ffffff 0%, #bae6fd 100%); border: 3px solid #0ea5e9; box-shadow: 0 6px 12px rgba(0,27,148,0.3); display: flex; align-items: center; justify-content: center; z-index: 2;">
                                                        <img src="seat.png" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" alt="Seat"/>
                                                        <div style="position: absolute; bottom: -10px; left: 50%; transform: translateX(-50%); background: #1e1b4b; color: white; font-size: 9px; font-weight: 800; padding: 3px 8px; border-radius: 8px; white-space: nowrap; box-shadow: 0 2px 4px rgba(0,0,0,0.3); z-index: 10; border: 1px solid rgba(255,255,255,0.2);">Seat 12A</div>
                                                    </div>
                                                    <!-- Bubble 3: Priority -->
                                                    <div style="position: absolute; left: 122px; top: 10px; width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%); border: 2px solid #0284c7; box-shadow: 0 4px 10px rgba(0,27,148,0.2); display: flex; align-items: center; justify-content: center; z-index: 1;">
                                                        <span style="font-size: 20px;">⏱️</span>
                                                        <div style="position: absolute; bottom: -10px; left: 50%; transform: translateX(-50%); background: #1e1b4b; color: white; font-size: 8px; font-weight: 800; padding: 2px 6px; border-radius: 8px; white-space: nowrap; box-shadow: 0 2px 4px rgba(0,0,0,0.3); z-index: 10; border: 1px solid rgba(255,255,255,0.2);">Fast Track</div>
                                                    </div>
                                                    
                                                    <!-- SAVE 500 Promo Badge -->
                                                    <div style="position: absolute; right: -25px; top: -15px; width: 42px; height: 42px; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 10; transform: rotate(10deg);">
                                                        <svg style="position: absolute; width: 100%; height: 100%; z-index: -1; drop-shadow: 0 2px 4px rgba(0,0,0,0.2);" viewBox="0 0 100 100">
                                                            <path fill="#14b8a6" d="M50 0 L61 11 L77 8 L82 23 L98 28 L91 42 L100 55 L88 65 L90 81 L75 82 L65 95 L50 88 L35 95 L25 82 L10 81 L12 65 L0 55 L9 42 L2 28 L18 23 L23 8 L39 11 Z"/>
                                                        </svg>
                                                        <span style="font-size: 9px; font-weight: 900; color: #ffffff; line-height: 1; margin-top: 2px;">SAVE</span>
                                                        <span style="font-size: 11px; font-weight: 900; color: #ffffff; line-height: 1;">₹500</span>
                                                    </div>
                                                </div>"""

content = content.replace(old_html, new_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Labels added.")
