with open('index.html', 'r') as f:
    html = f.read()

print("Offers Carousel snippet:")
idx = html.find('<!-- Slide 2: Save ₹400 per person -->')
if idx != -1:
    print(html[max(0, idx-500):idx+200])

