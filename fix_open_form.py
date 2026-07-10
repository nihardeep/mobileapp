import re

with open('app.js', 'r') as f:
    js = f.read()

old_logic = """    if (gender === 'Female') selectGender('Female');
    else selectGender('Male');

    const backdrop = document.getElementById('bottomSheetBackdrop');
    const sheet = document.getElementById('passengerFormSheet');
    if (backdrop) backdrop.classList.add('visible');
    if (sheet) sheet.classList.add('visible');
};"""

new_logic = """    if (gender === 'Female') selectGender('Female');
    else selectGender('Male');

    // Dynamic Next Button logic
    const saveBtn = document.getElementById('savePassengerBtn');
    if (saveBtn) {
        const emptyCardsCount = document.querySelectorAll('.passenger-card.empty').length;
        if (emptyCardsCount <= 1) {
            saveBtn.innerText = 'All Done';
        } else {
            saveBtn.innerText = 'Save & Next Passenger';
        }
    }

    const backdrop = document.getElementById('bottomSheetBackdrop');
    const sheet = document.getElementById('passengerFormSheet');
    if (backdrop) backdrop.classList.add('visible');
    if (sheet) sheet.classList.add('visible');
};"""

js = js.replace(old_logic, new_logic)

with open('app.js', 'w') as f:
    f.write(js)
