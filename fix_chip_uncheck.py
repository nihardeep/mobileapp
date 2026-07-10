import re

with open('app.js', 'r') as f:
    js = f.read()

old_logic = """window.toggleSavedPassengerChip = function(el, name) {
    if (el.classList.contains('active')) {
        el.classList.remove('active');
        el.querySelector('.chip-checkbox').innerHTML = '';
        el.style.background = '#fff';
        el.style.border = '1px solid #cbd5e1';
    } else {"""

new_logic = """window.toggleSavedPassengerChip = function(el, name) {
    if (el.classList.contains('active')) {
        el.classList.remove('active');
        el.querySelector('.chip-checkbox').innerHTML = '';
        el.style.background = '#fff';
        el.style.border = '1px solid #cbd5e1';
        el.querySelector('.chip-checkbox').style.background = 'transparent';
        el.querySelector('.chip-checkbox').style.border = '1px solid #cbd5e1';
        
        // Find the card that has this name and clear it
        document.querySelectorAll('.passenger-card.completed').forEach(card => {
            const cardNameEl = card.querySelector('.passenger-name');
            if (cardNameEl && cardNameEl.innerText === name) {
                card.classList.remove('completed');
                card.classList.add('empty');
                card.style.border = '1px solid #cbd5e1';
                const num = card.id.split('-')[2];
                const type = card.querySelector('.passenger-type').innerText;
                card.setAttribute('onclick', `openPassengerForm(${num}, '', '${type}', '')`);
                card.innerHTML = `
                    <div style="display: flex; align-items: center; gap: 16px;">
                        <div style="flex: 1;">
                            <div class="passenger-name">Passenger ${num}</div>
                            <div class="passenger-type">${type}</div>
                        </div>
                        <div class="passenger-add-btn">Add details ></div>
                    </div>
                `;
            }
        });
        updatePassengerCount();
    } else {"""

js = js.replace(old_logic, new_logic)

with open('app.js', 'w') as f:
    f.write(js)
