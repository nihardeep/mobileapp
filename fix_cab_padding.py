import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Cab Image position
content = content.replace(
    '<img src="https://pngimg.com/uploads/taxi/taxi_PNG74.png" alt="Taxi" style="position: absolute; right: -15px; bottom: -5px; width: 145px; z-index: 1; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.3));" />',
    '<img src="https://pngimg.com/uploads/taxi/taxi_PNG74.png" alt="Taxi" style="position: absolute; right: 0px; bottom: -5px; width: 145px; z-index: 1; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.3));" />'
)

# Fix Text padding
content = content.replace(
    '<div style="flex: 1; padding-left: 70px; padding-right: 60px; z-index: 3; position: relative;">',
    '<div style="flex: 1; padding-left: 50px; padding-right: 80px; z-index: 3; position: relative;">'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated cab padding")
