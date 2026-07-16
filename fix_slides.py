with open('index.html', 'r') as f:
    html = f.read()

# We need to replace tkCity1Code and tkCity2Code for the subsequent slides
# However, they all have the same IDs which is bad HTML (id should be unique).
# The current HTML has id="tkCity1Code" for all slides.
# Let's replace the occurrences sequentially.

parts = html.split('<div class="city-code" id="tkCity1Code">DEL</div>')
if len(parts) == 5:
    html = parts[0] + '<div class="city-code" id="tkCity1Code">DEL</div>' + \
           parts[1] + '<div class="city-code" id="tkCity1Code">BOM</div>' + \
           parts[2] + '<div class="city-code" id="tkCity1Code">GOI</div>' + \
           parts[3] + '<div class="city-code" id="tkCity1Code">BLR</div>' + \
           parts[4]
    
parts = html.split('<div class="city-code" id="tkCity2Code">BOM</div>')
if len(parts) == 5:
    html = parts[0] + '<div class="city-code" id="tkCity2Code">BOM</div>' + \
           parts[1] + '<div class="city-code" id="tkCity2Code">GOI</div>' + \
           parts[2] + '<div class="city-code" id="tkCity2Code">BLR</div>' + \
           parts[3] + '<div class="city-code" id="tkCity2Code">DEL</div>' + \
           parts[4]

with open('index.html', 'w') as f:
    f.write(html)
print("Updated slide destinations")
