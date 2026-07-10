import re

with open('app.js', 'r') as f:
    js = f.read()

# 1. Revert selectDestination
js = js.replace('flightList.classList.add(\'ios-card-stack\');', '')
js = js.replace('<div class="ai-flight-card stacked-card" id="ai-card-${i}">', '<div class="ai-flight-card" id="ai-card-${i}">')
js = js.replace('fanOutDeck(\'aiFlightList\');', 'animateFlightCardsUp();')

# 2. Revert renderFlightResults
js = js.replace('list.classList.add(\'ios-card-stack\');', '')
js = js.replace('<div class="flight-card stacked-card" id="flightCard-${i}">', '<div class="flight-card" id="flightCard-${i}">')

old_fan_out_call = """    setTimeout(() => {
        fanOutDeck('flightResultsList');
    }, 200);"""

new_cascade = """    setTimeout(() => {
        document.querySelectorAll('.flight-card').forEach((c, idx) => {
            setTimeout(() => {
                c.classList.add('slide-in');
                if (idx % 2 === 0) triggerHaptic('light', 'Card cascade');
            }, idx * 60);
        });
    }, 100);"""

js = js.replace(old_fan_out_call, new_cascade)

# 3. Revert closeDestinationAI
old_close = """function closeDestinationAI() {
    triggerHaptic('light', 'Close AI Destination');
    // Pause video
    const heroVideo = document.getElementById('aiDestHeroVideo');
    if (heroVideo) {
        heroVideo.pause();
    }
    // Remove animate class so they can be re-animated next time
    const cards = document.querySelectorAll('.stacked-card');
    cards.forEach(card => card.classList.add('stacked-card')); // Wait, if it's already removed? No, when closing we should re-add stacked-card so it stacks next time!
    
    // Actually, fanOutDeck removes stacked-card. So to reset, we must add it back.
    const flightCards = document.querySelectorAll('.ai-flight-card');
    flightCards.forEach(card => {
        card.classList.add('stacked-card');
    });

    navigateTo('home');
}"""

new_close = """function closeDestinationAI() {
    triggerHaptic('light', 'Close AI Destination');
    // Pause video
    const heroVideo = document.getElementById('aiDestHeroVideo');
    if (heroVideo) {
        heroVideo.pause();
    }
    // Remove animate class so they can be re-animated next time
    const cards = document.querySelectorAll('.ai-flight-card');
    cards.forEach(card => card.classList.remove('animate-in'));
    navigateTo('home');
}"""

js = js.replace(old_close, new_close)

with open('app.js', 'w') as f:
    f.write(js)

print("JS reverted")
