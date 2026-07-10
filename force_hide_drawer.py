import re

with open('app.js', 'r') as f:
    js = f.read()

# Forcefully ensure passenger form sheet is dead when navigating to add-ons
old_nav = """    } else if (screenName === 'addons') {
        const addonsScreen = document.getElementById('screenAddons');
        if (addonsScreen) {
            addonsScreen.classList.add('active');
            initAddonsScreen();
        }
    }"""

new_nav = """    } else if (screenName === 'addons') {
        const addonsScreen = document.getElementById('screenAddons');
        if (addonsScreen) {
            addonsScreen.classList.add('active');
            
            // SUPER KILL SWITCH FOR PASSENGER DRAWER
            document.querySelectorAll('.bottom-sheet-drawer').forEach(dr => dr.classList.remove('visible'));
            const bd = document.getElementById('bottomSheetBackdrop');
            if (bd) bd.classList.remove('visible');
            
            initAddonsScreen();
        }
    }"""

js = js.replace(old_nav, new_nav)

with open('app.js', 'w') as f:
    f.write(js)
