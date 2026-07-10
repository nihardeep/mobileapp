import re

with open('app.js', 'r') as f:
    content = f.read()

# Add the new JS functions at the end of the file
new_functions = """
// ==========================================================================
// UPFRONT UNLOCK FLOW (Option B)
// ==========================================================================
window.appState = window.appState || {};

function unlockUpfrontPerks(btn) {
    // 1. Show Toast
    if(typeof showToast === 'function') {
        showToast('🎉 Upgraded to IndiGo Upfront!');
    }
    
    // 2. Button State Change
    if (btn) {
        btn.innerHTML = 'Upgraded <span style="font-size: 14px; margin-left: 4px;">✅</span>';
        btn.style.background = '#e0f2fe';
        btn.style.color = '#0284c7';
        btn.onclick = null;
    }
    
    // 3. Inject "Claim your Perks" section right below PNR card
    const pnrCard = document.querySelector('.pnr-main-card');
    if (!pnrCard) return;
    
    // Remove if already exists
    const existing = document.getElementById('upfrontPerksSection');
    if (existing) existing.remove();
    
    const perksHtml = `
        <div id="upfrontPerksSection" style="margin-top: 16px; margin-bottom: 24px; animation: slideDown 0.4s ease-out forwards; padding: 0 16px;">
            <div style="font-size: 13px; font-weight: 800; color: #001B94; margin-bottom: 12px; letter-spacing: 0.5px; text-transform: uppercase; display: flex; align-items: center; gap: 6px;">
                <div style="width: 8px; height: 8px; background: #3b82f6; border-radius: 50%; box-shadow: 0 0 0 3px rgba(59,130,246,0.2); animation: pulseDot 2s infinite;"></div>
                Action Required: Claim Perks
            </div>
            
            <div style="display: flex; gap: 12px; overflow-x: auto; scrollbar-width: none; padding-bottom: 8px; margin-left: -16px; padding-left: 16px; padding-right: 16px;">
                <!-- Meal Card -->
                <div onclick="navigateToAddonsAndMakeFree('meals')" style="flex: 0 0 160px; background: #fff; border-radius: 16px; padding: 14px; border: 2px solid #3b82f6; box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15); cursor: pointer; position: relative; overflow: hidden; transition: transform 0.2s;">
                    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, #3b82f6, #0ea5e9);"></div>
                    <div style="font-size: 28px; margin-bottom: 12px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));">🍲</div>
                    <div style="font-size: 15px; font-weight: 800; color: #0f172a;">Free Meal</div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 4px; line-height: 1.4;">Claim your included Upfront meal</div>
                    <div style="margin-top: 16px; font-size: 12px; font-weight: 800; color: #3b82f6; display: flex; align-items: center; justify-content: space-between;">
                        Select Now <span>➔</span>
                    </div>
                </div>

                <!-- Seat Card -->
                <div onclick="navigateToSeatmapAndMakeFree()" style="flex: 0 0 160px; background: #fff; border-radius: 16px; padding: 14px; border: 2px solid #3b82f6; box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15); cursor: pointer; position: relative; overflow: hidden; transition: transform 0.2s;">
                    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, #3b82f6, #0ea5e9);"></div>
                    <div style="font-size: 28px; margin-bottom: 12px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));">💺</div>
                    <div style="font-size: 15px; font-weight: 800; color: #0f172a;">Free Seat</div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 4px; line-height: 1.4;">Pick any premium seat for free</div>
                    <div style="margin-top: 16px; font-size: 12px; font-weight: 800; color: #3b82f6; display: flex; align-items: center; justify-content: space-between;">
                        Select Now <span>➔</span>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    pnrCard.insertAdjacentHTML('afterend', perksHtml);
    window.appState.upfrontUnlocked = true;
}

function navigateToAddonsAndMakeFree(section) {
    if(typeof triggerHaptic === 'function') triggerHaptic('medium', 'Addons');
    if(typeof navigateTo === 'function') navigateTo('addons');
    
    setTimeout(() => {
        // Scroll to meals section
        if(section === 'meals') {
            const mealSection = document.getElementById('section-meals');
            if(mealSection) mealSection.scrollIntoView({behavior: 'smooth', block: 'start'});
        }
        
        // Make meals free visually
        const mealPrices = document.querySelectorAll('#section-meals .glass-price');
        mealPrices.forEach(price => {
            if(!price.innerText.includes('FREE')) {
                price.innerHTML = '<span style="text-decoration: line-through; opacity: 0.5; font-size: 10px; margin-right: 4px;">' + price.innerText + '</span> <span style="color: #10b981; font-weight: 900;">FREE</span>';
            }
        });
        const mealAddBtns = document.querySelectorAll('#section-meals .glass-add-btn');
        mealAddBtns.forEach(btn => {
            if(btn.innerText === '+ Add') {
                btn.style.background = '#d1fae5';
                btn.style.color = '#059669';
                btn.style.border = '1px solid #10b981';
            }
        });
        
        // Add a top banner inside Addons
        const addonsHeader = document.querySelector('#screenAddons .companion-header-inner');
        if (addonsHeader && !document.getElementById('addonsUpfrontBanner')) {
            addonsHeader.insertAdjacentHTML('afterend', `
                <div id="addonsUpfrontBanner" style="background: linear-gradient(90deg, #1e3a8a, #3b82f6); color: #fff; padding: 12px 24px; font-size: 13px; font-weight: 700; display: flex; align-items: center; gap: 8px;">
                    <span>✨</span> You are browsing with Upfront. Meals are free!
                </div>
            `);
        }
        
    }, 400);
}

function navigateToSeatmapAndMakeFree() {
    if(typeof triggerHaptic === 'function') triggerHaptic('medium', 'Seatmap');
    if(typeof navigateTo === 'function') navigateTo('seatmap_loading');
    
    // Seatmap loading takes 2.5s, wait before changing prices
    setTimeout(() => {
        // Look for any price tag elements in the seat map and make them free
        const seatPrices = document.querySelectorAll('.seat-price, .seat-cost'); // fallback classes
        seatPrices.forEach(p => {
            p.innerText = 'FREE';
            p.style.color = '#10b981';
            p.style.fontWeight = '900';
        });
        
        // Some implementations use raw text inside divs, we can search all small text divs
        document.querySelectorAll('div').forEach(d => {
            if (d.innerText && d.innerText.startsWith('₹') && d.innerText.length < 8 && !d.id.includes('total')) {
                d.innerText = 'FREE';
                d.style.color = '#10b981';
                d.style.fontWeight = '900';
            }
        });
        
        // Also update banner text inside seatmap if it exists
        const seatCohortBanner = document.getElementById('seatCohortBannerContainer');
        if (seatCohortBanner) {
            seatCohortBanner.style.display = 'flex';
            seatCohortBanner.style.background = 'linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)';
            seatCohortBanner.style.borderBottom = '1px solid #34d399';
            seatCohortBanner.innerHTML = '<div style="font-size: 12px; font-weight: 800; color: #065f46;">✨ Included with Upfront: Select any premium seat for free</div>';
        }
    }, 3200); // slightly longer to ensure seatmap is fully rendered
}
"""

if "unlockUpfrontPerks" not in content:
    with open('app.js', 'a') as f:
        f.write("\n" + new_functions)
    print("Added unlockUpfrontPerks to app.js")
else:
    print("unlockUpfrontPerks already exists in app.js")

