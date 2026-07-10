import re

with open('app.js', 'r') as f:
    js = f.read()

# 1. Update renderPopupCards to target cp-carousel and inject padders directly
old_render = "const track = document.getElementById('cp-track');\n    let html = '';"
new_render = "const track = document.getElementById('cp-carousel');\n    let html = '<div class=\"cp-carousel-padder\"></div>';"

js = js.replace(old_render, new_render)

old_track_inner = "track.innerHTML = html;"
new_track_inner = "html += '<div class=\"cp-carousel-padder\"></div>';\n    track.innerHTML = html;"

js = js.replace(old_track_inner, new_track_inner)

# 2. Update openCompareFaresModal to close popup
old_compare = """window.openCompareFaresModal = function(event, className) {
    if (event) event.stopPropagation();
    
    const modal = document.getElementById('compareFaresModal');"""
    
new_compare = """window.openCompareFaresModal = function(event, className) {
    if (event) event.stopPropagation();
    
    closeFarePopup();
    
    const modal = document.getElementById('compareFaresModal');"""

js = js.replace(old_compare, new_compare)

with open('app.js', 'w') as f:
    f.write(js)

print("Fixed JS logic")

# 3. Update index.html to remove cp-track
with open('index.html', 'r') as f:
    html = f.read()

# Remove the track and padders from index.html (they will be injected by JS now)
track_html = """                            <div class="cp-carousel-padder"></div>
                            <div class="cp-carousel-track" id="cp-track">
                                <!-- Cards injected here -->
                            </div>
                            <div class="cp-carousel-padder"></div>"""

html = html.replace(track_html, "                            <!-- Cards injected here directly by JS -->")

with open('index.html', 'w') as f:
    f.write(html)

print("Fixed HTML structure")
