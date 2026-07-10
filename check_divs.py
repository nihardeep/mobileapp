import re
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

depth = 0
for i, line in enumerate(lines):
    # simple heuristic for well-formatted HTML:
    adds = line.count('<div')
    subs = line.count('</div')
    depth += adds - subs
    
    # Just print out lines around the screens to see the depth
    if '<div class="screen"' in line or 'iphone-screen' in line:
        print(f"Line {i+1}: Depth={depth} | {line.strip()}")
        
