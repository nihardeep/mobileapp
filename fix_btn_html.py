with open('index.html', 'r') as f:
    html = f.read()

html = html.replace('<button class="primary-btn" style="width: 100%; padding: 16px; border-radius: 12px; font-size: 16px; font-weight: 800;" onclick="savePassengerForm()">Next</button>',
                    '<button id="savePassengerBtn" class="primary-btn" style="width: 100%; padding: 16px; border-radius: 12px; font-size: 16px; font-weight: 800;" onclick="savePassengerForm()">Save & Next Passenger</button>')

with open('index.html', 'w') as f:
    f.write(html)
