import re

with open('app.js', 'r') as f:
    js = f.read()

old_logic = """    const savedPaxSheet = document.getElementById('savedPassengersSheet');
    if (savedPaxSheet) {
        if (screenName === 'passenger') {
            savedPaxSheet.style.display = 'block';
        } else {
            savedPaxSheet.style.display = 'none';
        }
    }"""

new_logic = """    const savedPaxSheet = document.getElementById('savedPassengersSheet');
    if (savedPaxSheet) {
        if (screenName === 'passenger') {
            savedPaxSheet.style.display = 'block';
        } else {
            savedPaxSheet.style.display = 'none';
        }
    }
    
    const travelersSheet = document.getElementById('travelersSheetDrawer');
    if (travelersSheet) {
        if (screenName === 'home') {
            travelersSheet.style.display = 'block';
        } else {
            travelersSheet.style.display = 'none';
        }
    }"""

js = js.replace(old_logic, new_logic)

with open('app.js', 'w') as f:
    f.write(js)
