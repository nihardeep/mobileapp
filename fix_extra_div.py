with open('index.html', 'r') as f:
    html = f.read()

# The extra div is right after the closing div of travelersSheetDrawer
target = """                    <button class="confirm-travelers-btn" onclick="confirmTravelers()">Confirm</button>
                </div>

            </div>"""

replacement = """                    <button class="confirm-travelers-btn" onclick="confirmTravelers()">Confirm</button>
                </div>"""

if target in html:
    html = html.replace(target, replacement, 1)
    with open('index.html', 'w') as f:
        f.write(html)
    print("Fixed extra div!")
else:
    print("Target not found!")
