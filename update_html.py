with open('index.html', 'r') as f:
    html = f.read()

# Add a placeholder div right before homeFlightStateWrapper
placeholder = """
<div id="tripCompanionPlaceholder" style="height: 0; overflow: hidden; position: relative; transition: height 0.4s ease; margin-bottom: 0;">
    <svg id="inlinePlaneIcon" viewBox="0 0 24 24" width="32" height="32" fill="var(--indigo-blue)" style="position: absolute; top: 50%; left: -50px; transform: translateY(-50%) rotate(90deg); transition: left 1s cubic-bezier(0.4, 0, 0.2, 1);">
        <path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L14 19v-5.5l8 2.5z"/>
    </svg>
</div>
"""

# Insert placeholder right before homeFlightStateWrapper
wrapper_idx = html.find('<div class="flight-state-wrapper" id="homeFlightStateWrapper"')
html = html[:wrapper_idx] + placeholder + html[wrapper_idx:]

with open('index.html', 'w') as f:
    f.write(html)
