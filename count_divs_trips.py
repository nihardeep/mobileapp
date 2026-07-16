with open('index.html', 'r') as f:
    lines = f.readlines()

start_line = 2921 # <div class="screen" id="screenTrips"...>
end_line = 3331 # <div class="screen" id="screenResults">

depth = 0
for i in range(start_line, end_line):
    line = lines[i]
    # super basic counting
    open_count = line.count('<div')
    close_count = line.count('</div')
    depth += (open_count - close_count)

print("Depth at end of screenTrips:", depth)
