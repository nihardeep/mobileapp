with open('app.js', 'a') as f:
    f.write("""

// Passenger Details: Show Remaining Cards
window.showRemainingCards = function() {
    const btn = document.getElementById('addRemainingBtn');
    if (btn) btn.style.display = 'none';

    // Show cards 6, 7, 8
    for (let i = 6; i <= 8; i++) {
        const card = document.getElementById('passenger-card-' + i);
        if (card) {
            card.style.display = 'flex';
            // Reset animation to ensure stagger effect plays
            card.style.animation = 'none';
            card.offsetHeight; // trigger reflow
            card.style.animation = `staggerFadeIn 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) forwards`;
            card.style.animationDelay = `${(i - 5) * 0.15}s`;
        }
    }
    
    // Update container padding if needed
};
""")
