import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update marquee items
sbi_old = '<div class="marquee-item"><span class="m-icon">🏦</span> <strong>SBI Bank:</strong> Get upto 15% off on flight booking</div>'
sbi_new = '<div class="marquee-item" style="cursor: pointer;" onclick="openBankOffer(\'SBIFLIGHT\', \'SBI Bank: Get upto 15% off on flight booking\')"><span class="m-icon">🏦</span> <strong>SBI Bank:</strong> Get upto 15% off on flight booking</div>'

axis_old = '<div class="marquee-item"><span class="m-icon">💳</span> <strong>AXIS BANK Debit card:</strong> Get upto 20% off on flight booking</div>'
axis_new = '<div class="marquee-item" style="cursor: pointer;" onclick="openBankOffer(\'AXIS20\', \'AXIS BANK Debit card: Get upto 20% off on flight booking\')"><span class="m-icon">💳</span> <strong>AXIS BANK Debit card:</strong> Get upto 20% off on flight booking</div>'

mobi_old = '<div class="marquee-item"><span class="m-icon">📱</span> <strong>MobiKwik:</strong> Get upto 10% cashback</div>'
mobi_new = '<div class="marquee-item" style="cursor: pointer;" onclick="openBankOffer(\'MOBI10\', \'MobiKwik: Get upto 10% cashback\')"><span class="m-icon">📱</span> <strong>MobiKwik:</strong> Get upto 10% cashback</div>'

html = html.replace(sbi_old, sbi_new)
html = html.replace(axis_old, axis_new)
html = html.replace(mobi_old, mobi_new)


bank_offer_drawer_html = """
                <!-- Bank Offer Sheet -->
                <div class="bottom-sheet-drawer" id="bankOfferDrawer">
                    <div class="drawer-drag-handle" style="width: 36px; height: 4px; background: #E0E0E0; border-radius: 2px; margin: 12px auto 20px auto;"></div>
                    
                    <div style="padding: 0 24px 32px 24px;">
                        <h2 id="bankOfferSheetTitle" style="font-size: 22px; font-weight: 800; color: #000; margin: 0 0 12px 0;">SBIFLIGHT</h2>
                        <p id="bankOfferSheetDesc" style="font-size: 14px; color: #333; margin: 0 0 24px 0; line-height: 1.4;">Get upto 15% off on flight booking</p>
                        
                        <div style="display: flex; align-items: center; justify-content: space-between; background: #F8FAFC; border-radius: 12px; padding: 12px 16px;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="width: 32px; height: 32px; background: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(0,0,0,0.05); color: #8A2B60; font-weight: bold; border: 1px solid #eee;">₹</div>
                                <div id="bankOfferSheetCode" style="font-size: 16px; font-weight: 600; color: #000; letter-spacing: 0.5px;">SBIFLIGHT</div>
                            </div>
                            <button onclick="copyBankOffer()" style="background: #fff; border: 1px solid #E2E8F0; border-radius: 6px; padding: 6px 12px; color: #0EA5E9; font-size: 12px; font-weight: 600; display: flex; align-items: center; gap: 6px; cursor: pointer;">
                                copy code
                                <svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" fill="none" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                            </button>
                        </div>
                        
                        <div style="display: flex; flex-direction: column; align-items: center; margin-top: 24px;">
                            <div style="display: flex; gap: 6px; margin-bottom: 8px;">
                                <div style="width: 20px; height: 6px; border-radius: 3px; background: #888;"></div>
                                <div style="width: 6px; height: 6px; border-radius: 3px; background: #D1D5DB;"></div>
                                <div style="width: 6px; height: 6px; border-radius: 3px; background: #D1D5DB;"></div>
                                <div style="width: 6px; height: 6px; border-radius: 3px; background: #D1D5DB;"></div>
                                <div style="width: 6px; height: 6px; border-radius: 3px; background: #D1D5DB;"></div>
                            </div>
                            <div style="font-size: 12px; color: #000; font-weight: 500;">1/5</div>
                        </div>
                    </div>
                </div>
"""

# Only add if it doesn't already exist
if 'id="bankOfferDrawer"' not in html:
    # Insert safely right before the backdrop ends
    backdrop_end = '<div class="bottom-sheet-backdrop" id="bottomSheetBackdrop" onclick="closeAllDrawers()"></div>'
    html = html.replace(backdrop_end, backdrop_end + '\n\n' + bank_offer_drawer_html)

with open('index.html', 'w') as f:
    f.write(html)

print("Marquee interaction added safely inside iphone-screen!")
