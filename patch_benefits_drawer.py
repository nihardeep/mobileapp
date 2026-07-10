import re

with open('index.html', 'r') as f:
    html = f.read()

drawer_html = """                <!-- Addon Benefits Drawer -->
                <div class="bottom-sheet-drawer" id="addonBenefitsDrawer" style="z-index: 9999; padding-bottom: 20px;">
                    <div class="drawer-drag-handle" style="width: 36px; height: 4px; background: #cbd5e1; border-radius: 2px; margin: 12px auto 20px auto;"></div>
                    <div style="padding: 0 24px 32px 24px;">
                        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 24px;">
                            <h2 style="font-size: 20px; font-weight: 900; color: #001B94; font-style: italic; margin: 0;">UpFront Benefits</h2>
                        </div>
                        <div style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 32px;">
                            <div style="display: flex; align-items: flex-start; gap: 12px;">
                                <div style="font-size: 20px;">💺</div>
                                <div>
                                    <div style="font-size: 14px; font-weight: 800; color: #0f172a;">Premium Seat Selection</div>
                                    <div style="font-size: 12px; color: #64748b;">Free seat selection including XL seats</div>
                                </div>
                            </div>
                            <div style="display: flex; align-items: flex-start; gap: 12px;">
                                <div style="font-size: 20px;">🍲</div>
                                <div>
                                    <div style="font-size: 14px; font-weight: 800; color: #0f172a;">Hot Meal Included</div>
                                    <div style="font-size: 12px; color: #64748b;">Enjoy a complimentary hot meal on board</div>
                                </div>
                            </div>
                            <div style="display: flex; align-items: flex-start; gap: 12px;">
                                <div style="font-size: 20px;">⚡</div>
                                <div>
                                    <div style="font-size: 14px; font-weight: 800; color: #0f172a;">Priority Boarding</div>
                                    <div style="font-size: 12px; color: #64748b;">Skip the queue and board first</div>
                                </div>
                            </div>
                        </div>
                        <button class="primary-btn" style="width: 100%; padding: 16px; border-radius: 12px; font-size: 16px; font-weight: 800; background: #001B94; color: white; border: none;" onclick="closeAllDrawers()">Got it</button>
                    </div>
                </div>
"""

# Insert right after savedPassengersSheet
if 'id="savedPassengersSheet"' in html:
    # Find the end of savedPassengersSheet div roughly by looking for the next drawer
    html = html.replace('<!-- Bank Offer Sheet -->', drawer_html + '\n                <!-- Bank Offer Sheet -->')
    
with open('index.html', 'w') as f:
    f.write(html)
