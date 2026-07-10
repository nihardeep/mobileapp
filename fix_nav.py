import re

with open('app.js', 'r') as f:
    js = f.read()

# Add studentHub logic to navigateTo function
old_nav = """    } else if (screenName === 'results') {
        const resultsScreen = document.getElementById('screenResults');
        if (resultsScreen) resultsScreen.classList.add('active');
        // Keep flights tab semi-active or no tab active to focus on results
        renderFlightResults();
    }"""

new_nav = """    } else if (screenName === 'results') {
        const resultsScreen = document.getElementById('screenResults');
        if (resultsScreen) resultsScreen.classList.add('active');
        // Keep flights tab semi-active or no tab active to focus on results
        renderFlightResults();
    } else if (screenName === 'studentHub') {
        const studentScreen = document.getElementById('screenStudentHub');
        if (studentScreen) studentScreen.classList.add('active');
    }"""

if "screenName === 'studentHub'" not in js:
    js = js.replace(old_nav, new_nav)
    with open('app.js', 'w') as f:
        f.write(js)
    print("Fixed navigateTo logic!")
else:
    print("Already fixed.")
