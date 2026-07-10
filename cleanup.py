with open('index.html', 'r') as f:
    html = f.read()

# remove planeTransitionOverlay div
start = html.find('<div class="plane-transition-overlay" id="planeTransitionOverlay">')
if start != -1:
    end = html.find('</div>', html.find('</svg>', start)) + 6
    html = html[:start] + html[end:]

with open('index.html', 'w') as f:
    f.write(html)
