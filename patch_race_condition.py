import re

with open('app.js', 'r') as f:
    js = f.read()

# Fix race condition in savePassengerForm
old_timeout = """    // AUTO-ADVANCE: Find the next empty passenger and open it
    setTimeout(() => {
        const nextEmpty = document.querySelector('.passenger-card.empty');
        if (nextEmpty) {
            nextEmpty.click(); // Programmatically click the next empty card to open its form
        }
    }, 400);"""

new_timeout = """    // AUTO-ADVANCE: Find the next empty passenger and open it
    setTimeout(() => {
        const nextEmpty = document.querySelector('.passenger-card.empty');
        if (nextEmpty && appState.currentScreen === 'passenger') {
            nextEmpty.click(); // Programmatically click the next empty card to open its form
        }
    }, 400);"""

js = js.replace(old_timeout, new_timeout)

# Add explicit hide for passenger drawer in initAddonsScreen just to be ultra safe
js = js.replace('function initAddonsScreen() {\\n    closeAllDrawers();', 'function initAddonsScreen() {\\n    closeAllDrawers();\\n    document.getElementById("passengerFormSheet").classList.remove("visible");\\n    document.getElementById("bottomSheetBackdrop").classList.remove("visible");')

with open('app.js', 'w') as f:
    f.write(js)
