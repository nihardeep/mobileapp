import re

with open('style.css', 'r') as f:
    css = f.read()

# 1. Update the gradient ring to light blue
css = css.replace('linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%)', 'linear-gradient(45deg, #00d2ff 0%, #3a7bd5 100%)')

# 2. Add styles for insta-card-video
video_styles = """
.insta-card-video {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 0;
}
.insta-story-overlay, .insta-play-ring {
    z-index: 1;
}
"""

if "insta-card-video" not in css:
    css += video_styles

# 3. Ensure insta-stories-scroll is scrollable by forcing it to take 100vw or just full width
# It already has display: flex; overflow-x: auto; but we can make sure it spans the width.
css = css.replace('.insta-stories-scroll {\n    display: flex;', '.insta-stories-scroll {\n    display: flex;\n    width: 100vw;\n    margin-left: -16px; /* pull it out of padding */\n    padding-left: 16px;\n    padding-right: 16px;')

with open('style.css', 'w') as f:
    f.write(css)

print("CSS updated")
