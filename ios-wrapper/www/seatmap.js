
// ==========================================================================
// SEAT MAP LOGIC
// ==========================================================================

let seatMapState = {
    currentPaxIndex: 0,
    paxList: [],
    assignments: {}, // maps paxIndex -> { seatId: '12A', type: 'stretch', price: 0 }
    isVertical: true
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
            { name: 'Priyal', type: 'Adult' },
            { name: 'Rajendraprasad', type: 'Infant' },
            { name: 'Abhay', type: 'Senior Citizen' }
        ];
    }
    seatMapState.paxList = list;
    
    // 2. Render Header Pax Indicator
    renderSeatMapPaxHeader();
    
    // 3. Render Bottom Pax Scroller
    renderSeatMapPaxFooter();
    
    // 4. Generate Seat Grid
    renderSeatMapGrid();
    
    // 5. Setup native scroll snapping / pan handlers
    // Native CSS overflow handles scrolling perfectly for both horizontal and vertical if wrapper is sized right.
}

function renderSeatMapPaxHeader() {
    const indicator = document.getElementById('seatMapPaxIndicator');
    if (indicator && seatMapState.paxList[seatMapState.currentPaxIndex]) {
        indicator.innerText = `Selecting for ${seatMapState.paxList[seatMapState.currentPaxIndex].name.split(' ')[0]}`;
    }
}

function renderSeatMapPaxFooter() {
    const container = document.getElementById('seatMapPaxCartContainer');
    if (!container) return;
    
    container.innerHTML = '';
    seatMapState.paxList.forEach((pax, idx) => {
        const chip = document.createElement('div');
        chip.className = `compact-pax-chip ${idx === seatMapState.currentPaxIndex ? 'active' : ''}`;
        chip.id = `seatmap-pax-${idx}`;
        chip.onclick = () => selectSeatMapPax(idx, chip);
        
        let initials = pax.name.substring(0,2).toUpperCase();
        if (pax.name.includes(' ')) {
            const parts = pax.name.split(' ');
            initials = parts[0][0] + (parts[1] ? parts[1][0] : '');
        }
        
        const assignment = seatMapState.assignments[idx];
        const statusText = assignment ? `Seat ${assignment.seatId}` : 'Not selected';
        
        chip.innerHTML = `
            <div class="compact-pax-avatar">${initials}</div>
            <div class="compact-pax-info">
                <div class="compact-pax-name">${pax.name}</div>
                <div class="compact-pax-status" id="seatmap-pax-status-${idx}">${statusText}</div>
            </div>
        `;
        container.appendChild(chip);
    });
}

function selectSeatMapPax(idx, el) {
    triggerHaptic('light', 'Pax Changed');
    seatMapState.currentPaxIndex = idx;
    
    document.querySelectorAll('#seatMapPaxCartContainer .compact-pax-chip').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    
    renderSeatMapPaxHeader();
    updateSeatMapFooterCTA();
}

function renderSeatMapGrid() {
    const grid = document.getElementById('seatMapGrid');
    if (!grid) return;
    
    grid.innerHTML = '';
    
    // 30 Rows for standard A320
    for (let r = 1; r <= 30; r++) {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'seat-row';
        
        // Wing overlay check
        if (r === 12) {
            const leftWing = document.createElement('div');
            leftWing.className = 'aircraft-wing-left';
            const rightWing = document.createElement('div');
            rightWing.className = 'aircraft-wing-right';
            grid.appendChild(leftWing);
            grid.appendChild(rightWing);
        }

        // Left Side (A, B, C)
        ['A', 'B', 'C'].forEach(letter => {
            rowDiv.appendChild(createSeat(r, letter));
        });
        
        // Aisle
        const aisle = document.createElement('div');
        aisle.className = 'seat-aisle';
        aisle.innerText = r;
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
    let basePrice = 250;
    
    if (row === 1 || row === 12 || row === 13) {
        type = 'stretch';
        basePrice = 1500;
    } else if (row >= 2 && row <= 11) {
        type = 'upfront';
        basePrice = 800;
    }
    
    // Randomly occupy some seats (deterministic based on seatId)
    const seed = (row * 31 + letter.charCodeAt(0)) % 100;
    const isOccupied = seed < 30; // 30% occupied
    
    if (isOccupied) type = 'occupied';
    
    el.className = `seat-3d seat-${type}`;
    el.id = `seat-${seatId}`;
    
    // Handle Free Perks
    const isFree = appState.hasComplimentaryPerks && type !== 'occupied';
    const finalPrice = isFree ? 0 : basePrice;
    
    // Inner HTML
    if (type === 'occupied') {
        el.innerHTML = '×';
    } else {
        const displayPrice = isFree ? 'FREE' : `₹${finalPrice}`;
        const colorClass = isFree ? 'seat-free-badge' : '';
        el.innerHTML = `
            ${seatId}
            <div class="seat-price-badge ${colorClass}">${displayPrice}</div>
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
            
            // Add pax avatar
            const paxName = seatMapState.paxList[idx].name;
            const initial = paxName.substring(0,1).toUpperCase();
            const avatar = document.createElement('div');
            avatar.className = 'seat-pax-avatar';
            avatar.innerText = initial;
            newEl.appendChild(avatar);
            
            // Bouncy animation
            newEl.style.transform = 'translateY(-10px) scale(1.1)';
            setTimeout(() => newEl.style.transform = '', 200);
        }
        triggerHaptic('success', `Selected ${seatId}`);
    }
    
    // Update UI
    const statusEl = document.getElementById(`seatmap-pax-status-${idx}`);
    if (statusEl) {
        statusEl.innerText = seatMapState.assignments[idx] ? `Seat ${seatId}` : 'Not selected';
    }
    
    updateSeatMapFooterCTA();
    
    // Auto-advance to next passenger if available
    if (seatMapState.assignments[idx] && idx < seatMapState.paxList.length - 1) {
        setTimeout(() => {
            const nextChip = document.getElementById(`seatmap-pax-${idx + 1}`);
            if (nextChip) selectSeatMapPax(idx + 1, nextChip);
        }, 500);
    }
}

function updateSeatMapFooterCTA() {
    const label = document.getElementById('seatMapSelectedSeatLabel');
    const priceEl = document.getElementById('seatMapSelectedSeatPrice');
    const btn = document.getElementById('btnConfirmSeatSelection');
    
    const assignment = seatMapState.assignments[seatMapState.currentPaxIndex];
    
    if (assignment) {
        label.innerText = `Seat ${assignment.seatId} (${assignment.type.toUpperCase()})`;
        if (assignment.isFree) {
            priceEl.innerText = 'FREE (Complimentary)';
            priceEl.style.display = 'block';
        } else {
            priceEl.innerText = `₹${assignment.price}`;
            priceEl.style.display = 'block';
        }
    } else {
        label.innerText = 'Select a seat';
        priceEl.style.display = 'none';
    }
    
    // Enable CTA if all pax have seats
    const allSelected = seatMapState.paxList.every((p, i) => seatMapState.assignments[i] != null);
    if (allSelected) {
        btn.style.opacity = '1';
        btn.innerText = 'Confirm Seats';
        btn.onclick = () => alert('Seats Confirmed! Proceeding to Payment.');
    } else {
        btn.style.opacity = '0.5';
        btn.innerText = 'Confirm';
        btn.onclick = null;
    }
}

function toggleSeatMapView() {
    triggerHaptic('light', 'Toggle View');
    const wrapper = document.getElementById('aircraftFuselageWrapper');
    if (!wrapper) return;
    
    if (seatMapState.isVertical) {
        wrapper.classList.remove('vertical-view');
        wrapper.classList.add('horizontal-view');
        document.getElementById('btnToggleSeatView').innerText = 'Vertical';
    } else {
        wrapper.classList.remove('horizontal-view');
        wrapper.classList.add('vertical-view');
        document.getElementById('btnToggleSeatView').innerText = 'Horizontal';
    }
    seatMapState.isVertical = !seatMapState.isVertical;
}

function scrollToRecommendedSeat() {
    triggerHaptic('medium', 'Scroll to row 12');
    const row12 = document.getElementById('seat-12A');
    if (row12) {
        row12.scrollIntoView({ behavior: 'smooth', block: 'center' });
        // Pulse effect
        const seats = ['12A','12B','12C','12D','12E','12F'].map(id => document.getElementById(`seat-${id}`));
        seats.forEach(s => {
            if(s) {
                s.style.boxShadow = '0 0 0 4px rgba(15, 164, 107, 0.5)';
                setTimeout(() => s.style.boxShadow = '', 1500);
            }
        });
    }
}


// Zoom Logic
let seatMapZoomLevel = 1.0;
function zoomSeatMap(delta) {
    const wrapper = document.getElementById('aircraftFuselageWrapper');
    if (!wrapper) return;
    
    seatMapZoomLevel += delta;
    
    // Clamp zoom level between 0.5 and 2.0
    if (seatMapZoomLevel < 0.5) seatMapZoomLevel = 0.5;
    if (seatMapZoomLevel > 2.0) seatMapZoomLevel = 2.0;
    
    wrapper.style.transform = `scale(${seatMapZoomLevel})`;
    
    triggerHaptic('light', 'Zoom Changed');
}
