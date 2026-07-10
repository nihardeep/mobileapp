import re

with open('app.js', 'r') as f:
    js = f.read()

new_clause = """    } else if (screenName === 'DestinationAI') {
        const aiScreen = document.getElementById('screenDestinationAI');
        if (aiScreen) aiScreen.classList.add('active');
    }"""

js = js.replace("    } else if (screenName === 'results') {", new_clause + "\n    } else if (screenName === 'results') {")

with open('app.js', 'w') as f:
    f.write(js)
