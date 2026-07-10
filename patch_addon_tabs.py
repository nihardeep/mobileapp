import re

with open('app.js', 'r') as f:
    js = f.read()

# Replace dynamic-pax-chip with immersive-person-card
old_chip = """            const chip = document.createElement('div');
            chip.className = `dynamic-pax-chip ${idx === 0 ? 'active' : ''}`;
            chip.id = `pax-chip-${idx}`;
            chip.onclick = () => selectAddonPax(idx, chip);
            chip.innerHTML = `
                <div class="pax-name">${pax.name} <span>₹<span class="pax-chip-total">${addonCart[idx].total}</span></span></div>
                <div class="pax-subtotal">Cart: <span class="pax-chip-items">${addonCart[idx].items.length}</span> items</div>
            `;
            paxContainer.appendChild(chip);"""

new_chip = """            const chip = document.createElement('div');
            chip.className = `immersive-person-card ${idx === 0 ? 'active' : ''}`;
            chip.id = `addon-person-${idx}`;
            chip.onclick = () => selectAddonPax(idx, chip);
            
            // Extract initials
            let initials = pax.name.substring(0,2).toUpperCase();
            if (pax.name.includes(' ')) {
                const parts = pax.name.split(' ');
                initials = parts[0][0] + (parts[1] ? parts[1][0] : '');
            }
            
            chip.innerHTML = `
                <div class="person-avatar">${initials}</div>
                <div class="person-details">
                    <div class="person-name">${pax.name}</div>
                    <div class="person-cart-status"><span class="addon-badge">₹<span class="pax-chip-total">${addonCart[idx].total}</span></span> &bull; <span class="pax-chip-items">${addonCart[idx].items.length}</span> items</div>
                </div>
            `;
            paxContainer.appendChild(chip);"""

js = js.replace(old_chip, new_chip)

old_select = """function selectAddonPax(index, chipEl) {
    currentAddonPax = index;
    document.querySelectorAll('.dynamic-pax-chip').forEach(c => c.classList.remove('active'));
    chipEl.classList.add('active');
    chipEl.scrollIntoView({ behavior: 'smooth', inline: 'center' });
    triggerHaptic('light', 'Switched passenger');
    
    // Ideally here we would also re-render the buttons to show what THIS passenger has added.
    // For the prototype, we just switch the active visual state.
}"""

new_select = """function selectAddonPax(index, chipEl) {
    currentAddonPax = index;
    document.querySelectorAll('.immersive-person-card').forEach(c => c.classList.remove('active'));
    chipEl.classList.add('active');
    chipEl.scrollIntoView({ behavior: 'smooth', inline: 'center' });
    triggerHaptic('light', 'Switched passenger');
}"""

js = js.replace(old_select, new_select)

with open('app.js', 'w') as f:
    f.write(js)
