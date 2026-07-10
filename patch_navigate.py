import re

with open('app.js', 'r') as f:
    js = f.read()

# Add screenPassenger logic to navigateTo
old_code = """    } else if (screenName === 'addons') {"""

new_code = """    } else if (screenName === 'passenger') {
        const passengerScreen = document.getElementById('screenPassenger');
        if (passengerScreen) passengerScreen.classList.add('active');
    } else if (screenName === 'addons') {"""

js = js.replace(old_code, new_code)

with open('app.js', 'w') as f:
    f.write(js)
