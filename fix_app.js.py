import re

with open('app.js', 'r') as f:
    js = f.read()

# Fix selectGender
old_select = """window.selectGender = function(gender) {
    document.getElementById('gender-male').classList.remove('active');
    document.getElementById('gender-female').classList.remove('active');
    if (gender === 'Male') {
        document.getElementById('gender-male').classList.add('active');
    } else {
        document.getElementById('gender-female').classList.add('active');
    }
};"""
new_select = """window.selectGender = function(gender) {
    const male = document.getElementById('gender-male');
    const female = document.getElementById('gender-female');
    male.classList.remove('active');
    female.classList.remove('active');
    
    // Reset styles
    male.style.border = '1px solid #cbd5e1';
    male.style.background = 'transparent';
    male.style.color = '#64748b';
    
    female.style.border = '1px solid #cbd5e1';
    female.style.background = 'transparent';
    female.style.color = '#64748b';
    
    if (gender === 'Male') {
        male.classList.add('active');
        male.style.border = '1px solid var(--indigo-blue)';
        male.style.background = 'rgba(14,165,233,0.05)';
        male.style.color = '#0f172a';
    } else {
        female.classList.add('active');
        female.style.border = '1px solid var(--indigo-blue)';
        female.style.background = 'rgba(14,165,233,0.05)';
        female.style.color = '#0f172a';
    }
};"""
js = js.replace(old_select, new_select)


# We'll replace the everything after "window.openBulkAddSheet = function() {"
start_idx = js.find('window.openBulkAddSheet = function() {')
if start_idx != -1:
    js = js[:start_idx]

fixed_logic = """
window.openBulkAddSheet = function() {
    const backdrop = document.getElementById('bottomSheetBackdrop');
    const sheet = document.getElementById('savedPassengersSheet');
    if (backdrop) backdrop.classList.add('active');
    if (sheet) sheet.classList.add('active');
};

window.toggleBulkCheckbox = function(el) {
    const cb = el.querySelector('input[type="checkbox"]');
    cb.checked = !cb.checked;
};

window.applyBulkAdd = function() {
    closeAllDrawers();
    // Simulate auto-filling 3 slots based on checkboxes
    let added = 1; // start after ragini (already 1)
    
    // Quick and dirty simulation
    document.querySelectorAll('.passenger-card.empty').forEach(card => {
        if (added < 3) { // Simulate adding 2 more
            card.classList.remove('empty');
            card.classList.add('completed');
            card.style.border = '2px solid #22c55e';
            const name = added === 1 ? 'Alka Pande' : 'Rajvardhan Shah';
            const num = card.id.split('-')[2];
            const type = card.querySelector('.passenger-type').innerText;
            card.setAttribute('onclick', `openPassengerForm(${num}, '${name}', '${type}', 'Female')`);
            card.innerHTML = `
                <div style="display: flex; align-items: center; gap: 16px;">
                    <div class="passenger-avatar" style="background: rgba(34, 197, 94, 0.1); color: #22c55e;">${name.substring(0,2).toUpperCase()}</div>
                    <div style="flex: 1;">
                        <div class="passenger-name" style="color: #22c55e;">${name}</div>
                        <div class="passenger-type">${type}</div>
                    </div>
                    <div class="passenger-status" style="font-size: 12px; color: var(--indigo-blue); font-weight: 800;">Edit ✏️</div>
                </div>
            `;
            added++;
        }
    });
    updatePassengerCount();
};

window.toggleSavedPassengerChip = function(el, name) {
    if (el.classList.contains('active')) {
        el.classList.remove('active');
        el.querySelector('.chip-checkbox').innerHTML = '';
        el.style.background = '#fff';
        el.style.border = '1px solid #cbd5e1';
    } else {
        el.classList.add('active');
        el.querySelector('.chip-checkbox').innerHTML = '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
        el.style.background = 'rgba(14, 165, 233, 0.05)';
        el.style.border = '1px solid var(--indigo-blue)';
        el.querySelector('.chip-checkbox').style.background = 'var(--indigo-blue)';
        el.querySelector('.chip-checkbox').style.border = 'none';
        
        // Auto-fill an empty card
        const emptyCard = document.querySelector('.passenger-card.empty');
        if (emptyCard) {
            emptyCard.classList.remove('empty');
            emptyCard.classList.add('completed');
            emptyCard.style.border = '2px solid #22c55e';
            const num = emptyCard.id.split('-')[2];
            const type = emptyCard.querySelector('.passenger-type').innerText;
            emptyCard.setAttribute('onclick', `openPassengerForm(${num}, '${name}', '${type}', 'Female')`);
            emptyCard.innerHTML = `
                <div style="display: flex; align-items: center; gap: 16px;">
                    <div class="passenger-avatar" style="background: rgba(34, 197, 94, 0.1); color: #22c55e;">${name.substring(0,2).toUpperCase()}</div>
                    <div style="flex: 1;">
                        <div class="passenger-name" style="color: #22c55e;">${name}</div>
                        <div class="passenger-type">${type}</div>
                    </div>
                    <div class="passenger-status" style="font-size: 12px; color: var(--indigo-blue); font-weight: 800;">Edit ✏️</div>
                </div>
            `;
            updatePassengerCount();
        }
    }
};

window.savePassengerForm = function() {
    const id = parseInt(document.getElementById('pf-id').value);
    const type = document.getElementById('pf-type').value;
    const fname = document.getElementById('pf-fname').value;
    
    if (!fname) {
        alert("Please enter the First Name.");
        return;
    }

    // Update the card on the main screen
    const card = document.getElementById('passenger-card-' + id);
    if (card) {
        card.classList.remove('empty');
        card.classList.add('completed');
        card.style.border = '2px solid #22c55e';
        
        // Ensure the Edit button works by updating the onclick attribute with the new name
        card.setAttribute('onclick', `openPassengerForm(${id}, '${fname}', '${type}', 'Male')`);
        
        card.innerHTML = `
            <div style="display: flex; align-items: center; gap: 16px;">
                <div class="passenger-avatar" style="background: rgba(34, 197, 94, 0.1); color: #22c55e;">${fname.substring(0,2).toUpperCase()}</div>
                <div style="flex: 1;">
                    <div class="passenger-name" style="color: #22c55e;">${fname}</div>
                    <div class="passenger-type">${type}</div>
                </div>
                <div class="passenger-status" style="font-size: 12px; color: var(--indigo-blue); font-weight: 800;">Edit ✏️</div>
            </div>
        `;
    }

    updatePassengerCount();
    closeAllDrawers();

    // AUTO-ADVANCE: Find the next empty passenger and open it
    setTimeout(() => {
        const nextEmpty = document.querySelector('.passenger-card.empty');
        if (nextEmpty) {
            nextEmpty.click(); // Programmatically click the next empty card to open its form
        }
    }, 400); // Wait for drawer to close smoothly before opening the next
};

window.updatePassengerCount = function() {
    const completedCards = document.querySelectorAll('.passenger-card.completed').length;
    document.getElementById('passenger-added-count').innerText = completedCards;
    
    const nextBtn = document.getElementById('passenger-next-btn');
    if (completedCards === 4) { // Assuming 4 total for this prototype
        nextBtn.disabled = false;
        nextBtn.style.opacity = '1';
        nextBtn.style.background = 'var(--indigo-blue)';
        nextBtn.style.color = '#fff';
    } else {
        nextBtn.disabled = true;
        nextBtn.style.opacity = '0.5';
    }
};
"""

js += fixed_logic

with open('app.js', 'w') as f:
    f.write(js)
