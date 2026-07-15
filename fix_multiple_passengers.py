import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# First, let's extract RAVI's timeline wrapper, we'll use it as a base for the others.
# The timeline wrapper is right after the passenger name.
# Wait, actually, RAVI's timeline wrapper has multi-leg support (with the toggle). 
# But for passengers 2, 3, 4 we can just duplicate the exact same timeline wrapper.

# Let's find the start of ISHIKA's card
ishika_start = content.find('<div class="bp-pass-card">')
if ishika_start == -1:
    print("Could not find ISHIKA card start")

# Actually, finding ISHIKA's card specifically:
ishika_card_regex = re.compile(r'<div class="bp-pass-card">\s*<div class="bp-qr-section">.*?<div class="bp-passenger-name">SHARMA / ISHIKA</div>\s*</div>\s*<div class="bp-timeline-wrapper">.*?</div>\s*</div>\s*</div>\s*</div>', re.DOTALL)

# Let's extract RAVI's full card to duplicate it, then just change the names, seats, and sequences.
ravi_card_match = re.search(r'(<div class="bp-pass-card">.*?<div class="bp-passenger-name">SHARMA / RAVI</div>\s*</div>\s*<div class="bp-leg-toggle multi-only" id="bpLegToggle">.*?</div>\s*</div>\s*</div>)', content, re.DOTALL)

if ravi_card_match:
    ravi_card = ravi_card_match.group(1)
    
    # Create ISHIKA card
    ishika_card = ravi_card.replace('SHARMA / RAVI', 'SHARMA / ISHIKA')
    ishika_card = ishika_card.replace('SEC. 6E2341:001', 'SEC. 6E2341:002')
    ishika_card = ishika_card.replace('<div class="time bold">12C</div>', '<div class="time bold">12D</div>')
    ishika_card = ishika_card.replace('Economy (SSR: WCHR)', 'Economy')
    
    # Create ARYA card
    arya_card = ravi_card.replace('SHARMA / RAVI', 'SHARMA / ARYA')
    arya_card = arya_card.replace('SEC. 6E2341:001', 'SEC. 6E2341:003')
    arya_card = arya_card.replace('<div class="time bold">12C</div>', '<div class="time bold">12E</div>')
    arya_card = arya_card.replace('Economy (SSR: WCHR)', 'Economy')

    # Create ROHAN card
    rohan_card = ravi_card.replace('SHARMA / RAVI', 'SHARMA / ROHAN')
    rohan_card = rohan_card.replace('SEC. 6E2341:001', 'SEC. 6E2341:004')
    rohan_card = rohan_card.replace('<div class="time bold">12C</div>', '<div class="time bold">12F</div>')
    rohan_card = rohan_card.replace('Economy (SSR: WCHR)', 'Economy')
    
    # We need to replace everything in the bp-carousel-track
    track_start = content.find('<div class="bp-carousel-track" id="bpCarousel">')
    track_end = content.find('</div>\n                        \n                        \n                        <div class="bp-dots" id="bpDots">')
    
    if track_start != -1 and track_end != -1:
        new_track = '<div class="bp-carousel-track" id="bpCarousel">\n' + ravi_card + '\n' + ishika_card + '\n' + arya_card + '\n' + rohan_card + '\n                        '
        
        content = content[:track_start] + new_track + content[track_end:]
        
        # Now fix the dots
        dots_old = """<div class="bp-dots" id="bpDots">
                            <div class="bp-dot active" onclick="scrollToSlide(0)"></div>
                            <div class="bp-dot" onclick="scrollToSlide(1)"></div>
                        </div>"""
        dots_new = """<div class="bp-dots" id="bpDots">
                            <div class="bp-dot active" onclick="scrollToSlide(0)"></div>
                            <div class="bp-dot" onclick="scrollToSlide(1)"></div>
                            <div class="bp-dot" onclick="scrollToSlide(2)"></div>
                            <div class="bp-dot" onclick="scrollToSlide(3)"></div>
                        </div>"""
        content = content.replace(dots_old, dots_new)
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Successfully updated passengers.")
    else:
        print("Could not find carousel track.")
else:
    print("Could not find RAVI card.")
