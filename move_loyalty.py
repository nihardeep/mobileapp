import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Make loyalUserCard visible
    html = html.replace(
        '<div class="bluchip-3d-wrapper" id="loyalUserCard" style="position: relative; perspective: 1500px; margin-bottom: 24px; display: none;">',
        '<div class="bluchip-3d-wrapper" id="loyalUserCard" style="position: relative; perspective: 1500px; margin-bottom: 24px;">'
    )

    # 2. Extract newUserCard
    # We will use string finding because regex on HTML can be tricky.
    start_str = '                                <!-- STATE 2: NEW USER (Zero Balance) -->\n                                <div class="bluchip-3d-wrapper" id="newUserCard"'
    
    start_idx = html.find(start_str)
    if start_idx == -1:
        print("Could not find newUserCard start")
        return
        
    # Find the closing div of newUserCard. We can count divs or just find the exact end based on line 1228.
    # Looking at the snippet:
    # 1226:                                         </div>
    # 1227:                                     </div>
    # 1228:                                 </div>
    # 1229:                             </div>
    end_str = '                                    </div>\n                                </div>\n'
    
    # We need to find the specific end. Let's just find the start of the next section:
    # `                            <!-- Offers Carousel (Not business as usual slides) -->`
    next_section_idx = html.find('                            <!-- Offers Carousel (Not business as usual slides) -->', start_idx)
    
    if next_section_idx == -1:
        print("Could not find next section")
        return
        
    # The end of the newUserCard block is right before `</div>` that closes `loyaltySection`
    
    # Let's find the closing div of loyaltySection
    # which is `                            </div>\n                            \n                            <!-- Offers Carousel`
    end_idx = html.rfind('                            </div>', start_idx, next_section_idx)
    
    new_user_card_html = html[start_idx:end_idx]
    
    # Remove it from the original place
    html = html[:start_idx] + html[end_idx:]
    
    # Wrap it in a drawer
    drawer_html = f'''
<!-- Profile Drawer -->
<div class="bottom-sheet-drawer" id="profileDrawer" style="z-index: 999999; padding-bottom: 20px; padding-left: 16px; padding-right: 16px;">
    <div class="drawer-drag-handle" style="width: 36px; height: 4px; background: #cbd5e1; border-radius: 2px; margin: 12px auto 20px auto;"></div>
    <div style="font-size: 20px; font-weight: 800; margin-bottom: 16px; color: #0f172a;">Your Profile</div>
{new_user_card_html}
</div>
'''

    # Insert the drawer right before bottomSheetBackdrop
    backdrop_idx = html.find('<div class="bottom-sheet-backdrop" id="bottomSheetBackdrop"')
    if backdrop_idx != -1:
        html = html[:backdrop_idx] + drawer_html + html[backdrop_idx:]
    else:
        print("Could not find bottomSheetBackdrop")
        return

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    # Now update app.js toggleLoyaltyState
    with open('app.js', 'r', encoding='utf-8') as f:
        js = f.read()
        
    old_func = '''function toggleLoyaltyState() {
    const loyalCard = document.getElementById('loyalUserCard');
    const newCard = document.getElementById('newUserCard');
    
    if (loyalCard.style.display !== 'none') {
        // Switch to New User Flow
        loyalCard.style.display = 'none';
        newCard.style.display = 'block';
    } else {
        // Switch to Loyal User Flow
        loyalCard.style.display = 'block';
        newCard.style.display = 'none';
    }
}'''

    new_func = '''function toggleLoyaltyState() {
    let drawer = document.getElementById('profileDrawer');
    let backdrop = document.getElementById('bottomSheetBackdrop');
    if(drawer) {
        drawer.classList.add('active');
        if (backdrop) backdrop.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}'''

    if old_func in js:
        js = js.replace(old_func, new_func)
    else:
        print("Could not find old toggleLoyaltyState function in app.js")

    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(js)
        
    print("Success")

if __name__ == "__main__":
    main()
