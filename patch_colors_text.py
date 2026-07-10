import re

# 1. Update style.css
with open('style.css', 'r') as f:
    css = f.read()

# Change border
css = css.replace('border: 1.5px solid #001b94;', 'border: 1.5px solid #0ea5e9;')
# Change expanded gradient
css = css.replace('background: linear-gradient(135deg, #001b94 0%, #00105c 100%);', 'background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);')
# Change border-color of expanded
css = css.replace('border-color: #001b94;', 'border-color: #0ea5e9;')
# The unexpanded text is dark blue. Maybe keep it or change to light blue?
# ".pass-header { ... color: #001b94; " -> "#0ea5e9"
css = css.replace('color: #001b94;', 'color: #0ea5e9;')

with open('style.css', 'w') as f:
    f.write(css)

# 2. Update index.html
with open('index.html', 'r') as f:
    html = f.read()

html = html.replace('>BOARDING PASS<', '>INDIGO DEALS<')

with open('index.html', 'w') as f:
    f.write(html)

# 3. Update app.js
with open('app.js', 'r') as f:
    js = f.read()

old_calendar = """        chip.innerHTML = `
            <span class="pass-chip-date">${fare.date}</span>
            <span class="pass-chip-price">${fare.display}</span>
        `;"""

new_calendar = """        const originalPrice = fare.price;
        const discountedPrice = Math.floor(originalPrice * 0.9);
        const originalDisplay = `₹${originalPrice.toLocaleString('en-IN')}`;
        const discountedDisplay = `₹${discountedPrice.toLocaleString('en-IN')}`;
        
        chip.innerHTML = `
            <span class="pass-chip-date">${fare.date}</span>
            <span class="pass-chip-price" style="display: flex; flex-direction: column; align-items: center; gap: 2px;">
                <span style="text-decoration: line-through; opacity: 0.6; font-size: 8px; font-weight: 500;">${originalDisplay}</span>
                <span>${discountedDisplay}</span>
            </span>
        `;"""

js = js.replace(old_calendar, new_calendar)

with open('app.js', 'w') as f:
    f.write(js)

