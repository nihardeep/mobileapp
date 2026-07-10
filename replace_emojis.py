import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_sandwich = '<span style="font-size: 20px;">🥪</span>'
new_sandwich = '<img src="sandwich.png" style="width: 38px; height: 38px; border-radius: 50%; object-fit: cover;" alt="Sandwich"/>'

old_seat = '<span style="font-size: 28px;">💺</span>'
new_seat = '<img src="seat.png" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" alt="Seat"/>'

content = content.replace(old_sandwich, new_sandwich)
content = content.replace(old_seat, new_seat)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Emojis replaced with images.")
