import re

with open('app.js', 'r') as f:
    content = f.read()

# Replace the Seat Map Logic block
new_js = """
// ==========================================================================
// SEAT MAP LOGIC
// ==========================================================================

let seatMapState = {
    currentPaxIndex: 0,
    paxList: [],
    assignments: {}, // maps paxIndex -> { seatId: '1A', type: 'stretch', price: 750 }
};

function initSeatMapScreen() {
    // 1. Setup Passengers
    const completedPax = document.querySelectorAll('.passenger-card.completed');
    let list = [];
    if (completedPax.length > 0) {
        completedPax.forEach((card) => {
            const nameEl = card.querySelector('.passenger-name');
            const typeEl = card.querySelector('.passenger-type');
            if (nameEl && typeEl) list.push({ name: nameEl.innerText, type: typeEl.innerText });
        });
    } else {
        list = [
            { name: 'Rahul Sharma', type: 'Adult' },
            { name: 'Anita Sharma', type: 'Adult' },
            { name: 'Aarav Sharma', type: 'Child' }
        ];
    }
    seatMapState.paxList = list;
    
    // 2. Render Passenger Chips
    renderSeatMapPaxChips();
    
    // 3. Render Grid
    renderSeatMapGrid();
    
    // 4. Init Bottom Bar
    updateSeatMapFooterCTA();
}

function getPaxInitials(name) {
    let initials = name.substring(0,2).toUpperCase();
    if (name.includes(' ')) {
        const parts = name.split(' ');
        initials = parts[0][0] + (parts[1] ? parts[1][0] : '');
    }
    return initials;
}

function renderSeatMapPaxChips() {
    const container = document.getElementById('seatMapPaxCartContainer');
    if (!container) return;
    
    container.innerHTML = '';
    seatMapState.paxList.forEach((pax, idx) => {
        const chip = document.createElement('div');
        chip.id = `seatmap-pax-${idx}`;
        chip.style.cssText = `
            flex-shrink: 0;
            width: 160px;
            border: 2px solid ${idx === seatMapState.currentPaxIndex ? '#0066FF' : '#e2e8f0'};
            border-radius: 12px;
            padding: 12px;
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
            background: ${idx === seatMapState.currentPaxIndex ? '#f0fdf4' : '#fff'};
            transition: all 0.2s;
        `;
        chip.onclick = () => selectSeatMapPax(idx, chip);
        
        let imgHtml = `<div style="width: 32px; height: 32px; border-radius: 50%; background: #0f172a; color: white; display: flex; justify-content: center; align-items: center; font-size: 12px; font-weight: 800;">${getPaxInitials(pax.name)}</div>`;
        
        const assignment = seatMapState.assignments[idx];
        const statusText = assignment ? assignment.seatId : '--';
        
        chip.innerHTML = `
            ${imgHtml}
            <div>
                <div style="font-size: 13px; font-weight: 800; color: #0f172a; line-height: 1.2;">${pax.name}</div>
                <div style="font-size: 11px; font-weight: 600; color: #64748b; margin-top: 4px;">SEAT <span id="seatmap-pax-status-${idx}" style="color: ${assignment ? '#0066FF' : '#94a3b8'}; font-weight: 800; margin-left: 4px;">${statusText}</span></div>
            </div>
        `;
        container.appendChild(chip);
    });
}

function selectSeatMapPax(idx) {
    triggerHaptic('light', 'Pax Changed');
    seatMapState.currentPaxIndex = idx;
    renderSeatMapPaxChips();
}

function renderSeatMapGrid() {
    const grid = document.getElementById('seatMapGrid');
    if (!grid) return;
    
    grid.innerHTML = '';
    
    for (let r = 1; r <= 30; r++) {
        // Wing exit indicator
        if (r === 12 || r === 13) {
            const exitBanner = document.createElement('div');
            exitBanner.style.cssText = 'text-align: center; margin: 16px 0;';
            exitBanner.innerHTML = '<span style="background: #ffedd5; color: #ea580c; font-size: 10px; font-weight: 800; padding: 4px 12px; border-radius: 4px; letter-spacing: 1px;">EMERGENCY EXIT ROW</span>';
            grid.appendChild(exitBanner);
        }

        const rowDiv = document.createElement('div');
        rowDiv.className = 'seat-row';
        if (r === 12 || r === 13) rowDiv.classList.add('exit-row');

        // Left Side (A, B, C)
        ['A', 'B', 'C'].forEach(letter => {
            rowDiv.appendChild(createSeat(r, letter));
        });
        
        // Aisle
        const aisle = document.createElement('div');
        aisle.className = 'seat-aisle';
        aisle.innerText = `ROW ${r}`;
        rowDiv.appendChild(aisle);
        
        // Right Side (D, E, F)
        ['D', 'E', 'F'].forEach(letter => {
            rowDiv.appendChild(createSeat(r, letter));
        });
        
        grid.appendChild(rowDiv);
    }
}

function createSeat(row, letter) {
    const seatId = `${row}${letter}`;
    const el = document.createElement('div');
    
    // Determine seat type
    let type = 'standard';
    let basePrice = 350;
    
    if (row === 1 || row === 12 || row === 13) {
        type = 'stretch';
        basePrice = 800;
    } else if (row >= 2 && row <= 11) {
        type = 'upfront';
        basePrice = 750;
    }
    
    // Randomly occupy some seats (deterministic based on seatId)
    const seed = (row * 31 + letter.charCodeAt(0)) % 100;
    const isOccupied = seed < 25; // 25% occupied
    
    if (isOccupied) type = 'occupied';
    
    // Handle Free Perks
    const isFree = appState.hasComplimentaryPerks && type !== 'occupied';
    if (isFree) type = 'free';
    
    const finalPrice = isFree ? 0 : basePrice;
    
    el.className = `seat-3d seat-${type}`;
    el.id = `seat-${seatId}`;
    
    // Inner HTML
    if (type === 'occupied') {
        el.innerHTML = `<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#cbd5e1" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>`;
    } else {
        const displayPrice = isFree ? 'INCLUDED' : `₹${finalPrice}`;
        el.innerHTML = `
            <div class="seat-label">${seatId}</div>
            <div class="seat-price">${displayPrice}</div>
        `;
        el.onclick = () => selectSeat(seatId, type, finalPrice, isFree);
    }
    
    return el;
}

function selectSeat(seatId, type, price, isFree) {
    const idx = seatMapState.currentPaxIndex;
    
    // Check if this seat is already selected by someone
    let alreadyAssignedTo = -1;
    for (const p in seatMapState.assignments) {
        if (seatMapState.assignments[p].seatId === seatId) {
            alreadyAssignedTo = parseInt(p);
            break;
        }
    }
    
    if (alreadyAssignedTo !== -1 && alreadyAssignedTo !== idx) {
        triggerHaptic('error', 'Seat Taken');
        showToast('This seat is already selected for another passenger.');
        return;
    }
    
    // Deselect previously selected seat for this pax
    const previous = seatMapState.assignments[idx];
    if (previous) {
        const prevEl = document.getElementById(`seat-${previous.seatId}`);
        if (prevEl) {
            prevEl.classList.remove('seat-selected');
            const avatar = prevEl.querySelector('.seat-pax-avatar');
            if (avatar) avatar.remove();
        }
    }
    
    // If clicking same seat, deselect it
    if (previous && previous.seatId === seatId) {
        delete seatMapState.assignments[idx];
        triggerHaptic('medium', 'Seat Deselected');
    } else {
        // Select new seat
        seatMapState.assignments[idx] = { seatId, type, price, isFree };
        const newEl = document.getElementById(`seat-${seatId}`);
        if (newEl) {
            newEl.classList.add('seat-selected');
            
            // Add pax avatar to seat
            const paxName = seatMapState.paxList[idx].name;
            const initials = getPaxInitials(paxName);
            const avatar = document.createElement('div');
            avatar.className = 'seat-pax-avatar';
            avatar.innerText = initials;
            newEl.appendChild(avatar);
        }
        triggerHaptic('success', `Selected ${seatId}`);
    }
    
    // Update UI
    renderSeatMapPaxChips();
    updateSeatMapFooterCTA();
    
    // Auto-advance to next passenger if available
    if (seatMapState.assignments[idx] && idx < seatMapState.paxList.length - 1) {
        setTimeout(() => {
            selectSeatMapPax(idx + 1);
        }, 500);
    }
}

function updateSeatMapFooterCTA() {
    // 1. Update Subtotal
    let total = 0;
    for (const p in seatMapState.assignments) {
        total += seatMapState.assignments[p].price;
    }
    const priceEl = document.getElementById('seatMapSelectedSeatPrice');
    if (priceEl) priceEl.innerText = `₹${total}`;
    
    // 2. Update Indicator Circles
    const indContainer = document.getElementById('seatMapBottomIndicators');
    if (indContainer) {
        indContainer.innerHTML = '';
        seatMapState.paxList.forEach((pax, idx) => {
            if (seatMapState.assignments[idx]) {
                const initials = getPaxInitials(pax.name);
                indContainer.innerHTML += `<div style="width: 24px; height: 24px; border-radius: 50%; background: #0066FF; color: white; display: flex; justify-content: center; align-items: center; font-size: 9px; font-weight: 800; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); z-index: ${10-idx}; position: relative;">${initials}</div>`;
            }
        });
    }
}

function confirmSeatSelection() {
    triggerHaptic('success', 'Seats Confirmed');
    navigateTo('addons');
}
"""

start_idx = content.find("// ==========================================================================\n// SEAT MAP LOGIC")

if start_idx != -1:
    final_content = content[:start_idx] + new_js
    with open('app.js', 'w') as f:
        f.write(final_content)
    print("JS Updated Successfully")
else:
    print("Could not find JS boundary")
