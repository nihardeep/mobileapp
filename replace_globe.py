import re

with open('world_map.svg', 'r') as f:
    svg_content = f.read()

# Add styling directly to SVG to be safe, though we will also use CSS
# The user wants "make the bakground whitel and map lines in blue"
svg_content = svg_content.replace('<svg class="flat-world-map"', '<svg class="flat-world-map" style="width: 100%; height: auto; display: block;" ')
# We will target all paths via CSS

with open('index.html', 'r') as f:
    html = f.read()

# Extract and remove the globe-sphere-wrapper
globe_wrapper_regex = r'<div class="globe-sphere-wrapper">.*?</div>\s*</div>\s*</div>'
# Wait, the globe-sphere-wrapper structure:
# <div class="globe-sphere-wrapper">
#    <div class="globe-sphere" id="globeSphere">
#       <div class="globe-texture"...></div>
#       <div class="globe-inner-shadow"></div>
#       <div class="globe-atmosphere-glow"></div>
#    </div>
# </div>
globe_regex = r'<div class="globe-sphere-wrapper">.*?<div class="globe-atmosphere-glow"></div>\s*</div>\s*</div>'
match = re.search(globe_regex, html, re.DOTALL)

if match:
    flat_map_html = f"""
        <div class="flat-map-wrapper" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #ffffff; display: flex; align-items: center; justify-content: center; overflow: hidden; border-radius: 24px;">
            {svg_content}
        </div>
    """
    html = html.replace(match.group(0), flat_map_html)
    
    # We should also ensure the globe-map-container doesn't have styling that breaks the flat map
    # We'll adjust CSS for that
else:
    print("Could not find globe-sphere-wrapper!")

with open('index.html', 'w') as f:
    f.write(html)


with open('style.css', 'r') as f:
    css = f.read()

# Append flat map styles
flat_map_css = """
/* Flat Map Styles */
.flat-map-wrapper {
    z-index: 1;
}

.flat-world-map path {
    fill: #f0f4f8;
    stroke: var(--indigo-blue);
    stroke-width: 0.5px;
    transition: fill 0.3s ease;
}

.flat-world-map path:hover {
    fill: #e1ebf5;
}

.globe-map-container {
    background: #ffffff !important;
    box-shadow: none !important;
    border: 1px solid rgba(0,95,169,0.1);
}
"""
css += flat_map_css

with open('style.css', 'w') as f:
    f.write(css)

print("Updated index.html and style.css for flat map!")
