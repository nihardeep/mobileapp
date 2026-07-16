import re
with open('index.html', 'r') as f:
    lines = f.readlines()

start_line = 2921
end_line = 3331
depth = 0

for i in range(start_line, end_line):
    line = lines[i]
    # Handle same-line open and close carefully
    divs_open = len(re.findall(r'<div', line))
    divs_close = len(re.findall(r'</div', line))
    depth += (divs_open - divs_close)
    if depth < 0 or (depth == 0 and divs_open > 0) or (i > 3320):
        print(f"Line {i+1} (Depth {depth}): {line.strip()}")

print("Final Depth:", depth)
