import re

with open('app.js', 'r') as f:
    js = f.read()

# Make sure savedPassengersSheet is hidden when not on passenger screen
old_pform = """    // Globally hide passenger form when navigating away from passenger screen
    const pForm = document.getElementById('paxDetailsDrawerModal');
    if (pForm) {
        if (screenName === 'passenger') {
            pForm.style.display = 'block';
        } else {
            pForm.style.display = 'none';
        }
    }"""

new_pform = """    // Globally hide passenger form when navigating away from passenger screen
    const pForm = document.getElementById('paxDetailsDrawerModal');
    if (pForm) {
        if (screenName === 'passenger') {
            pForm.style.display = 'block';
        } else {
            pForm.style.display = 'none';
        }
    }
    
    const savedPaxSheet = document.getElementById('savedPassengersSheet');
    if (savedPaxSheet) {
        if (screenName === 'passenger') {
            savedPaxSheet.style.display = 'block';
        } else {
            savedPaxSheet.style.display = 'none';
        }
    }"""

js = js.replace(old_pform, new_pform)

with open('app.js', 'w') as f:
    f.write(js)
