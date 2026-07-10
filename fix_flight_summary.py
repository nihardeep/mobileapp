import re

with open('index.html', 'r') as f:
    html = f.read()

old_snippet = """                        <!-- Flight Info Snippet -->
                        <div class="neo-card" style="margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; padding: 16px;">
                            <div>
                                <div style="font-size: 12px; color: #64748b; font-weight: 600; margin-bottom: 4px;">Flight Summary</div>
                                <div style="font-size: 16px; font-weight: 800; color: #0f172a;">DEL → BOM</div>
                                <div style="font-size: 12px; color: #64748b;">3 Adults, 1 Child • <span id="passenger-fare-type" style="color: var(--indigo-blue); font-weight: 700;">Saver</span></div>
                            </div>
                            <div style="font-size: 12px; color: var(--indigo-blue); font-weight: 700;">View details ></div>
                        </div>"""

new_snippet = """                        <!-- Flight Info Snippet -->
                        <div style="margin-bottom: 24px; background: linear-gradient(135deg, rgba(255,255,255,0.8), rgba(255,255,255,0.4)); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.5); border-radius: 16px; padding: 16px; box-shadow: 0 8px 32px rgba(31, 38, 135, 0.05); position: relative; overflow: hidden;">
                            <div style="position: absolute; top: -20px; right: -20px; width: 100px; height: 100px; background: var(--indigo-blue); opacity: 0.05; border-radius: 50%;"></div>
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                                <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: var(--indigo-blue); font-weight: 800;">Flight Summary</div>
                                <div style="font-size: 12px; color: var(--indigo-blue); font-weight: 700; cursor: pointer; background: #fff; padding: 4px 8px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">View details ></div>
                            </div>
                            
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                                <div>
                                    <div style="font-size: 20px; font-weight: 800; color: #0f172a;">DEL</div>
                                    <div style="font-size: 11px; color: #64748b; font-weight: 600;">05:00</div>
                                </div>
                                <div style="flex: 1; display: flex; flex-direction: column; align-items: center; padding: 0 16px;">
                                    <div style="font-size: 10px; color: #64748b; margin-bottom: 4px;">2h 10m</div>
                                    <div style="width: 100%; height: 2px; background: #cbd5e1; position: relative;">
                                        <div style="position: absolute; top: -6px; left: 50%; transform: translateX(-50%); background: #E6EAF0; padding: 0 4px;">
                                            <svg viewBox="0 0 24 24" width="14" height="14" fill="var(--indigo-blue)"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg>
                                        </div>
                                    </div>
                                    <div style="font-size: 10px; color: #64748b; margin-top: 4px;">Non-stop</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-size: 20px; font-weight: 800; color: #0f172a;">BOM</div>
                                    <div style="font-size: 11px; color: #64748b; font-weight: 600;">08:10</div>
                                </div>
                            </div>
                            
                            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px dashed rgba(203, 213, 225, 0.5); padding-top: 12px; margin-top: 4px;">
                                <div style="font-size: 11px; color: #64748b; font-weight: 600;">3 Adults, 1 Child</div>
                                <div style="background: rgba(14,165,233,0.1); padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 800; color: var(--indigo-blue);">
                                    <span id="passenger-fare-type">Saver</span> Fare
                                </div>
                            </div>
                        </div>"""

html = html.replace(old_snippet, new_snippet)

with open('index.html', 'w') as f:
    f.write(html)
