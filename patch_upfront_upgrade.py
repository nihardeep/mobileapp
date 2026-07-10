import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace the "Got it" button with an "Upgrade" button that calls a new function
old_btn = """<button class="primary-btn" style="width: 100%; padding: 16px; border-radius: 12px; font-size: 16px; font-weight: 800; background: #001B94; color: white; border: none;" onclick="closeAllDrawers()">Got it</button>"""
new_btn = """<button class="primary-btn" style="width: 100%; padding: 16px; border-radius: 12px; font-size: 16px; font-weight: 800; background: #001B94; color: white; border: none;" onclick="upgradeToUpfront()">Upgrade for ₹2,499</button>"""

html = html.replace(old_btn, new_btn)

# Add an ID to the Upfront banner text so we can change it
old_banner_text = """<div style="font-size: 11px; font-weight: 700; color: #475569;">Upgrade @ ₹2,499</div>"""
new_banner_text = """<div id="upfront-status-text" style="font-size: 11px; font-weight: 700; color: #475569;">Upgrade @ ₹2,499</div>"""

html = html.replace(old_banner_text, new_banner_text)

# Add an ID to the SEE BENEFITS button so we can hide it
old_see_benefits = """<div style="font-size: 10px; font-weight: 800; color: var(--indigo-blue); letter-spacing: 0.5px; cursor: pointer;" onclick="document.getElementById('addonBenefitsDrawer').classList.add('visible'); document.getElementById('bottomSheetBackdrop').classList.add('visible');">SEE BENEFITS →</div>"""
new_see_benefits = """<div id="upfront-see-benefits-btn" style="font-size: 10px; font-weight: 800; color: var(--indigo-blue); letter-spacing: 0.5px; cursor: pointer;" onclick="document.getElementById('addonBenefitsDrawer').classList.add('visible'); document.getElementById('bottomSheetBackdrop').classList.add('visible');">SEE BENEFITS →</div>"""

html = html.replace(old_see_benefits, new_see_benefits)

with open('index.html', 'w') as f:
    f.write(html)


with open('app.js', 'r') as f:
    js = f.read()

# Add the upgradeToUpfront function
new_function = """
window.upgradeToUpfront = function() {
    triggerHaptic('medium', 'Upgrade');
    
    // Update the UI on the Addons screen
    const statusText = document.getElementById('upfront-status-text');
    if (statusText) {
        statusText.innerText = 'Upgraded to UpFront!';
        statusText.style.color = '#15803d'; // Green color for success
    }
    
    const seeBenefitsBtn = document.getElementById('upfront-see-benefits-btn');
    if (seeBenefitsBtn) {
        seeBenefitsBtn.style.display = 'none';
    }
    
    // Add to total fare
    masterTotalFare += 2499;
    const addonTotal = document.getElementById('addon-checkout-total');
    if (addonTotal) {
        addonTotal.innerText = '₹ ' + masterTotalFare.toLocaleString('en-IN');
    }
    
    // Also update passenger total fare just in case
    const paxTotal = document.getElementById('passenger-total-fare');
    if (paxTotal) {
        paxTotal.innerText = '₹ ' + masterTotalFare.toLocaleString('en-IN');
    }
    
    closeAllDrawers();
    
    setTimeout(() => {
        alert('Successfully upgraded to UpFront for ₹2,499!');
    }, 300);
};
"""

js = js + new_function

with open('app.js', 'w') as f:
    f.write(js)
