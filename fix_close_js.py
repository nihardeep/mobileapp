import re

with open('app.js', 'r') as f:
    js = f.read()

# Update closeDestinationAI
new_close = """function closeDestinationAI() {
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

# Actually, my previous code for closeDestinationAI had this:
# function closeDestinationAI() {
#     triggerHaptic('light', 'Close AI Destination');
#     // Remove animate class so they can be re-animated next time
#     const cards = document.querySelectorAll('.ai-flight-card');
#     cards.forEach(card => card.classList.remove('animate-in'));
#     navigateTo('home');
# }

js = re.sub(r'function closeDestinationAI\(\) \{.*?(?=\n\}|\Z)\n\}', new_close, js, flags=re.DOTALL)

with open('app.js', 'w') as f:
    f.write(js)
print("Updated closeDestinationAI logic")
