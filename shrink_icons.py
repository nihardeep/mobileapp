import sys

with open('index.html', 'r') as f:
    content = f.read()

# Replace circle sizes
content = content.replace('width: 36px; height: 36px; border-radius: 50%;', 'width: 28px; height: 28px; border-radius: 50%;')

# Replace SVG sizes inside the hidden menu
# Wait, let's just find and replace the specific SVGs we added.
# They all have `width="16" height="16" fill="none"` or similar.
# Let's replace the common svg width/height properties within that section.
# We know they are inside the div with border-radius 50%.
# But it's easier to just do a regex sub.

import re
# Match the div and the svg inside it
pattern = re.compile(r'(<div style="width: 28px; height: 28px; border-radius: 50%;[^>]+>\s*<svg[^>]+)width="16" height="16"')
content = pattern.sub(r'\1width="12" height="12"', content)

# Write back
with open('index.html', 'w') as f:
    f.write(content)

print("Icons shrunk successfully.")
