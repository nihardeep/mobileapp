import re

with open('app.js', 'r') as f:
    js = f.read()

old_logic = """    // 2. Apply Staggered Stack Entrance (Searching Mode)
    const cards = list.querySelectorAll('.flight-card');
    cards.forEach((card, i) => {
        // Initial hidden state at the bottom
        card.style.opacity = '0';
        card.style.transform = 'translateY(150px) scale(0.9)';
        card.style.position = 'absolute';
        card.style.top = '0';
        card.style.left = '16px';
        card.style.right = '16px';
        card.style.zIndex = 20 - i; // Stack on top of each other
        card.classList.add('shimmering');

        // Phase 1: Fly in to stacked position
        setTimeout(() => {
            card.style.transition = 'all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1)';
            card.style.opacity = '1';
            card.style.transform = `translateY(${i * 12}px) scale(${1 - (i * 0.04)})`;
            triggerHaptic('light', `Flight card ${i} stack`);
        }, 50 + (i * 60));
    });"""

new_logic = """    // 2. Apply Staggered Stack Entrance (Searching Mode)
    const cards = list.querySelectorAll('.flight-card');
    
    // Make list a positioned container so absolute children are placed at the bottom correctly
    list.style.position = 'relative';
    // Center the stack vertically in the viewport initially or just near the bottom
    const topOffset = '200px'; 
    
    cards.forEach((card, i) => {
        // Initial hidden state at the bottom (slide up from off-screen)
        card.style.opacity = '0';
        card.style.transform = 'translateY(100vh) scale(0.9)';
        card.style.position = 'absolute';
        card.style.top = topOffset; 
        card.style.left = '16px';
        card.style.right = '16px';
        card.style.zIndex = 20 - i; // Stack on top of each other
        card.classList.add('shimmering');

        // Phase 1: Fly in to iOS stacked position
        setTimeout(() => {
            card.style.transition = 'all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1)';
            
            if (i === 0) {
                card.style.opacity = '1';
                card.style.transform = `translateY(0px) scale(1)`;
            } else if (i === 1) {
                card.style.opacity = '1';
                card.style.transform = `translateY(-16px) scale(0.95)`;
                card.style.filter = 'brightness(0.9)';
            } else if (i === 2) {
                card.style.opacity = '1';
                card.style.transform = `translateY(-32px) scale(0.90)`;
                card.style.filter = 'brightness(0.8)';
            } else {
                // Hide any cards beyond the 3rd one directly behind the 3rd card
                card.style.opacity = '0';
                card.style.transform = `translateY(-32px) scale(0.90)`;
            }
            
            triggerHaptic('light', `Flight card ${i} stack`);
        }, 50 + (i * 60));
    });"""

js = js.replace(old_logic, new_logic)

# Also need to reset filter in spread phase
old_spread = """            card.style.position = 'relative';
            card.style.top = 'auto';
            card.style.left = 'auto';
            card.style.right = 'auto';
            card.style.zIndex = 'auto';
            
            // Allow CSS flex gap to handle spacing by resetting transform
            card.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
            card.style.transform = 'translateY(0) scale(1)';"""

new_spread = """            card.style.position = 'relative';
            card.style.top = 'auto';
            card.style.left = 'auto';
            card.style.right = 'auto';
            card.style.zIndex = 'auto';
            card.style.filter = 'none';
            card.style.opacity = '1';
            
            // Allow CSS flex gap to handle spacing by resetting transform
            card.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
            card.style.transform = 'translateY(0) scale(1)';"""

js = js.replace(old_spread, new_spread)

with open('app.js', 'w') as f:
    f.write(js)
