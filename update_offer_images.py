import re

with open('style.css', 'r') as f:
    css = f.read()

# Replace local image URLs with high-res Unsplash URLs
css = css.replace(
    "background: url('offer_card_1.png') center center / cover no-repeat !important;",
    "background: url('https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?w=800&h=600&fit=crop&q=80') center center / cover no-repeat !important;"
)

css = css.replace(
    "background: url('offer_card_2.png') center center / cover no-repeat !important;",
    "background: url('https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&h=600&fit=crop&q=80') center center / cover no-repeat !important;"
)

css = css.replace(
    "background: url('offer_card_3.png') center center / cover no-repeat !important;",
    "background: url('https://images.unsplash.com/photo-1540541338287-41700207dee6?w=800&h=600&fit=crop&q=80') center center / cover no-repeat !important;"
)

with open('style.css', 'w') as f:
    f.write(css)

print("Offer images updated to high-res")
