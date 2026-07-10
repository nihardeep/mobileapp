import urllib.request
import re

url = 'https://upload.wikimedia.org/wikipedia/commons/8/80/World_map_-_low_resolution.svg'

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        svg_data = response.read().decode('utf-8')
        
        # Clean up the SVG to allow CSS styling
        # Remove hardcoded fill and stroke
        svg_data = re.sub(r'fill="[^"]+"', '', svg_data)
        svg_data = re.sub(r'stroke="[^"]+"', '', svg_data)
        
        # We can add a class to the SVG to style it
        svg_data = svg_data.replace('<svg ', '<svg class="flat-world-map" ')
        
        with open('world_map.svg', 'w') as f:
            f.write(svg_data)
        print("Successfully downloaded and cleaned world_map.svg")
except Exception as e:
    print("Error:", e)
