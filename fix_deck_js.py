import re

with open('app.js', 'r') as f:
    js = f.read()

# 1. Update selectDestination
js = js.replace('const flightList = document.getElementById(\'aiFlightList\');\n    flightList.innerHTML = \'\';', 'const flightList = document.getElementById(\'aiFlightList\');\n    flightList.innerHTML = \'\';\n    flightList.classList.add(\'ios-card-stack\');')
js = js.replace('<div class="ai-flight-card" id="ai-card-${i}">', '<div class="ai-flight-card stacked-card" id="ai-card-${i}">')

# Replace animateFlightCardsUp call with fanOutDeck
js = js.replace('animateFlightCardsUp();', 'fanOutDeck(\'aiFlightList\');')

# 2. Update renderFlightResults
js = js.replace('const list = document.getElementById(\'flightResultsList\');\n    if (!list) return;', 'const list = document.getElementById(\'flightResultsList\');\n    if (!list) return;\n    list.classList.add(\'ios-card-stack\');')
js = js.replace('<div class="flight-card" id="flightCard-${i}">', '<div class="flight-card stacked-card" id="flightCard-${i}">')

# Find the end of renderFlightResults to add fanOutDeck
# It ends with: 
#     setTimeout(() => {
#         document.querySelectorAll('.flight-card').forEach((c, idx) => {
#             setTimeout(() => {
#                 c.classList.add('slide-in');
#                 if (idx % 2 === 0) triggerHaptic('light', 'Card cascade');
#             }, idx * 60);
#         });
#     }, 100);
# }

# We will replace that slide-in logic with fanOutDeck
old_cascade = """    setTimeout(() => {
        document.querySelectorAll('.flight-card').forEach((c, idx) => {
            setTimeout(() => {
                c.classList.add('slide-in');
                if (idx % 2 === 0) triggerHaptic('light', 'Card cascade');
            }, idx * 60);
        });
    }, 100);"""

js = js.replace(old_cascade, "    setTimeout(() => {\n        fanOutDeck('flightResultsList');\n    }, 200);")


# 3. Add fanOutDeck function definition
fan_out_func = """
function fanOutDeck(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const cards = container.querySelectorAll('.stacked-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.remove('stacked-card');
            if (index % 2 === 0) triggerHaptic('light', 'Deck Fan Out');
        }, index * 90); 
    });
}
"""

if "function fanOutDeck" not in js:
    js += fan_out_func

with open('app.js', 'w') as f:
    f.write(js)

print("JS updated for fanOutDeck")
