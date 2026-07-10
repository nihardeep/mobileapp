import sys
import re

file_path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
with open(file_path, 'r') as f:
    html = f.read()

divs_open = len(re.findall(r'<div\b[^>]*>', html))
divs_close = len(re.findall(r'</div>', html))

print(f"{file_path} - <div...>: {divs_open}, </div>: {divs_close}")
