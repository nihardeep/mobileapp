with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Cab Deals order
old_cab = '<div id="companionCabDeals" style="margin-top: 16px; display: none; padding: 0 20px;">'
new_cab = '<div id="companionCabDeals" style="margin-top: 16px; display: none; padding: 0 20px; order: 4;">'
html = html.replace(old_cab, new_cab)

# Fix Hotel Deals order
old_hotel = '<div id="companionHotelDeals" style="margin-top: 16px; display: none; margin-bottom: 24px;">'
new_hotel = '<div id="companionHotelDeals" style="margin-top: 16px; display: none; margin-bottom: 24px; order: 5;">'
html = html.replace(old_hotel, new_hotel)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated order in index.html")
