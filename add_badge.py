import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_html = """                                                    <!-- Bubble 3: Priority -->
                                                    <div style="position: absolute; left: 82px; top: 10px; width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%); border: 2px solid #0284c7; box-shadow: 0 4px 10px rgba(0,27,148,0.2); display: flex; align-items: center; justify-content: center; z-index: 1;">
                                                        <span style="font-size: 20px;">⏱️</span>
                                                    </div>
                                                </div>"""

new_html = """                                                    <!-- Bubble 3: Priority -->
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

content = content.replace(old_html, new_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Badge added.")
