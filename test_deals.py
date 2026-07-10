with open('index.html', 'r') as f:
    content = f.read()

start = content.find('<!-- COMPANION CAB DEALS -->')
hotel_start = content.find('<!-- COMPANION HOTEL DEALS -->', start)
if start != -1:
    print("Found Cab Deals at", start)
else:
    print("Cab Deals not found (maybe they were moved!)")
