import re

with open('style.css', 'r') as f:
    css = f.read()

old_pass_title = """.pass-title {
    font-size: 7px;
    font-weight: 700;
    letter-spacing: 0.5px;
    padding: 1.5px 4px;
    border: 1px solid currentColor;
    border-radius: 3px;
    line-height: 1;
}"""

new_pass_title = """.pass-title {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.5px;
    padding: 4px 8px;
    background: #fff;
    color: #00A1E4;
    border: none;
    border-radius: 4px;
    line-height: 1;
}"""

css = css.replace(old_pass_title, new_pass_title)

with open('style.css', 'w') as f:
    f.write(css)

with open('index.html', 'r') as f:
    html = f.read()

# Pattern to find each boarding pass card, extract the price, and replace the footer
# <div class="boarding-pass-card" ... > ... <span class="pass-min-price">PRICE</span> ... <div class="pass-footer"> ... </div> ... </div>

def replacer(match):
    prefix = match.group(1)
    price = match.group(2)
    mid = match.group(3)
    # Reconstruct the new footer
    new_footer = f"""<div class="pass-footer">
                                                <div class="pass-view-more-stub" style="margin: 0; text-align: left; text-decoration: underline; font-weight: 700; color: rgba(255, 255, 255, 0.9); cursor: pointer;" onclick="event.stopPropagation(); triggerHaptic('light', 'View Details'); navigateTo('results')">
                                                    View details
                                                </div>
                                                <div class="pass-book-cta" onclick="event.stopPropagation(); triggerHaptic('medium', 'Book CTA'); navigateTo('passenger')" style="background: #ffd15c; color: #000; padding: 8px 16px; border-radius: 20px; font-weight: 800; font-size: 14px; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
                                                    Book at {price}
                                                </div>
                                            </div>"""
    return prefix + price + mid + new_footer

# Regex: capture everything up to pass-min-price (group 1)
# Capture price (group 2)
# Capture everything between price and <div class="pass-footer"> (group 3)
# The footer itself is what we replace. We must match the footer exactly.
# Since the footer has a predictable structure:
pattern = r'(<div class="boarding-pass-card"[^>]*>.*?<span class="pass-min-price">)([^<]+)(</span>.*?)(<div class="pass-footer">.*?</div>\s*</div>)'

# Wait, the footer contains nested divs. A non-greedy match to </div> might stop early!
# The footer is:
# <div class="pass-footer">
#     <div class="pass-barcode-wrapper">...</div>
#     <div class="pass-view-more-stub"...>...</div>
# </div>
# Then the pass-body ends with </div>
pattern2 = r'(<div class="boarding-pass-card"[^>]*>.*?<span class="pass-min-price">)([^<]+)(</span>.*?)(<div class="pass-footer">.*?</div>\s*</div>\s*</div>\s*</div>)'
# Actually, it's safer to just split the file by pass-footer and replace it contextually, or use a more precise regex.

import re
# Let's find all pass-min-price
blocks = html.split('<div class="boarding-pass-card"')
new_blocks = [blocks[0]]

for block in blocks[1:]:
    # Find price
    price_match = re.search(r'<span class="pass-min-price">([^<]+)</span>', block)
    if price_match:
        price = price_match.group(1)
        
        # Now find the pass-footer block and replace it
        # pass-footer always ends the pass-body
        footer_start = block.find('<div class="pass-footer">')
        if footer_start != -1:
            # Find the end of pass-footer. We know it ends before the closing of pass-body.
            # In the HTML, it's followed by </div>\n</div>\n</div> (closing pass-body, pass-card, and ?)
            # Let's just find the exact string to replace using regex.
            # <div class="pass-footer"> ... </div> (where the inner doesn't have class="pass-footer")
            # We can use a simple regex for the footer block.
            footer_pattern = re.compile(r'<div class="pass-footer">.*?</div>\s*</div>\s*</div>', re.DOTALL)
            
            new_footer = f"""<div class="pass-footer" style="display: flex; justify-content: space-between; align-items: center; padding: 12px 16px;">
                                                <div class="pass-view-more-stub" style="margin: 0; text-align: left; text-decoration: underline; font-weight: 700; color: rgba(255, 255, 255, 0.9); cursor: pointer;" onclick="event.stopPropagation(); triggerHaptic('light', 'View Details'); navigateTo('results')">
                                                    View details
                                                </div>
                                                <div class="pass-book-cta" onclick="event.stopPropagation(); triggerHaptic('medium', 'Book CTA'); navigateTo('passenger')" style="background: #ffd15c; color: #000; padding: 8px 16px; border-radius: 20px; font-weight: 800; font-size: 14px; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
                                                    Book at {price}
                                                </div>
                                            </div>
                                        </div>
                                    </div>"""
            
            block = footer_pattern.sub(new_footer, block, count=1)
    
    new_blocks.append('<div class="boarding-pass-card"' + block)

final_html = "".join(new_blocks)

with open('index.html', 'w') as f:
    f.write(final_html)

print("Updated index.html and style.css")
