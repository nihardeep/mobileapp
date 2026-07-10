import re

with open('app.js', 'r') as f:
    js = f.read()

# Make sure passengerFormSheet is hidden when not on passenger screen
old_nav = """    } else if (screenName === 'addons') {"""

new_nav = """    
    // Globally hide passenger form when navigating away from passenger screen
    const pForm = document.getElementById('passengerFormSheet');
    if (pForm) {
        if (screenName === 'passenger') {
            pForm.style.display = 'block';
        } else {
            pForm.style.display = 'none';
        }
    }
    
    if (screenName === 'addons') {"""

js = js.replace(old_nav, new_nav)

with open('app.js', 'w') as f:
    f.write(js)
