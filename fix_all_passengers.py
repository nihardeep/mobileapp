import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The carousel track starts here:
track_start_marker = '                            <div class="bp-carousel-track" id="bpTrack">'
track_start = content.find(track_start_marker)
if track_start == -1:
    print("Could not find track start")
    exit()

# It ends here:
track_end_marker = '                        </div>\n                        \n                        \n                        <div class="bp-dots" id="bpDots">'
track_end = content.find(track_end_marker, track_start)
if track_end == -1:
    print("Could not find track end")
    exit()

track_content = content[track_start + len(track_start_marker):track_end]

# Extract Passenger 1 block (up to the start of Passenger 2)
p2_start = track_content.find('                                <!-- Passenger 2 -->')
if p2_start == -1:
    p2_start = track_content.find('<div class="bp-slide">', 10) # Find the next slide if comment is missing

if p2_start != -1:
    p1_content = track_content[:p2_start].strip()
else:
    print("Could not separate P1")
    exit()

# Now create the new passengers
p2 = p1_content.replace('<!-- Passenger 1 -->', '<!-- Passenger 2 -->')
p2 = p2.replace('SHARMA / RAVI', 'SHARMA / ISHIKA')
p2 = p2.replace('SEC. 6E2341:001', 'SEC. 6E2341:002')
p2 = p2.replace('<div class="time bold">12C</div>', '<div class="time bold">12D</div>')
p2 = p2.replace('Economy (SSR: WCHR)', 'Economy')

p3 = p1_content.replace('<!-- Passenger 1 -->', '<!-- Passenger 3 -->')
p3 = p3.replace('SHARMA / RAVI', 'SHARMA / ARYA')
p3 = p3.replace('SEC. 6E2341:001', 'SEC. 6E2341:003')
p3 = p3.replace('<div class="time bold">12C</div>', '<div class="time bold">12E</div>')
p3 = p3.replace('Economy (SSR: WCHR)', 'Economy')

p4 = p1_content.replace('<!-- Passenger 1 -->', '<!-- Passenger 4 -->')
p4 = p4.replace('SHARMA / RAVI', 'SHARMA / ROHAN')
p4 = p4.replace('SEC. 6E2341:001', 'SEC. 6E2341:004')
p4 = p4.replace('<div class="time bold">12C</div>', '<div class="time bold">12F</div>')
p4 = p4.replace('Economy (SSR: WCHR)', 'Economy')

new_track_content = f"\n{p1_content}\n\n{p2}\n\n{p3}\n\n{p4}\n"

content = content[:track_start + len(track_start_marker)] + new_track_content + content[track_end:]

# Update the dots
old_dots = """<div class="bp-dots" id="bpDots">
                            <div class="bp-dot active" onclick="scrollToSlide(0)"></div>
                            <div class="bp-dot" onclick="scrollToSlide(1)"></div>
                        </div>"""
new_dots = """<div class="bp-dots" id="bpDots">
                            <div class="bp-dot active" onclick="scrollToSlide(0)"></div>
                            <div class="bp-dot" onclick="scrollToSlide(1)"></div>
                            <div class="bp-dot" onclick="scrollToSlide(2)"></div>
                            <div class="bp-dot" onclick="scrollToSlide(3)"></div>
                        </div>"""
                        
content = content.replace(old_dots, new_dots)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Passengers fully rebuilt!")
