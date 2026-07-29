import re

with open('app.js', 'r') as f:
    js = f.read()

# Remove the vertical timeline injection from updateTimelineState
target_vert = """    } else if (state === 'connection_risk') {
        return container.innerHTML = `
            <div style="padding: 16px; background: #fff8f1; border-bottom: 1px solid rgba(249, 115, 22, 0.1);">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                    <div style="font-size: 20px;">⚠️</div>
                    <div>
                        <div style="font-size: 14px; font-weight: 800; color: #c2410c;">Connection at risk!</div>
                        <div style="font-size: 11px; color: #ea580c; font-weight: 600;">You have 55 min to reach your next gate</div>
                    </div>
                </div>
                <div style="display: flex; gap: 16px; align-items: stretch; position: relative; margin-top: 24px;">
                    <div style="width: 2px; background: #e2e8f0; position: absolute; left: 11px; top: 12px; bottom: 12px; z-index: 0;"></div>
                    <div style="display: flex; flex-direction: column; gap: 24px; width: 100%; position: relative; z-index: 1;">
                        <div style="display: flex; align-items: flex-start; gap: 12px;">
                            <div style="width: 24px; height: 24px; border-radius: 50%; background: #fff; border: 2px solid #eab308; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"><div style="width: 8px; height: 8px; border-radius: 50%; background: #eab308;"></div></div>
                            <div style="flex: 1; display: flex; justify-content: space-between; align-items: center;">
                                <div><div style="font-size: 13px; font-weight: 700; color: #334155;">Arriving at DEL</div><div style="font-size: 11px; color: #10b981; font-weight: 600;">On time</div></div>
                                <div style="font-size: 11px; font-weight: 700; color: #334155;">09:15</div>
                            </div>
                        </div>
                        <div style="display: flex; align-items: flex-start; gap: 12px;">
                            <div style="width: 24px; height: 24px; border-radius: 50%; background: #fff; border: 2px solid #f97316; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"><div style="width: 8px; height: 8px; border-radius: 50%; background: #f97316;"></div></div>
                            <div style="flex: 1; display: flex; justify-content: space-between; align-items: center;">
                                <div><div style="font-size: 13px; font-weight: 700; color: #334155;">Layover at DEL</div><div style="font-size: 11px; color: #64748b; font-weight: 500;">Terminal 2 ➔ T1</div></div>
                                <div style="font-size: 11px; font-weight: 700; color: #10b981; background: #ecfdf5; padding: 2px 6px; border-radius: 12px;">1h 45m</div>
                            </div>
                        </div>
                        <div style="display: flex; align-items: flex-start; gap: 12px;">
                            <div style="width: 24px; height: 24px; border-radius: 50%; background: #fff; border: 2px solid #ef4444; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"><div style="width: 8px; height: 8px; border-radius: 50%; background: #ef4444;"></div></div>
                            <div style="flex: 1; display: flex; justify-content: space-between; align-items: center;">
                                <div><div style="font-size: 13px; font-weight: 700; color: #334155;">Next: Depart DEL</div><div style="font-size: 11px; color: #64748b; font-weight: 500;">10:10</div></div>
                                <div style="font-size: 11px; font-weight: 700; color: #ef4444;">Gate 32</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>`;"""

replacement_vert = """    } else if (state === 'connection_risk') {
        return container.innerHTML = ''; """

if target_vert in js:
    js = js.replace(target_vert, replacement_vert)
else:
    print("WARNING: target_vert not found")

# Replace renderFlightStateCard for connection_risk
target_card = """    } else if (state === 'connection_risk') {
        html = `
            <div style="background: #fdf2f8; padding: 12px; border-radius: 12px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between; margin-top: 8px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: #db2777; font-size: 16px;">❤️</span>
                    <div>
                        <div style="font-size: 12px; font-weight: 700; color: #1e293b;">We've informed the gate</div>
                        <div style="font-size: 10px; color: #64748b; font-weight: 500;">Priority boarding for you</div>
                    </div>
                </div>
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#db2777" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
            </div>
            <button class="btn-primary-action" style="width: 100%; justify-content: center; background: transparent; border: 1px solid #ef4444; color: #ef4444;" onclick="triggerHaptic('medium', 'Directions')">Step-by-step directions</button>
        `;"""

replacement_card = """    } else if (state === 'connection_risk') {
        html = `
            <div style="background: #fff8f1; border-radius: 16px; padding: 16px; margin-top: -10px; margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <div>
                        <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
                            <span style="font-size: 16px; color: #ea580c;">⚠️</span>
                            <span style="font-size: 15px; font-weight: 800; color: #c2410c;">Connection at risk!</span>
                        </div>
                        <div style="font-size: 11px; font-weight: 600; color: #1e293b; margin-bottom: 8px; margin-left: 26px;">You have 55 min to reach<br>your next gate</div>
                        <div style="display: flex; align-items: center; gap: 4px; margin-left: 26px;">
                            <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="#ea580c" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                            <span style="font-size: 10px; font-weight: 700; color: #475569;">Run time: 8 min</span>
                        </div>
                    </div>
                    <!-- Running Person Animation -->
                    <div style="margin-right: 8px;">
                        <svg class="running-risk" style="animation: runningUrgency 0.6s infinite alternate;" viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="#ea580c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="5" r="2" fill="#1e293b" stroke="#1e293b"></circle>
                            <path d="M12 7 L12 13" stroke="#ea580c" stroke-width="4"></path>
                            <path d="M12 9 L8 11 L6 8" stroke="#ea580c" stroke-width="3"></path>
                            <path d="M12 9 L15 11 L18 10" stroke="#ea580c" stroke-width="3"></path>
                            <path d="M12 13 L10 18 L12 21" stroke="#1e293b" stroke-width="3"></path>
                            <path d="M12 13 L15 16 L17 14" stroke="#1e293b" stroke-width="3"></path>
                        </svg>
                    </div>
                </div>

                <div style="display: flex; gap: 16px; align-items: stretch; position: relative;">
                    <div style="width: 2px; background: #cbd5e1; position: absolute; left: 11px; top: 12px; bottom: 12px; z-index: 0;"></div>
                    <div style="display: flex; flex-direction: column; gap: 24px; width: 100%; position: relative; z-index: 1;">
                        <div style="display: flex; align-items: flex-start; gap: 12px;">
                            <div style="width: 24px; height: 24px; border-radius: 50%; background: #fff; border: 2px solid #eab308; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"><div style="width: 8px; height: 8px; border-radius: 50%; background: #eab308;"></div></div>
                            <div style="flex: 1; display: flex; justify-content: space-between; align-items: flex-start;">
                                <div><div style="font-size: 13px; font-weight: 700; color: #1e293b; margin-bottom: 4px;">Arriving at BOM</div><div style="font-size: 11px; color: #10b981; font-weight: 700; background: #ecfdf5; padding: 2px 8px; border-radius: 12px; display: inline-block;">On time</div></div>
                                <div style="text-align: right;"><div style="font-size: 11px; font-weight: 800; color: #1e293b;">09:15</div><div style="font-size: 11px; font-weight: 800; color: #1e293b; margin-top: 4px;">09:15</div></div>
                            </div>
                        </div>
                        <div style="display: flex; align-items: flex-start; gap: 12px;">
                            <div style="width: 24px; height: 24px; border-radius: 50%; background: #fff; border: 2px solid #ea580c; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"><div style="width: 8px; height: 8px; border-radius: 50%; background: #ea580c;"></div></div>
                            <div style="flex: 1; display: flex; justify-content: space-between; align-items: flex-start;">
                                <div><div style="font-size: 13px; font-weight: 700; color: #1e293b; margin-bottom: 2px;">Layover at BOM</div><div style="font-size: 11px; color: #475569; font-weight: 600;">Terminal 2 ➔ T1</div></div>
                                <div style="font-size: 11px; font-weight: 800; color: #10b981; background: #ecfdf5; padding: 4px 8px; border-radius: 12px;">1h 45m</div>
                            </div>
                        </div>
                        <div style="display: flex; align-items: flex-start; gap: 12px;">
                            <div style="width: 24px; height: 24px; border-radius: 50%; background: #fff; border: 2px solid #ef4444; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"><div style="width: 8px; height: 8px; border-radius: 50%; background: #ef4444;"></div></div>
                            <div style="flex: 1; display: flex; justify-content: space-between; align-items: flex-start;">
                                <div><div style="font-size: 13px; font-weight: 700; color: #1e293b; margin-bottom: 2px;">Next: Depart BOM</div><div style="font-size: 12px; color: #1e293b; font-weight: 700;">10:10</div></div>
                                <div style="font-size: 11px; font-weight: 800; color: #ef4444; background: #fef2f2; padding: 4px 8px; border-radius: 12px;">Gate 32</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div style="background: #fdf2f8; padding: 12px 16px; border-radius: 12px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="color: #ef4444; font-size: 18px;">❤️</span>
                    <div>
                        <div style="font-size: 13px; font-weight: 800; color: #1e293b; margin-bottom: 2px;">We've informed the gate</div>
                        <div style="font-size: 11px; color: #64748b; font-weight: 600;">Priority boarding for you</div>
                    </div>
                </div>
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#ef4444" stroke-width="3"><polyline points="6 9 12 15 18 9"></polyline></svg>
            </div>
            
            <button class="btn-primary-action" style="width: 100%; justify-content: center; background: transparent; border: 1.5px solid #ef4444; color: #ef4444; font-weight: 800; font-size: 13px;" onclick="triggerHaptic('medium', 'Directions')">Step-by-step directions</button>
        `;"""

if target_card in js:
    js = js.replace(target_card, replacement_card)
else:
    print("WARNING: target_card not found")


# Hide standard horizontal timeline logic
hide_logic = """    if (state === 'upcoming_trip') {
        if (header) header.style.display = 'none';
        if (drawer) drawer.style.display = 'none';
        return;
    } else {"""

hide_logic_new = """    if (['upcoming_trip', 'connection_risk', 'missed_flight'].includes(state)) {
        if (header) header.style.display = 'none';
        if (drawer) drawer.style.display = 'none';
        if (state === 'upcoming_trip') return; // Exit for upcoming trip, but risk/missed still need state setting internally
    } else {"""

js = js.replace(hide_logic, hide_logic_new)

with open('app.js', 'w') as f:
    f.write(js)
print("app.js patched successfully")
