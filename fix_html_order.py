with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove home-bottom-content wrapper
html = html.replace('<div class="home-bottom-content" id="homeBottomContent">\n', '')
html = html.replace('</div><!-- end home-bottom-content -->\n', '')

# 2. Add inline style "order: 3;" to tripCompanionPlaceholder and homeFlightStateWrapper
# tripCompanionPlaceholder already has inline styles. We'll inject 'order: 3;'
html = html.replace('id="tripCompanionPlaceholder" style="', 'id="tripCompanionPlaceholder" style="order: 3; ')

# homeFlightStateWrapper also has inline styles.
html = html.replace('id="homeFlightStateWrapper" style="', 'id="homeFlightStateWrapper" style="order: 3; ')

with open('index.html', 'w') as f:
    f.write(html)
