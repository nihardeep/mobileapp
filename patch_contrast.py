import re

# 1. Update style.css
with open('style.css', 'r') as f:
    css = f.read()

# Change lowest-fare colors from green to gold/yellow so it contrasts with light blue
old_lowest_chip = """.pass-chip.lowest-fare {
    border-color: rgba(16, 185, 129, 0.3);
    background: rgba(16, 185, 129, 0.08);
}

.pass-chip.lowest-fare .pass-chip-price {
    color: #10b981; /* Green cheapest rate */
}"""

new_lowest_chip = """.pass-chip.lowest-fare {
    border-color: rgba(255, 209, 92, 0.6);
    background: rgba(255, 209, 92, 0.15);
}

.pass-chip.lowest-fare .pass-chip-price {
    color: #ffd15c; /* Gold cheapest rate */
}"""

css = css.replace(old_lowest_chip, new_lowest_chip)

with open('style.css', 'w') as f:
    f.write(css)

# 2. Update app.js for opacity
with open('app.js', 'r') as f:
    js = f.read()

js = js.replace('opacity: 0.6;', 'opacity: 0.9;')

with open('app.js', 'w') as f:
    f.write(js)

