with open('app.js', 'a') as f:
    f.write('''

// ==========================================================================
// ADD-ONS: RADICAL REDESIGN LOGIC
// ==========================================================================

let addonCart = {}; // { paxIndex: { total: 0, items: [] } }
let currentAddonPax = 0;
let masterTotalFare = 6182;
let baseFare = 6182;

function initAddonsScreen() {
    // 1. Populate Passenger Cart Headers
    const paxContainer = document.getElementById('addonPaxCartContainer');
    if (paxContainer) {
        paxContainer.innerHTML = '';
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
            paxList = [
                { name: 'Priyal', type: 'Adult' },
                { name: 'Rajendraprasad', type: 'Infant' },
                { name: 'Abhay', type: 'Senior Citizen' }
            ];
        }

        paxList.forEach((pax, idx) => {
            if (!addonCart[idx]) {
                addonCart[idx] = { total: 0, items: [] };
            }
            const chip = document.createElement('div');
            chip.className = `dynamic-pax-chip ${idx === 0 ? 'active' : ''}`;
            chip.id = `pax-chip-${idx}`;
            chip.onclick = () => selectAddonPax(idx, chip);
            chip.innerHTML = `
                <div class="pax-name">${pax.name} <span>₹<span class="pax-chip-total">${addonCart[idx].total}</span></span></div>
                <div class="pax-subtotal">Cart: <span class="pax-chip-items">${addonCart[idx].items.length}</span> items</div>
            `;
            paxContainer.appendChild(chip);
        });
        currentAddonPax = 0;
    }

    // 2. Setup Scroll-Spy
    setupScrollSpy();

    // 3. Smart Inclusion Freebies
    const mealBanner = document.getElementById('meal-freebie-banner');
    const baggageBanner = document.getElementById('baggage-freebie-banner');
    
    // Reset pricing just in case
    document.getElementById('veg-meal-price').innerText = '₹ 370';
    document.getElementById('veg-meal-btn').innerText = 'Add';
    
    if (appState.isStudentMode) {
        if (baggageBanner) baggageBanner.style.display = 'flex';
        if (mealBanner) mealBanner.style.display = 'none';
    } else if (appState.selectedFareIndex === 1) { // Popular Fare
        if (mealBanner) mealBanner.style.display = 'flex';
        if (baggageBanner) baggageBanner.style.display = 'none';
        
        // Make Veg Meal Free
        document.getElementById('veg-meal-price').innerText = 'Free';
        document.getElementById('veg-meal-btn').innerText = 'Included';
        document.getElementById('veg-meal-btn').style.background = '#22c55e';
        document.getElementById('veg-meal-btn').style.borderColor = '#22c55e';
    } else {
        if (baggageBanner) baggageBanner.style.display = 'none';
        if (mealBanner) mealBanner.style.display = 'none';
    }

    updateMasterTotal();
}

// Ensure initAddonsScreen is called from navigateTo
// (This was already added in the previous step's teardown/rebuild logic)

function selectAddonPax(index, chipEl) {
    currentAddonPax = index;
    document.querySelectorAll('.dynamic-pax-chip').forEach(c => c.classList.remove('active'));
    chipEl.classList.add('active');
    chipEl.scrollIntoView({ behavior: 'smooth', inline: 'center' });
    triggerHaptic('light', 'Switched passenger');
    
    // Ideally here we would also re-render the buttons to show what THIS passenger has added.
    // For the prototype, we just switch the active visual state.
}

function toggleAddonCart(btn, itemName, price) {
    if (btn.innerText === 'Included') return;
    
    const isAdded = btn.classList.contains('added');
    
    if (isAdded) {
        btn.classList.remove('added');
        btn.innerHTML = btn.classList.contains('neon-add-btn') ? 'Add to Cart' : 'Add';
        addonCart[currentAddonPax].total -= price;
        const index = addonCart[currentAddonPax].items.indexOf(itemName);
        if (index > -1) addonCart[currentAddonPax].items.splice(index, 1);
        triggerHaptic('medium', 'Removed');
    } else {
        btn.classList.add('added');
        btn.innerHTML = btn.classList.contains('neon-add-btn') ? 'Added ✓' : 'Added ✓';
        addonCart[currentAddonPax].total += price;
        addonCart[currentAddonPax].items.push(itemName);
        triggerHaptic('success', 'Added');
        
        // Fly animation could go here
    }
    
    // Update individual passenger chip
    const chip = document.getElementById(`pax-chip-${currentAddonPax}`);
    if (chip) {
        chip.querySelector('.pax-chip-total').innerText = addonCart[currentAddonPax].total;
        chip.querySelector('.pax-chip-items').innerText = addonCart[currentAddonPax].items.length;
    }
    
    updateMasterTotal();
}

function updateMasterTotal() {
    let addonsSum = 0;
    for (let key in addonCart) {
        addonsSum += addonCart[key].total;
    }
    masterTotalFare = baseFare + addonsSum;
    const totalEl = document.getElementById('addon-checkout-total');
    if (totalEl) totalEl.innerText = `₹ ${masterTotalFare.toLocaleString('en-IN')}`;
}

// SCROLL SPY LOGIC
function setupScrollSpy() {
    const feed = document.getElementById('addonsMainFeed');
    const sections = document.querySelectorAll('.addon-scroll-section');
    const tabs = document.querySelectorAll('.spy-tab');
    
    if (!feed || sections.length === 0) return;
    
    feed.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(sec => {
            const secTop = sec.offsetTop;
            const secHeight = sec.clientHeight;
            if (feed.scrollTop >= (secTop - 150)) {
                current = sec.getAttribute('id').replace('section-', '');
            }
        });
        
        tabs.forEach(tab => {
            tab.classList.remove('active');
            if (tab.innerText.toLowerCase().includes(current)) {
                tab.classList.add('active');
                tab.scrollIntoView({ behavior: 'smooth', inline: 'center' });
            }
        });
    });
}

function scrollToAddonSection(id) {
    const feed = document.getElementById('addonsMainFeed');
    const section = document.getElementById(`section-${id}`);
    if (feed && section) {
        // smooth scroll to section
        feed.scrollTo({
            top: section.offsetTop - 20,
            behavior: 'smooth'
        });
    }
}

// MEAL FILTERS
function filterMeals(type, filterBtn) {
    document.querySelectorAll('.meal-filter').forEach(btn => btn.classList.remove('active'));
    filterBtn.classList.add('active');
    triggerHaptic('light', 'Filtered meals');
    
    const meals = document.querySelectorAll('.immersive-meal-card');
    meals.forEach(meal => {
        if (type === 'all' || meal.getAttribute('data-type') === type) {
            meal.style.display = 'block';
        } else {
            meal.style.display = 'none';
        }
    });
}

// BAGGAGE STEPPER
let baggageExtra = 0;
function updateBaggage(change) {
    const valEl = document.getElementById('baggage-val');
    const costEl = document.getElementById('baggage-cost');
    
    if (!valEl || !costEl) return;
    
    let currentVal = parseInt(valEl.innerText);
    currentVal += change;
    if (currentVal < 0) currentVal = 0;
    
    // Calculate difference
    const diff = currentVal - baggageExtra;
    baggageExtra = currentVal;
    
    valEl.innerText = baggageExtra;
    
    const cost = baggageExtra * 100; // 100 rs per kg
    costEl.innerText = `₹ ${cost}`;
    
    // Update master cart directly for baggage
    addonCart[currentAddonPax].total += (diff * 100);
    
    const chip = document.getElementById(`pax-chip-${currentAddonPax}`);
    if (chip) {
        chip.querySelector('.pax-chip-total').innerText = addonCart[currentAddonPax].total;
    }
    updateMasterTotal();
    triggerHaptic('light', 'Baggage updated');
}

''')
