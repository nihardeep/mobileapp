import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Cab Card Padding
html = html.replace('<div id="companionCabDeals" style="margin-top: 16px; display: none; padding: 0 20px; order: 4;">',
                    '<div id="companionCabDeals" style="margin-top: 16px; display: none; padding: 0 12px; order: 4;">')

# 2. Add CTR Arrow & Fix Taxi Size
# We need to find the Taxi img tag inside companionCabDeals
cab_start = html.find('id="companionCabDeals"')
cab_end = html.find('id="companionHotelDeals"')

cab_html = html[cab_start:cab_end]

old_taxi = '<img src="https://pngimg.com/uploads/taxi/taxi_PNG74.png" alt="Taxi" style="position: absolute; right: 10px; bottom: -10px; width: 110px; z-index: 1; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.25));" />'
new_taxi = """<img src="https://pngimg.com/uploads/taxi/taxi_PNG74.png" alt="Taxi" style="position: absolute; right: -15px; bottom: -15px; width: 155px; z-index: 1; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.3));" />
        
        <!-- CTR Arrow -->
        <div style="position: absolute; right: 12px; top: 12px; z-index: 3; background: #fff; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#005eb8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </div>"""

new_cab_html = cab_html.replace(old_taxi, new_taxi)
html = html[:cab_start] + new_cab_html + html[cab_end:]


# 3. CRED Style Hotel Cards
# We need to replace the entire content of <div style="display: flex; gap: 16px; overflow-x: auto; scroll-snap-type: x mandatory; padding: 0 20px 20px 20px; margin: 0; scrollbar-width: none;">
hotel_start = html.find('id="companionHotelDeals"')
loyalty_start = html.find('id="loyaltySection"')

hotel_html = html[hotel_start:loyalty_start]

# Find the start of the cards container
cards_container_start = hotel_html.find('<div style="display: flex; gap: 16px;')
# Find the end of the cards container
# We know it ends just before '</div>\n\n                            <!-- Loyalty Panel'
cards_container_end = hotel_html.rfind('</div>', 0, hotel_html.rfind('</div>') - 1)

cred_cards = """<div style="display: flex; gap: 12px; overflow-x: auto; scroll-snap-type: x mandatory; padding: 0 20px 20px 20px; margin: 0; scrollbar-width: none; -webkit-overflow-scrolling: touch;">
        <!-- CRED-Inspired Hotel Card 1 -->
        <div style="flex: 0 0 145px; height: 200px; scroll-snap-align: center; border-radius: 16px; overflow: hidden; position: relative; box-shadow: 0 10px 24px rgba(0,0,0,0.12); border: 1px solid rgba(255,255,255,0.4); cursor: pointer;">
            <div style="position: absolute; inset: 0; background: url('https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&q=80') center/cover; z-index: 1;"></div>
            <div style="position: absolute; inset: 0; background: linear-gradient(to top, #0f172a 0%, rgba(15,23,42,0.6) 40%, rgba(15,23,42,0) 80%); z-index: 2;"></div>
            
            <div style="position: absolute; top: 10px; left: 10px; background: rgba(16, 185, 129, 0.95); color: #fff; padding: 4px 8px; border-radius: 6px; font-size: 9px; font-weight: 900; text-transform: uppercase; z-index: 3; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.4); letter-spacing: 0.5px;">
                30% OFF
            </div>
            
            <div style="position: absolute; bottom: 0; left: 0; width: 100%; padding: 12px; z-index: 3; box-sizing: border-box;">
                <h4 style="margin: 0 0 2px 0; font-size: 15px; font-weight: 800; color: #fff; line-height: 1.2;">Taj Lands End</h4>
                <div style="font-size: 10px; font-weight: 600; color: #94a3b8; margin-bottom: 8px;">Mumbai</div>
                
                <div style="display: flex; align-items: flex-end; justify-content: space-between;">
                    <div>
                        <div style="font-size: 9px; color: #cbd5e1; text-decoration: line-through; opacity: 0.7;">₹18,500</div>
                        <div style="font-size: 16px; font-weight: 900; color: #fff; letter-spacing: -0.5px;">₹12,950</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); padding: 6px; border-radius: 50%; color: #fff; border: 1px solid rgba(255,255,255,0.25);">
                        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- CRED-Inspired Hotel Card 2 -->
        <div style="flex: 0 0 145px; height: 200px; scroll-snap-align: center; border-radius: 16px; overflow: hidden; position: relative; box-shadow: 0 10px 24px rgba(0,0,0,0.12); border: 1px solid rgba(255,255,255,0.4); cursor: pointer;">
            <div style="position: absolute; inset: 0; background: url('https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80') center/cover; z-index: 1;"></div>
            <div style="position: absolute; inset: 0; background: linear-gradient(to top, #0f172a 0%, rgba(15,23,42,0.6) 40%, rgba(15,23,42,0) 80%); z-index: 2;"></div>
            
            <div style="position: absolute; top: 10px; left: 10px; background: rgba(16, 185, 129, 0.95); color: #fff; padding: 4px 8px; border-radius: 6px; font-size: 9px; font-weight: 900; text-transform: uppercase; z-index: 3; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.4); letter-spacing: 0.5px;">
                25% OFF
            </div>
            
            <div style="position: absolute; bottom: 0; left: 0; width: 100%; padding: 12px; z-index: 3; box-sizing: border-box;">
                <h4 style="margin: 0 0 2px 0; font-size: 15px; font-weight: 800; color: #fff; line-height: 1.2;">Trident Hotel</h4>
                <div style="font-size: 10px; font-weight: 600; color: #94a3b8; margin-bottom: 8px;">Nariman Point</div>
                
                <div style="display: flex; align-items: flex-end; justify-content: space-between;">
                    <div>
                        <div style="font-size: 9px; color: #cbd5e1; text-decoration: line-through; opacity: 0.7;">₹15,000</div>
                        <div style="font-size: 16px; font-weight: 900; color: #fff; letter-spacing: -0.5px;">₹11,250</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); padding: 6px; border-radius: 50%; color: #fff; border: 1px solid rgba(255,255,255,0.25);">
                        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
                    </div>
                </div>
            </div>
        </div>

        <!-- CRED-Inspired Hotel Card 3 -->
        <div style="flex: 0 0 145px; height: 200px; scroll-snap-align: center; border-radius: 16px; overflow: hidden; position: relative; box-shadow: 0 10px 24px rgba(0,0,0,0.12); border: 1px solid rgba(255,255,255,0.4); cursor: pointer;">
            <div style="position: absolute; inset: 0; background: url('https://images.unsplash.com/photo-1542314831-c6a4d27a658d?w=600&q=80') center/cover; z-index: 1;"></div>
            <div style="position: absolute; inset: 0; background: linear-gradient(to top, #0f172a 0%, rgba(15,23,42,0.6) 40%, rgba(15,23,42,0) 80%); z-index: 2;"></div>
            
            <div style="position: absolute; top: 10px; left: 10px; background: rgba(59, 130, 246, 0.95); color: #fff; padding: 4px 8px; border-radius: 6px; font-size: 9px; font-weight: 900; text-transform: uppercase; z-index: 3; box-shadow: 0 4px 10px rgba(59, 130, 246, 0.4); letter-spacing: 0.5px;">
                NEW
            </div>
            
            <div style="position: absolute; bottom: 0; left: 0; width: 100%; padding: 12px; z-index: 3; box-sizing: border-box;">
                <h4 style="margin: 0 0 2px 0; font-size: 15px; font-weight: 800; color: #fff; line-height: 1.2;">JW Marriott</h4>
                <div style="font-size: 10px; font-weight: 600; color: #94a3b8; margin-bottom: 8px;">Juhu</div>
                
                <div style="display: flex; align-items: flex-end; justify-content: space-between;">
                    <div>
                        <div style="font-size: 9px; color: #cbd5e1; text-decoration: line-through; opacity: 0.7;">₹21,000</div>
                        <div style="font-size: 16px; font-weight: 900; color: #fff; letter-spacing: -0.5px;">₹18,500</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); padding: 6px; border-radius: 50%; color: #fff; border: 1px solid rgba(255,255,255,0.25);">
                        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
                    </div>
                </div>
            </div>
        </div>
    </div>"""

new_hotel_html = hotel_html[:cards_container_start] + cred_cards + '\n'
html = html[:hotel_start] + new_hotel_html + html[loyalty_start:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated design")
