with open('index.html', 'r') as f:
    html = f.read()

start_idx = html.find('<!-- Loyalty Panel (IndiGo BluChip balance) -->')
end_idx = html.find('<!-- Offers Carousel (Not business as usual slides) -->')

print(f"Loyalty Panel length: {end_idx - start_idx}")
# Check if the toggle is really there
if "toggleLoyaltyState()" in html:
    print("toggleLoyaltyState() is bound in HTML")
else:
    print("toggleLoyaltyState() NOT found in HTML!")

