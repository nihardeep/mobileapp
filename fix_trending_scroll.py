import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace <div class="insta-stories-scroll"> with carousel containers
new_scroll_start = """                                <div class="carousel-container" id="trendingInstaContainer">
                                    <div class="carousel-3d-track" id="trendingInstaCarousel">"""

html = html.replace('<div class="insta-stories-scroll">', new_scroll_start)

# Add dots before explore-all-text
dots_html = """                                    </div>
                                </div>
                                <div class="carousel-dots" id="trendingInstaDots">
                                    <div class="dot active"></div>
                                    <div class="dot"></div>
                                    <div class="dot"></div>
                                    <div class="dot"></div>
                                    <div class="dot"></div>
                                </div>"""

html = html.replace('                                </div>\n                                <div class="explore-all-text"', dots_html + '\n                                <div class="explore-all-text"')

# Add carousel-slide class to the cards
html = html.replace('class="insta-story-card"', 'class="insta-story-card carousel-slide"')

with open('index.html', 'w') as f:
    f.write(html)
print("HTML updated to use 3D carousel structure")
