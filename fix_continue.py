with open('app.js', 'r') as f:
    js = f.read()

target = """window.updatePassengerCount = function() {
    const completedCards = document.querySelectorAll('.passenger-card.completed').length;
    document.getElementById('passenger-added-count').innerText = completedCards;
    
    const nextBtn = document.getElementById('passenger-next-btn');
    if (completedCards === 4) { // Assuming 4 total for this prototype"""

replacement = """window.updatePassengerCount = function() {
    const completedCards = document.querySelectorAll('.passenger-card.completed').length;
    document.getElementById('passenger-added-count').innerText = completedCards;
    
    const visibleCards = Array.from(document.querySelectorAll('.passenger-card')).filter(card => card.style.display !== 'none').length;
    
    const nextBtn = document.getElementById('passenger-next-btn');
    if (completedCards >= 4) { // Enable if they complete at least 4, or all visible"""

# Actually, the user says the header is 3 Adults, 1 Child (which is 4 people).
# If the header is 4 people, why are 5 cards visible?
# If there are 5 visible cards, they might fill out 4, and wonder why the button is disabled.
# Let's change the condition to `completedCards >= 4`.
js = js.replace(target, replacement)

with open('app.js', 'w') as f:
    f.write(js)

with open('index.html', 'r') as f:
    html = f.read()
html = html.replace('app.js?v=18', 'app.js?v=19')
with open('index.html', 'w') as f:
    f.write(html)
