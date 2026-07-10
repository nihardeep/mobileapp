import re

with open('index.html', 'r') as f:
    html = f.read()

target_start_str = '<div class="bluchip-bottom-layout">'
target_start = html.find(target_start_str, html.find('id="loyalUserCard"'))

if target_start != -1:
    target_end = html.find('                                </div>\n\n                                <!-- ========================================================= -->\n                                <!-- ========================================================= -->\n                                <!-- STATE 2: NEW USER (Zero Balance) -->', target_start)
    if target_end != -1:
        replacement = """<div class="bluchip-bottom-layout" style="display: block; padding-top: 12px;">
                                        <div class="partners-scroll-container" style="background: #F4F5F7; border-radius: 12px; padding: 16px; box-shadow: inset 0 2px 4px rgba(255,255,255,0.1);">
                                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                                <span style="font-size: 13px; font-weight: 600; color: #000; letter-spacing: 0.5px;">OUR POPULAR PARTNERS</span>
                                                <span style="font-size: 14px; font-weight: 600; color: #001A70; text-decoration: underline; cursor: pointer;" onclick="event.stopPropagation(); alert('View all partners')">View all <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-left: 2px;"><polyline points="9 18 15 12 9 6"></polyline></svg></span>
                                            </div>
                                            
                                            <div class="partners-scroll-track" style="display: flex; overflow-x: auto; gap: 10px; padding-bottom: 4px; scroll-snap-type: x mandatory; -webkit-overflow-scrolling: touch;">
                                                
                                                <!-- SBI Card -->
                                                <div class="partner-box" style="flex: 0 0 auto; width: 140px; height: 68px; background: #000; border-radius: 12px; display: flex; align-items: center; justify-content: center; scroll-snap-align: start;" onclick="event.stopPropagation(); triggerHaptic('light', 'Partner clicked');">
                                                    <div style="display: flex; align-items: center; gap: 6px;">
                                                        <svg width="24" height="24" viewBox="0 0 100 100">
                                                            <circle cx="50" cy="50" r="48" fill="#00A1E4" />
                                                            <circle cx="50" cy="50" r="18" fill="#000" />
                                                            <rect x="42" y="50" width="16" height="35" fill="#000" />
                                                        </svg>
                                                        <span style="font-family: sans-serif; font-size: 18px; font-weight: 700;">
                                                            <span style="color: #fff; letter-spacing: -0.5px;">SBI</span> <span style="color: #00A1E4; font-weight: 400; letter-spacing: -0.5px;">card</span>
                                                        </span>
                                                    </div>
                                                </div>

                                                <!-- Swiggy -->
                                                <div class="partner-box" style="flex: 0 0 auto; width: 110px; height: 68px; background: #000; border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; scroll-snap-align: start;" onclick="event.stopPropagation(); triggerHaptic('light', 'Partner clicked');">
                                                    <div style="background: #FC8019; width: 28px; height: 28px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 4px;">
                                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="#fff">
                                                            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm-1 9c-1.1 0-2-.9-2-2s.9-2 2-2h2c.55 0 1 .45 1 1v1c0 .55-.45 1-1 1h-1v1h2v1h-3z"/>
                                                        </svg>
                                                    </div>
                                                    <span style="color: #FC8019; font-weight: 700; font-size: 14px; letter-spacing: -0.5px;">Swiggy</span>
                                                </div>

                                                <!-- Kotak -->
                                                <div class="partner-box" style="flex: 0 0 auto; width: 140px; height: 68px; background: #000; border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; scroll-snap-align: start;" onclick="event.stopPropagation(); triggerHaptic('light', 'Partner clicked');">
                                                    <div style="display: flex; align-items: center; gap: 4px; margin-bottom: 2px;">
                                                        <div style="width: 24px; height: 24px; background: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; position: relative;">
                                                             <svg width="18" height="10" viewBox="0 0 30 14" fill="none" stroke="#000" stroke-width="3">
                                                                <circle cx="8" cy="7" r="5" />
                                                                <circle cx="22" cy="7" r="5" />
                                                             </svg>
                                                             <div style="position: absolute; left: 9px; top: 7px; width: 2.5px; height: 11px; background: #000; transform: rotate(45deg);"></div>
                                                        </div>
                                                        <span style="color: #fff; font-weight: 700; font-size: 18px; letter-spacing: -0.5px;">kotak</span>
                                                    </div>
                                                    <span style="color: #ccc; font-size: 9px;">Kotak Mahindra B...</span>
                                                </div>

                                            </div>
                                        </div>
"""
        html = html[:target_start] + replacement + html[target_end:]
        with open('index.html', 'w') as f:
            f.write(html)
        print("Successfully replaced bluchip-bottom-layout.")
    else:
        print("End target not found!")
else:
    print("Start target not found!")

