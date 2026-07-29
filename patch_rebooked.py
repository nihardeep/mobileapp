import re

with open('app.js', 'r') as f:
    js = f.read()

target = """            <div style="font-size: 11px; font-weight: 700; color: #ef4444; margin-bottom: 8px;">Auto Rebooked For You</div>
            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 16px;">
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: #1e293b; margin-bottom: 4px;">LKO ➔ LON</div>
                    <div style="font-size: 11px; color: #64748b;">25 Jun, 10:30 | Terminal 1</div>
                    <div style="font-size: 11px; font-weight: 700; color: #1e293b; margin-top: 4px;">XAir 1522</div>
                </div>
                <div style="font-size: 11px; font-weight: 700; color: #005eb8; cursor: pointer;">View details</div>
            </div>"""

replacement = """            <div style="font-size: 12px; font-weight: 800; color: #ef4444; margin-bottom: 12px; margin-top: 24px; display: flex; align-items: center; gap: 6px;">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg>
                Auto Rebooked For You
            </div>
            
            <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px dashed #cbd5e1; padding-bottom: 12px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="width: 24px; height: 24px; background: #f1f5f9; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 800; color: #001B94;">XA</div>
                        <div style="font-size: 12px; font-weight: 800; color: #0f172a;">XAir 1522</div>
                    </div>
                    <div style="font-size: 11px; font-weight: 700; color: #005eb8; cursor: pointer; display: flex; align-items: center; gap: 2px;">
                        View details
                        <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 18px; font-weight: 900; color: #0f172a;">10:30</div>
                        <div style="font-size: 13px; font-weight: 800; color: #005eb8; margin-top: 2px;">LKO <span style="font-size: 10px; color: #64748b; font-weight: 600;">T1</span></div>
                        <div style="font-size: 11px; color: #64748b; font-weight: 600; margin-top: 4px;">25 Jun</div>
                    </div>
                    
                    <div style="display: flex; flex-direction: column; align-items: center; flex: 1; margin: 0 16px;">
                        <div style="font-size: 9px; font-weight: 700; color: #64748b; margin-bottom: 6px; letter-spacing: 0.5px;">12H 00M</div>
                        <div style="width: 100%; height: 1.5px; background: #cbd5e1; position: relative; display: flex; align-items: center; justify-content: center;">
                            <svg viewBox="0 0 24 24" width="12" height="12" fill="#94a3b8" style="background: #fff; padding: 0 4px;"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg>
                        </div>
                        <div style="font-size: 9px; font-weight: 800; color: #10b981; margin-top: 6px; background: #ecfdf5; padding: 2px 6px; border-radius: 4px; text-transform: uppercase;">Confirmed</div>
                    </div>
                    
                    <div style="text-align: right;">
                        <div style="font-size: 18px; font-weight: 900; color: #0f172a;">22:30</div>
                        <div style="font-size: 13px; font-weight: 800; color: #005eb8; margin-top: 2px;">LON <span style="font-size: 10px; color: #64748b; font-weight: 600;">T3</span></div>
                        <div style="font-size: 11px; color: #64748b; font-weight: 600; margin-top: 4px;">25 Jun</div>
                    </div>
                </div>
            </div>"""

if target in js:
    js = js.replace(target, replacement)
    with open('app.js', 'w') as f:
        f.write(js)
    print("Rebooked UI patched successfully")
else:
    print("WARNING: target not found")

