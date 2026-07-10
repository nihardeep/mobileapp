import re

with open('index.html', 'r') as f:
    content = f.read()

cab_deals = """
<!-- COMPANION CAB DEALS -->
<div id="companionCabDeals" style="margin-top: 24px; padding: 0 20px;">
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
        <div style="font-size: 16px; font-weight: 800; color: #0f172a;">Cab Deals</div>
    </div>
    <div style="display: flex; align-items: center; background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.9); border-radius: 16px; padding: 12px 16px; box-shadow: 0 8px 24px rgba(0,31,84,0.08); position: relative; overflow: hidden; width: 100%; cursor: pointer; min-height: 80px;">
        <!-- Huge Bleeding Taxi Illustration on Right -->
        <img src="https://pngimg.com/uploads/taxi/taxi_PNG74.png" alt="Taxi" style="position: absolute; right: 40px; bottom: -10px; width: 140px; z-index: 1; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.25));" />
        
        <div style="position: absolute; right: 12px; top: 12px; z-index: 3; background: #fff; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#0f172a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
        </div>

        <!-- Animated Keychain SVG coming from left -->
        <div style="position: absolute; left: -10px; top: -20px; width: 60px; height: 120px; transform-origin: top center; z-index: 2; animation: swingKeychain 3s ease-in-out infinite;">
            <svg viewBox="0 0 100 200" width="100%" height="100%">
                <path d="M40 0 L60 0 L60 20 L40 20 Z" fill="#2c1815"/>
                <path d="M50 20 L50 60" stroke="#94a3b8" stroke-width="4"/>
                <circle cx="50" cy="55" r="10" fill="none" stroke="#94a3b8" stroke-width="3"/>
                <rect x="20" y="65" width="60" height="90" rx="8" fill="#e84b38" />
                <circle cx="50" cy="75" r="4" fill="#f8fafc" />
                <path d="M 50 95 C 40 95 32 103 32 115 C 32 127 40 135 50 135 C 57 135 63 131 66 125 L 56 125 C 54 128 52 130 50 130 C 44 130 39 125 39 115 C 39 105 44 100 50 100 C 55 100 59 104 60 110 L 68 110 C 66 98 59 95 50 95 Z" fill="#f8ecec"/>
                <circle cx="38" cy="118" r="4" fill="#f8ecec"/>
                <rect x="52" y="115" width="16" height="5" fill="#f8ecec"/>
                <rect x="63" y="115" width="5" height="20" fill="#f8ecec"/>
            </svg>
        </div>

        <div style="flex: 1; padding-left: 70px; padding-right: 40px; z-index: 3; position: relative;">
            <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-bottom: 2px; letter-spacing: -0.2px;">Airport to City</div>
            <div style="font-size: 13px; font-weight: 600; color: #64748b;">Exclusive Cab Deal</div>
            <!-- Dashed Ticket Coupon -->
            <div style="display: inline-flex; align-items: center; margin-top: 6px; padding: 2px 8px; border: 1px dashed #94a3b8; border-radius: 6px; background: rgba(255,255,255,0.6); font-size: 10px; font-weight: 800; color: #334155; letter-spacing: 0.5px;" onclick="event.stopPropagation(); triggerHaptic('success', 'Code copied!'); alert('Code CAB20 copied!');">
                <svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2.5" style="margin-right: 4px;"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                CODE: CAB20
            </div>
        </div>
    </div>
    <style>
        @keyframes swingKeychain {
            0% { transform: rotate(5deg); }
            50% { transform: rotate(-5deg); }
            100% { transform: rotate(5deg); }
        }
    </style>
</div>
"""

hotel_deals = """
<!-- COMPANION HOTEL DEALS -->
<div id="companionHotelDeals" style="margin-top: 32px; margin-bottom: 24px;">
    <div style="padding: 0 20px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 16px; font-weight: 800; color: #0f172a;">Hotel Deals</span>
            <!-- Torn Ticket Coupon -->
            <div style="display: inline-flex; align-items: center; background: rgba(15, 23, 42, 0.08); padding: 3px 12px; font-size: 11px; font-weight: 800; color: #0f172a; letter-spacing: 0.5px; -webkit-mask-image: radial-gradient(circle at 0 50%, transparent 4px, black 4px), radial-gradient(circle at 100% 50%, transparent 4px, black 4px); -webkit-mask-size: 51% 100%; -webkit-mask-position: left, right; -webkit-mask-repeat: no-repeat; cursor: pointer;" onclick="event.stopPropagation(); triggerHaptic('success', 'Coupon copied!'); alert('Coupon STAY30 copied!');">
                <span style="border-right: 1px dashed rgba(15, 23, 42, 0.3); padding-right: 6px; margin-right: 6px;">✂️</span>STAY30
            </div>
        </div>
        <span style="font-size: 11px; font-weight: 700; color: #005eb8; cursor: pointer;">View All</span>
    </div>
    
    <div style="display: flex; gap: 16px; overflow-x: auto; scroll-snap-type: x mandatory; padding: 0 20px 20px 20px; margin: 0; scrollbar-width: none;">
        <!-- Hotel Card 1 -->
        <div style="flex: 0 0 82%; scroll-snap-align: center; background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.9); border-radius: 16px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,31,84,0.06);">
            <div style="height: 120px; background: url('https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&q=80') center/cover; position: relative;">
                <div style="position: absolute; top: 12px; left: 12px; background: rgba(0,0,0,0.6); backdrop-filter: blur(4px); color: #fff; padding: 4px 8px; border-radius: 8px; font-size: 11px; font-weight: 700;">⭐ 4.8 Excellent</div>
            </div>
            <div style="padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <div>
                        <h4 style="margin: 0 0 2px 0; font-size: 16px; font-weight: 800; color: #0f172a;">Taj Lands End</h4>
                        <span style="font-size: 12px; color: #64748b;">Bandra West, Mumbai</span>
                    </div>
                    <div style="display: inline-block; background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 4px 8px; border-radius: 8px; font-size: 10px; font-weight: 800; text-transform: uppercase;">30% OFF • USE TAJ30</div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: flex-end;">
                    <div>
                        <div style="font-size: 11px; color: #94a3b8; text-decoration: line-through;">₹18,500</div>
                        <div style="font-size: 18px; font-weight: 800; color: #0f172a;">₹12,950 <span style="font-size: 11px; font-weight: 600; color: #64748b;">/night</span></div>
                    </div>
                    <button style="background: #005eb8; color: #fff; border: none; padding: 8px 16px; border-radius: 10px; font-weight: 700; font-size: 13px;">Book</button>
                </div>
            </div>
        </div>
        <!-- Hotel Card 2 -->
        <div style="flex: 0 0 82%; scroll-snap-align: center; background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.9); border-radius: 16px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,31,84,0.06);">
            <div style="height: 120px; background: url('https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80') center/cover; position: relative;">
                <div style="position: absolute; top: 12px; left: 12px; background: rgba(0,0,0,0.6); backdrop-filter: blur(4px); color: #fff; padding: 4px 8px; border-radius: 8px; font-size: 11px; font-weight: 700;">⭐ 4.5 Very Good</div>
            </div>
            <div style="padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <div>
                        <h4 style="margin: 0 0 2px 0; font-size: 16px; font-weight: 800; color: #0f172a;">Trident Nariman Point</h4>
                        <span style="font-size: 12px; color: #64748b;">Nariman Point, Mumbai</span>
                    </div>
                    <div style="display: inline-block; background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 4px 8px; border-radius: 8px; font-size: 10px; font-weight: 800; text-transform: uppercase;">25% OFF</div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: flex-end;">
                    <div>
                        <div style="font-size: 11px; color: #94a3b8; text-decoration: line-through;">₹15,000</div>
                        <div style="font-size: 18px; font-weight: 800; color: #0f172a;">₹11,250 <span style="font-size: 11px; font-weight: 600; color: #64748b;">/night</span></div>
                    </div>
                    <button style="background: #005eb8; color: #fff; border: none; padding: 8px 16px; border-radius: 10px; font-weight: 700; font-size: 13px;">Book</button>
                </div>
            </div>
        </div>
    </div>
</div>
"""

end_idx = content.find('<!-- SCREEN 3: MY TRIPS / COMPANION CARD -->')
if end_idx != -1:
    new_content = content[:end_idx] + cab_deals + hotel_deals + "\n" + content[end_idx:]
    with open('index.html', 'w') as f:
        f.write(new_content)
    print("Injected Cab Deals and Hotel Deals successfully!")
else:
    print("Could not find insertion point!")
