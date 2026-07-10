with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix the taxi size and position to avoid overlapping the coupon
old_taxi = 'width: 155px; z-index: 1; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.3));"'
new_taxi = 'width: 135px; z-index: 1; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.3)); right: -5px;"'
html = html.replace(old_taxi, new_taxi)

# Wait, the old taxi tag had `right: -15px; bottom: -15px;` in it. Let's do a proper string replace.
old_taxi_full = '<img src="https://pngimg.com/uploads/taxi/taxi_PNG74.png" alt="Taxi" style="position: absolute; right: -15px; bottom: -15px; width: 155px; z-index: 1; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.3));" />'
new_taxi_full = '<img src="https://pngimg.com/uploads/taxi/taxi_PNG74.png" alt="Taxi" style="position: absolute; right: -15px; bottom: -12px; width: 135px; z-index: 1; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.3));" />'
html = html.replace(old_taxi_full, new_taxi_full)

# 2. Move arrow closer to the corner (right extreme)
old_arrow = '<div style="position: absolute; right: 12px; top: 12px; z-index: 3; background: #fff; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">'
new_arrow = '<div style="position: absolute; right: 8px; top: 8px; z-index: 3; background: #fff; border-radius: 50%; width: 26px; height: 26px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">'
html = html.replace(old_arrow, new_arrow)

# 3. Add left extreme arrow in case they REALLY wanted it on the left (maybe above the keychain?)
# Let's ask them if they meant right or left, but for now just move it to top right.
# Wait, "a liitle above on left extreme corner". If the arrow is currently on the right, and they want it on the left...
# Why would they want an arrow on the left? The chevron points right (>), meaning "go to cab deals". Usually that's on the right.
# Maybe they want it on the right extreme corner.

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
