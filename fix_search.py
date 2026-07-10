with open('app.js', 'r') as f:
    content = f.read()

old = """function searchFlights() {
    if (!appState.selectedFrom) appState.selectedFrom = 'DEL';
    if (!appState.selectedTo) appState.selectedTo = 'BOM';"""

new = """function searchFlights() {
    if (!appState.selectedFrom) appState.selectedFrom = { code: 'DEL', city: 'Delhi' };
    if (!appState.selectedTo) appState.selectedTo = { code: 'BOM', city: 'Mumbai' };"""

if old in content:
    content = content.replace(old, new)
    with open('app.js', 'w') as f:
        f.write(content)
    print("Fixed search flights objects!")
else:
    print("Not found!")
