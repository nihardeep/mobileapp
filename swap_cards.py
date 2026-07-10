with open('index.html', 'r') as f:
    text = f.read()

# Hide loyalUserCard
target_loyal = '<div class="bluchip-3d-wrapper" id="loyalUserCard" style="position: relative; perspective: 1500px; margin-bottom: 24px;">'
replace_loyal = '<div class="bluchip-3d-wrapper" id="loyalUserCard" style="position: relative; perspective: 1500px; margin-bottom: 24px; display: none;">'

# Show newUserCard
target_new = '<div class="bluchip-3d-wrapper" id="newUserCard" style="position: relative; perspective: 1500px; display: none;">'
replace_new = '<div class="bluchip-3d-wrapper" id="newUserCard" style="position: relative; perspective: 1500px;">'

text = text.replace(target_loyal, replace_loyal)
text = text.replace(target_new, replace_new)

with open('index.html', 'w') as f:
    f.write(text)

print("Swapped cards!")
