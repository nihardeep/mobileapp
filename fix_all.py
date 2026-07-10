import re

# 1. Update savePassengerForm in app.js to auto-open next
with open('app.js', 'r') as f:
    js = f.read()

target_js = """        closeAllDrawers();
        updatePassengerCount();
    }
};"""

replacement_js = """        closeAllDrawers();
        updatePassengerCount();
        
        // Auto-open next empty passenger
        setTimeout(() => {
            const nextEmpty = document.querySelector('.passenger-card.empty');
            if (nextEmpty) {
                nextEmpty.click();
            }
        }, 400);
    }
};"""

js = js.replace(target_js, replacement_js)

with open('app.js', 'w') as f:
    f.write(js)

# 2. Update z-index in style.css
with open('style.css', 'r') as f:
    css = f.read()

css = css.replace("z-index: 990;", "z-index: 99998;")
css = css.replace("z-index: 1000;", "z-index: 99999;")

with open('style.css', 'w') as f:
    f.write(css)

# 3. Update index.html z-index
with open('index.html', 'r') as f:
    html = f.read()

html = html.replace('z-index: 9999;', 'z-index: 999999;')
# Ensure pointer-events: none on passenger-add-btn so it doesn't trap clicks
html = html.replace('class="passenger-add-btn" style="', 'class="passenger-add-btn" style="pointer-events: none; ')

with open('index.html', 'w') as f:
    f.write(html)

