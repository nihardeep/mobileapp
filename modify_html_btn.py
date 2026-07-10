with open('index.html', 'r') as f:
    html = f.read()

html = html.replace('id="devNavTrips" onclick="navigateTo(\'trips\')"', 'id="devNavTrips" onclick="triggerHomepageCompanion()"')

with open('index.html', 'w') as f:
    f.write(html)
