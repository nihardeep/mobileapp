import re

with open('app.js', 'r') as f:
    js = f.read()

# Replace the search logic in renderFlightResults
old_search_logic = """    // 2. Apply Staggered Stack Entrance (Searching Mode)
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
    });

    // 3. Spread Phase: Unstack into scrollable list after "Search" completes
    setTimeout(() => {
        list.classList.remove('searching-mode');
        
        cards.forEach((card, i) => {
            card.classList.remove('shimmering');
            card.style.position = 'relative';
            card.style.top = 'auto';
            card.style.left = 'auto';
            card.style.right = 'auto';
            card.style.zIndex = 'auto';
            card.style.filter = 'none';
            card.style.opacity = '1';
            
            // Allow CSS flex gap to handle spacing by resetting transform
            card.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
            card.style.transform = 'translateY(0) scale(1)';
        });"""

new_search_logic = """    // 2. Best Practice: CSS-driven Stack Entrance
    list.classList.add('searching-mode');
    
    // We will use standard relative positioning but with negative margins to stack them elegantly
    // without breaking the DOM flow (which causes layout snaps when switching from absolute).
    const cards = list.querySelectorAll('.flight-card');
    
    cards.forEach((card, i) => {
        card.classList.add('shimmering');
        
        // Initial state: way off screen bottom
        card.style.transform = 'translateY(100vh) scale(0.8)';
        card.style.opacity = '0';
        card.style.transition = 'all 0.6s cubic-bezier(0.25, 1, 0.5, 1)';
        card.style.zIndex = 20 - i;
        
        // Force the stack overlap using negative margin for all but the first card
        if (i > 0) {
            card.style.marginTop = '-180px'; // overlap heavily
        }
        
        // Phase 1: Slide up into the iOS stack
        setTimeout(() => {
            if (i === 0) {
                card.style.transform = `translateY(0px) scale(1)`;
                card.style.opacity = '1';
            } else if (i === 1) {
                card.style.transform = `translateY(-16px) scale(0.95)`;
                card.style.opacity = '1';
                card.style.filter = 'brightness(0.9)';
            } else if (i === 2) {
                card.style.transform = `translateY(-32px) scale(0.90)`;
                card.style.opacity = '1';
                card.style.filter = 'brightness(0.8)';
            } else {
                card.style.transform = `translateY(-32px) scale(0.90)`;
                card.style.opacity = '0';
            }
            if (i < 3) triggerHaptic('light', `Stack entry ${i}`);
        }, 50 + (i * 80));
    });

    // 3. Unfurl Phase: Smoothly transition out of the stack
    setTimeout(() => {
        list.classList.remove('searching-mode');
        
        cards.forEach((card, i) => {
            card.classList.remove('shimmering');
            card.style.filter = 'none';
            card.style.opacity = '1';
            
            // Removing the negative margin smoothly unfurls them natively in the flex container!
            card.style.marginTop = '0px';
            card.style.transform = 'translateY(0) scale(1)';
        });"""

js = js.replace(old_search_logic, new_search_logic)

with open('app.js', 'w') as f:
    f.write(js)
