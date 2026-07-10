import re

with open('app.js', 'r') as f:
    js = f.read()

# Replace the search logic in renderFlightResults
old_search_logic = """    // 2. Best Practice: CSS-driven Stack Entrance
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

new_search_logic = """    // 2. Standard Staggered List Entrance
    const cards = list.querySelectorAll('.flight-card');
    
    cards.forEach((card, i) => {
        card.classList.add('shimmering');
        
        // Initial state: hidden and slightly pushed down
        card.style.transform = 'translateY(30px)';
        card.style.opacity = '0';
        card.style.transition = 'all 0.4s ease-out';
        
        // Staggered slide in
        setTimeout(() => {
            card.style.transform = 'translateY(0)';
            card.style.opacity = '1';
            if (i < 5) triggerHaptic('light', `Card entry ${i}`);
        }, 50 + (i * 100)); // 100ms delay between each card
    });

    // 3. Reveal Phase: Remove shimmer skeleton
    setTimeout(() => {
        cards.forEach((card, i) => {
            card.classList.remove('shimmering');
        });"""

js = js.replace(old_search_logic, new_search_logic)

with open('app.js', 'w') as f:
    f.write(js)
