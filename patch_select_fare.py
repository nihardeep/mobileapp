import re

with open('app.js', 'r') as f:
    js = f.read()

# Replace selectBoardingPassDate logic
old_select_logic = """function selectBoardingPassDate(code, index) {
    selectedTapFareIndex = index;
    const dest = travelOnTapData[code];
    if (!dest) return;
    const fare = dest.fares[index];
    
    triggerHaptic('success', `Ticket preselected: Delhi to ${dest.name} on ${fare.date}`);
    
    // Re-render chips to update visual selected state
    renderBoardingPassCalendar(code);
    
    // Auto-fill Search Widget parameters:
    // 1. Origin (Delhi - DEL)
    const originAp = airports.find(ap => ap.code === 'DEL');
    if (originAp) {
        appState.selectedFrom = originAp;
        document.getElementById('valFromCode').innerText = originAp.city;
        
        // Trigger DEL layout shifts (Trending destinations slides up)
        const homeContent = document.getElementById('homeContentContainer');
        if (homeContent) {
            homeContent.classList.add('route-selected');
            document.getElementById('userGreeting').innerText = 'Delhi';
        }
    }

    // 2. Destination
    const destAp = airports.find(ap => ap.code === code);
    if (destAp) {
        appState.selectedTo = destAp;
        document.getElementById('valToCode').innerText = destAp.city;
    }
    
    // 3. Date
    appState.departureDate = fare.date;
    document.getElementById('valDepDate').innerHTML = `<strong>${fare.date.split(' ')[0]}</strong> <span style="font-size: 10px;">${fare.date.split(' ')[1]}</span>`;
}"""

new_select_logic = """function selectBoardingPassDate(code, index) {
    selectedTapFareIndex = index;
    const dest = travelOnTapData[code];
    if (!dest) return;
    const fare = dest.fares[index];
    
    triggerHaptic('success', `Ticket preselected: Delhi to ${dest.name} on ${fare.date}`);
    
    // Auto-fill Search Widget parameters silently without triggering massive layout shifts
    // 1. Origin (Delhi - DEL)
    const originAp = airports.find(ap => ap.code === 'DEL');
    if (originAp) {
        appState.selectedFrom = originAp;
        document.getElementById('valFromCode').innerText = originAp.city;
    }

    // 2. Destination
    const destAp = airports.find(ap => ap.code === code);
    if (destAp) {
        appState.selectedTo = destAp;
        document.getElementById('valToCode').innerText = destAp.city;
    }
    
    // 3. Date
    appState.departureDate = fare.date;
    document.getElementById('valDepDate').innerHTML = `<strong>${fare.date.split(' ')[0]}</strong> <span style="font-size: 10px;">${fare.date.split(' ')[1]}</span>`;
    
    // Update visual selected state without re-rendering the whole scroll container
    const container = document.getElementById(`passCalendar${code}`);
    if (container) {
        const chips = container.querySelectorAll('.pass-chip');
        chips.forEach(c => c.classList.remove('selected-fare'));
        if (chips[index]) {
            chips[index].classList.add('selected-fare');
        }
    }
}"""

js = js.replace(old_select_logic, new_select_logic)

with open('app.js', 'w') as f:
    f.write(js)
