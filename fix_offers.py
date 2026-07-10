import re

with open('style.css', 'r') as f:
    css = f.read()

# Fix the CSS syntax for the backgrounds
css = css.replace(
    "background: url('https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?w=800&h=600&fit=crop&q=80') center center / cover no-repeat !important;",
    "background-image: url('https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?w=800&h=600&fit=crop&q=80') !important; background-size: cover !important; background-position: center !important;"
)

css = css.replace(
    "background: url('https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&h=600&fit=crop&q=80') center center / cover no-repeat !important;",
    "background-image: url('https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&h=600&fit=crop&q=80') !important; background-size: cover !important; background-position: center !important;"
)

css = css.replace(
    "background: url('https://images.unsplash.com/photo-1540541338287-41700207dee6?w=800&h=600&fit=crop&q=80') center center / cover no-repeat !important;",
    "background-image: url('https://images.unsplash.com/photo-1540541338287-41700207dee6?w=800&h=600&fit=crop&q=80') !important; background-size: cover !important; background-position: center !important;"
)

# Add CSS for the text overlay
overlay_css = """
.offer-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 40px 16px 16px 16px;
    background: linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0) 100%);
    color: white;
    text-align: left;
}
.offer-title {
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 4px;
}
.offer-subtitle {
    font-size: 13px;
    font-weight: 500;
    opacity: 0.9;
}
"""

if ".offer-overlay" not in css:
    css += "\n" + overlay_css

with open('style.css', 'w') as f:
    f.write(css)


# Now update index.html
with open('index.html', 'r') as f:
    html = f.read()

slide_1_new = """<div class="carousel-slide offers-slide-1" onclick="triggerHaptic('medium', 'Book Weekend Exclusives'); alert('Redirecting to Weekend Exclusives flight search...')">
                                            <div class="offer-overlay">
                                                <div class="offer-title">Weekend Exclusives</div>
                                                <div class="offer-subtitle">Book your perfect getaway now</div>
                                            </div>
                                        </div>"""

slide_2_new = """<div class="carousel-slide offers-slide-2" onclick="triggerHaptic('medium', 'Save 400 Offer'); alert('Redirecting to Save ₹400 flight offer search...')">
                                            <div class="offer-overlay">
                                                <div class="offer-title">Save ₹400 per person</div>
                                                <div class="offer-subtitle">Use code INDIGO400 on domestic flights</div>
                                            </div>
                                        </div>"""

slide_3_new = """<div class="carousel-slide offers-slide-3" onclick="triggerHaptic('medium', 'Up to 5000 Off'); alert('Redirecting to flight offers page...')">
                                            <div class="offer-overlay">
                                                <div class="offer-title">Up to ₹5,000 Off</div>
                                                <div class="offer-subtitle">On your next international vacation</div>
                                            </div>
                                        </div>"""

html = re.sub(r'<div class="carousel-slide offers-slide-1" onclick=".*?">\s*</div>', slide_1_new, html)
html = re.sub(r'<div class="carousel-slide offers-slide-2" onclick=".*?">\s*</div>', slide_2_new, html)
html = re.sub(r'<div class="carousel-slide offers-slide-3" onclick=".*?">\s*</div>', slide_3_new, html)

with open('index.html', 'w') as f:
    f.write(html)

print("Fixed CSS and added HTML text overlays")
