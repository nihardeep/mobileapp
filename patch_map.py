import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Add Search Bar and Overlay to .globe-map-container
search_ui = """
<div class="globe-map-container" style="position: relative; overflow: hidden; touch-action: pan-x pan-y;">
    <!-- Map Search UI -->
    <div style="position: absolute; top: 16px; left: 16px; right: 16px; z-index: 10; display: flex; align-items: center; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(8px); border-radius: 20px; padding: 4px 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#64748b" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" id="mapSearchInput" placeholder="Search destination (e.g. Paris, Dubai)" style="border: none; background: transparent; padding: 10px; font-size: 14px; font-weight: 600; color: #0f172a; width: 100%; outline: none;" onfocus="this.parentElement.style.boxShadow='0 4px 20px rgba(0,94,184,0.2)'" onblur="this.parentElement.style.boxShadow='0 4px 16px rgba(0,0,0,0.1)'" onkeyup="handleMapSearch(this.value)">
    </div>
    
    <!-- Autocomplete Results -->
    <div id="mapSearchResults" style="position: absolute; top: 65px; left: 16px; right: 16px; z-index: 10; background: #fff; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.15); display: none; max-height: 200px; overflow-y: auto;"></div>

    <!-- Scroll Warning Overlay -->
    <div id="mapScrollWarning" style="position: absolute; inset: 0; background: rgba(0,0,0,0.4); color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 20; opacity: 0; pointer-events: none; transition: opacity 0.3s ease;">
        <svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="currentColor" stroke-width="2" style="margin-bottom: 12px;"><path d="M7 11V7a5 5 0 0 1 10 0v4"></path><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect></svg>
        <div style="font-size: 18px; font-weight: 700;">Use two fingers to pan</div>
    </div>
"""

content = content.replace('<div class="globe-map-container">', search_ui)

# 2. Add Transform Layer to flat-map-wrapper
wrapper_start = '<div class="flat-map-wrapper"'
transform_layer = '<div class="flat-map-wrapper" id="mapWrapper"\n<div id="mapTransformLayer" style="width: 100%; height: 100%; transform-origin: 0 0; transition: transform 0.1s linear;">'
# Actually we can just do regex replacement
content = re.sub(r'<div class="flat-map-wrapper"[^>]*>', r'<div class="flat-map-wrapper" id="mapWrapper" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: #ffffff;">\n<div id="mapTransformLayer" style="width: 100%; height: 100%; transform-origin: 0 0; transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1); position: relative;">', content)

# 3. Close the transform layer. Find the closing </svg> of the flat-map-wrapper.
# The SVG has sodipodi:docname="World_map_-_low_resolution.svg"
# We can find that string, then find the next </svg>, then insert </div>
import sys
if "World_map_-_low_resolution.svg" in content:
    idx = content.find("World_map_-_low_resolution.svg")
    svg_end = content.find("</svg>", idx)
    if svg_end != -1:
        # Add a pin container right after the SVG
        pin_html = '\n<!-- Map Pins Layer -->\n<div id="mapPinsLayer" style="position: absolute; top: 0; left: 0; width: 950px; height: 620px; pointer-events: none;"></div>\n'
        content = content[:svg_end+6] + pin_html + "\n</div>" + content[svg_end+6:]
    else:
        print("Could not find </svg>")
        sys.exit(1)

with open('index.html', 'w') as f:
    f.write(content)
print("index.html patched!")
