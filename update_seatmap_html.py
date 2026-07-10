import re

with open('index.html', 'r') as f:
    content = f.read()

new_html = """
<div class="screen" id="screenSeatLoading" style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(180deg, #e0f2fe 0%, #ffffff 100%); z-index: 215; overflow: hidden; display: flex; flex-direction: column;">
    
    <!-- Header tabs mimicking the target screen -->
    <div style="padding: 52px 24px 16px 24px; display: flex; justify-content: center; gap: 12px; z-index: 10;">
        <div style="background: #0066FF; color: white; padding: 12px 24px; border-radius: 30px; font-weight: 800; font-size: 14px; box-shadow: 0 4px 12px rgba(0,102,255,0.3);">DEL ➔ BOM</div>
        <div style="background: rgba(255,255,255,0.8); color: #0f172a; padding: 12px 24px; border-radius: 30px; font-weight: 800; font-size: 14px; backdrop-filter: blur(10px);">BOM ➔ DEL</div>
    </div>
    
    <!-- Aeroplane Animation Area -->
    <div style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative;">
        
        <!-- Animated Plane -->
        <div id="seatLoadingPlane" style="position: relative; z-index: 5; transform: translateY(100px); opacity: 0; transition: all 2s cubic-bezier(0.25, 1, 0.5, 1);">
            <svg viewBox="0 0 400 400" width="280" height="280" style="filter: drop-shadow(0 20px 30px rgba(0,0,0,0.15));">
                <!-- Simple top-down airplane SVG -->
                <path d="M190 20 C190 10, 210 10, 210 20 L210 150 L380 250 L380 270 L210 220 L210 320 L260 360 L260 380 L200 360 L140 380 L140 360 L190 320 L190 220 L20 270 L20 250 L190 150 Z" fill="#0f172a" stroke="#ffffff" stroke-width="2"/>
                <path d="M200 15 L200 360" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>
            </svg>
        </div>
        
        <!-- Clouds background (static for prototype) -->
        <div style="position: absolute; top: 20%; left: 10%; width: 150px; height: 50px; background: rgba(255,255,255,0.6); border-radius: 50px; filter: blur(20px); z-index: 1;"></div>
        <div style="position: absolute; top: 40%; right: 10%; width: 200px; height: 80px; background: rgba(255,255,255,0.5); border-radius: 50px; filter: blur(30px); z-index: 1;"></div>
        
    </div>
    
    <!-- Footer Text -->
    <div style="padding-bottom: 60px; text-align: center; z-index: 10;">
        <div style="font-size: 16px; font-weight: 800; color: #0f172a;" id="seatLoadingDate">22 Jun 2026</div>
        <div style="font-size: 13px; font-weight: 600; color: #64748b; margin-top: 4px;">6E 2135 • Setting up BOEING 787 Seats...</div>
    </div>
</div>

<div class="screen" id="screenSeatMap" style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: #ffffff; z-index: 210; overflow: hidden;">
    
    <!-- Header Area -->
    <div style="flex-shrink: 0; background: #ffffff; border-bottom: 1px solid #f1f5f9; z-index: 50;">
        <!-- Top Nav Route -->
        <div style="display: flex; align-items: center; padding: 52px 24px 12px 24px;">
            <div class="back-btn-chevron" onclick="navigateTo('addons')" style="background: transparent; margin-right: 12px; width: 24px; height: 24px;">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#0f172a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="15 18 9 12 15 6"></polyline>
                </svg>
            </div>
            <div style="flex: 1;">
                <div style="font-size: 14px; font-weight: 800; color: #0f172a; display: flex; align-items: center; gap: 6px;">
                    DEL <span style="color: #94a3b8; font-size: 12px;">➔</span> BOM
                </div>
                <div style="font-size: 10px; color: #64748b; font-weight: 600;">07:30 - 09:45</div>
            </div>
            <div class="dev-trigger-btn" onclick="toggleSeatMap3DView()" id="btnToggleSeatView" style="margin: 0 12px 0 0; background: #f1f5f9; color: #0f172a; padding: 6px 12px; font-size: 11px;">
                Rotate
            </div>
            <div style="width: 20px; height: 20px; border: 1.5px solid #cbd5e1; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: #0f172a; font-size: 10px; font-weight: 800;">i</div>
        </div>
        
        <!-- Segment Tabs (Compact) -->
        <div style="display: flex; border-bottom: 1px solid #e2e8f0; height: 36px;">
            <div style="flex: 1; text-align: center; border-bottom: 2px solid #0066FF; font-size: 11px; font-weight: 800; color: #0f172a; display: flex; justify-content: center; align-items: center;">DEL ➔ BOM</div>
            <div style="flex: 1; text-align: center; color: #94a3b8; font-size: 11px; font-weight: 700; display: flex; justify-content: center; align-items: center;">BOM ➔ DEL</div>
        </div>
        
        <!-- Pax Selection Horizontal Scroll (Compact) -->
        <div style="padding: 10px 24px; display: flex; gap: 8px; overflow-x: auto; scrollbar-width: none;" id="seatMapPaxCartContainer">
            <!-- JS populated with passengers -->
        </div>
        
        <!-- Upfront Banner (Sleek) -->
        <div style="margin: 0 24px 10px 24px; background: #0b7a4d; border-radius: 8px; padding: 10px 12px; display: flex; align-items: center; justify-content: space-between; color: white;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="background: rgba(255,255,255,0.2); width: 24px; height: 24px; border-radius: 6px; display: flex; justify-content: center; align-items: center;">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
                </div>
                <div>
                    <div style="font-size: 12px; font-weight: 800;">IndiGo Upfront</div>
                    <div style="font-size: 9px; font-weight: 500; opacity: 0.9;">Priority boarding & meals</div>
                </div>
            </div>
            <button style="background: white; color: #0b7a4d; border: none; padding: 6px 12px; border-radius: 12px; font-size: 10px; font-weight: 800;">Upgrade</button>
        </div>
        
        <!-- Quick Filters & Legend (Combined) -->
        <div style="padding: 0 24px 10px 24px; display: flex; gap: 6px; border-bottom: 1px solid #f1f5f9; overflow-x: auto; scrollbar-width: none; align-items: center;">
            <!-- Filters -->
            <div style="padding: 4px 10px; border: 1px solid #e2e8f0; border-radius: 12px; font-size: 10px; font-weight: 700; color: #0f172a; display: flex; align-items: center; gap: 4px; flex-shrink: 0;"><svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg> Free seats</div>
            <div style="padding: 4px 10px; border: 1px solid #e2e8f0; border-radius: 12px; font-size: 10px; font-weight: 700; color: #0f172a; display: flex; align-items: center; gap: 4px; flex-shrink: 0;"><svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 3 21 3 21 9"></polyline><polyline points="9 21 3 21 3 15"></polyline><line x1="21" y1="3" x2="14" y2="10"></line><line x1="3" y1="21" x2="10" y2="14"></line></svg> Extra Legroom</div>
            <div style="padding: 4px 10px; border: 1px solid #e2e8f0; border-radius: 12px; font-size: 10px; font-weight: 700; color: #0f172a; display: flex; align-items: center; gap: 4px; flex-shrink: 0;"><svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="4" ry="4"></rect></svg> Window</div>
            
            <div style="width: 1px; height: 16px; background: #cbd5e1; margin: 0 4px; flex-shrink: 0;"></div>
            
            <!-- Legends -->
            <div style="display: flex; align-items: center; gap: 4px; font-size: 9px; font-weight: 700; color: #64748b; flex-shrink: 0;"><div style="width: 8px; height: 8px; border-radius: 2px; background: #e0e7ff; border: 1px solid #a5b4fc;"></div> Upfront</div>
            <div style="display: flex; align-items: center; gap: 4px; font-size: 9px; font-weight: 700; color: #64748b; flex-shrink: 0;"><div style="width: 8px; height: 8px; border-radius: 2px; background: #ffedd5; border: 1px solid #fdba74;"></div> Emergency XL</div>
        </div>
    </div>

    <!-- Map Area (Pan/Zoom Container) -->
    <div id="seatMapPanZoomArea" style="flex: 1; min-height: 0; overflow: hidden; background: #ffffff; position: relative;">
        
        <!-- The transforming layer for Pan/Zoom -->
        <div id="seatMapTransformContainer" style="width: 100%; height: 100%; transform-origin: top center; transition: transform 0.1s; will-change: transform; overflow: visible; padding: 20px 0 150px 0; touch-action: none;">
            
            <!-- Wing overlays inside pan area for smooth scrolling -->
            <div class="top-down-fuselage is-3d-vertical" id="seatMapFuselage">
                <div class="top-down-nose"></div>
                
                <div class="seat-grid" id="seatMapGrid">
                    <!-- Javascript will populate rows here -->
                </div>
                
                <div class="top-down-tail"></div>
            </div>
            
            <!-- Sit Together Guarantee (Compact) -->
            <div style="margin: 24px auto; width: 280px; padding: 12px; border: 1px dashed #cbd5e1; border-radius: 12px; display: flex; gap: 12px; align-items: center; background: #f8fafc; position: relative;">
                <div style="background: #e0f2fe; width: 32px; height: 32px; border-radius: 50%; display: flex; justify-content: center; align-items: center; flex-shrink: 0;">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#0066FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>
                </div>
                <div style="flex: 1;">
                    <div style="font-size: 12px; font-weight: 800; color: #0f172a;">Sit Together Guarantee</div>
                    <div style="font-size: 10px; font-weight: 600; color: #64748b; margin-top: 2px;">Rows 14-16 recommended</div>
                </div>
                <button style="background: #0066FF; color: white; border: none; padding: 6px 16px; border-radius: 20px; font-size: 10px; font-weight: 800;">Book</button>
            </div>
            
        </div>
    </div>
    
    <!-- Sticky Footer -->
    <div style="flex-shrink: 0; background: #ffffff; border-top: 1px solid rgba(0,0,0,0.05); padding: 12px 24px 30px 24px; z-index: 50; display: flex; flex-direction: column;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div style="display: flex; gap: -8px;" id="seatMapBottomIndicators">
                <!-- R, A circles -->
            </div>
            <div style="text-align: right;">
                <div style="font-size: 10px; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">SUBTOTAL</div>
                <div style="font-size: 20px; font-weight: 900; color: #0066FF;" id="seatMapSelectedSeatPrice">₹1,200</div>
            </div>
        </div>
        <div style="display: flex; gap: 12px;">
            <button style="flex: 1; padding: 12px 0; border-radius: 12px; background: #ffffff; border: 1px solid #cbd5e1; font-size: 13px; font-weight: 800; color: #64748b;" onclick="navigateTo('addons')">Skip Selection</button>
            <button style="flex: 2; padding: 12px 0; border-radius: 12px; background: #0066FF; color: white; border: none; font-size: 13px; font-weight: 800; box-shadow: 0 4px 12px rgba(0,102,255,0.3);" onclick="confirmSeatSelection()">Continue</button>
        </div>
    </div>
</div>
"""

start_str = '<div class="screen" id="screenSeatMap"'
end_str = '<!-- Map Area (Top-Down 3D View) -->'

start_idx = content.find(start_str)

if start_idx != -1:
    end_of_screen = content.find('</div>\n</div>', start_idx) + 12
    if end_of_screen != -1:
        final_content = content[:start_idx] + new_html + content[end_of_screen:]
        with open('index.html', 'w') as f:
            f.write(final_content)
        print("HTML updated successfully")
else:
    print("Could not find start idx")
