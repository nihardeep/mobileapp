import re

with open('app.js', 'r') as f:
    js = f.read()

# Add logic inside navigateTo
old_nav = """    } else if (screenName === 'studentHub') {
        const studentScreen = document.getElementById('screenStudentHub');
        if (studentScreen) studentScreen.classList.add('active');
    }"""

new_nav = """    } else if (screenName === 'studentHub') {
        const studentScreen = document.getElementById('screenStudentHub');
        if (studentScreen) studentScreen.classList.add('active');
    } else if (screenName === 'addons') {
        const addonsScreen = document.getElementById('screenAddons');
        if (addonsScreen) {
            addonsScreen.classList.add('active');
            initAddonsScreen();
        }
    }"""

js = js.replace(old_nav, new_nav)

# Append Addons Logic
js += """
// ==========================================================================
// ADD-ONS SCREEN LOGIC
// ==========================================================================

let currentAddonPax = 0;
let addonTotalFare = 6182; // Base mock fare

function initAddonsScreen() {
    // 1. Populate Passenger Chips
    const paxContainer = document.getElementById('addonPaxChipsContainer');
    if (paxContainer) {
        paxContainer.innerHTML = '';
        
        // We look at the actual completed passengers from the passenger screen
        const completedPax = document.querySelectorAll('.passenger-card.completed');
        let paxList = [];
        
        if (completedPax.length > 0) {
            completedPax.forEach((card, idx) => {
                const nameEl = card.querySelector('.passenger-name');
                const typeEl = card.querySelector('.passenger-type');
                if (nameEl && typeEl) {
                    paxList.push({ name: nameEl.innerText, type: typeEl.innerText });
                }
            });
        } else {
            // Fallback mock pax if navigated directly
            paxList = [
                { name: 'Priyal', type: 'Adult' },
                { name: 'Rajendraprasad', type: 'Infant' },
                { name: 'Abhay', type: 'Senior Citizen' }
            ];
        }

        paxList.forEach((pax, idx) => {
            const chip = document.createElement('div');
            chip.className = `addon-pax-chip ${idx === 0 ? 'active' : ''}`;
            chip.onclick = () => selectAddonPax(idx, chip);
            chip.innerHTML = `
                <div class="pax-name">${pax.name} <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-4"></path><path d="M12 8h.01"></path></svg></div>
                <div class="pax-type">${pax.type}</div>
            `;
            paxContainer.appendChild(chip);
        });
        currentAddonPax = 0;
    }

    // 2. Smart Inclusions Logic
    const banner = document.getElementById('smart-inclusion-banner');
    const title = document.getElementById('smart-inclusion-title');
    const desc = document.getElementById('smart-inclusion-desc');
    const mealPrice = document.getElementById('meal-price-val');
    const seatPrice = document.getElementById('seat-eat-price');
    const mealAddBtn = document.getElementById('meal-add-btn');
    const seatAddBtn = document.getElementById('seat-eat-add-btn');

    if (banner) {
        if (appState.isStudentMode) {
            banner.style.display = 'flex';
            title.innerText = 'Student Benefits Applied';
            desc.innerText = '10kg extra baggage and standard seat is free!';
        } else if (appState.selectedFareIndex === 1) { // Popular Fare (assuming index 1 is Popular)
            banner.style.display = 'flex';
            title.innerText = 'Popular Fare Benefits Applied';
            desc.innerText = 'Free Veg Meal and standard seat included!';
            if (mealPrice) mealPrice.innerText = 'Free';
            if (seatPrice) seatPrice.innerText = 'Free';
            if (mealAddBtn) mealAddBtn.innerText = 'Included';
            if (seatAddBtn) seatAddBtn.innerText = 'Included';
        } else {
            banner.style.display = 'none';
        }
    }
    
    // Set initial fare
    document.getElementById('addon-total-fare').innerText = `₹ ${addonTotalFare.toLocaleString('en-IN')}`;
}

function selectAddonPax(index, chipEl) {
    currentAddonPax = index;
    document.querySelectorAll('.addon-pax-chip').forEach(c => c.classList.remove('active'));
    chipEl.classList.add('active');
    chipEl.scrollIntoView({ behavior: 'smooth', inline: 'center' });
    triggerHaptic('light', 'Switched passenger');
}

function addAddon(btn, itemName, price) {
    if (btn.innerText === 'Included') return; // Cannot modify included items

    const card = btn.closest('.addon-bundle-card') || btn.closest('.addon-meal-card');
    
    if (card.classList.contains('added')) {
        // Remove Addon
        card.classList.remove('added');
        btn.innerHTML = 'Add';
        addonTotalFare -= price;
        triggerHaptic('medium', 'Addon removed');
    } else {
        // Add Addon
        card.classList.add('added');
        btn.innerHTML = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>';
        addonTotalFare += price;
        triggerHaptic('success', 'Addon added');
        
        // Show Toast
        const toast = document.getElementById('addon-toast');
        if (toast) {
            toast.style.transform = 'translateY(0)';
            toast.style.opacity = '1';
            setTimeout(() => {
                toast.style.transform = 'translateY(150%)';
                toast.style.opacity = '0';
            }, 3000);
        }
    }
    
    // Update Total
    document.getElementById('addon-total-fare').innerText = `₹ ${addonTotalFare.toLocaleString('en-IN')}`;
}
"""

with open('app.js', 'w') as f:
    f.write(js)
