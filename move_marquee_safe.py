import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Extract marquee from the homepage
marquee_regex = r'(<!-- Bank Offers Marquee -->\s*<div class="offers-marquee-wrapper">.*?</div>\s*</div>)'
match = re.search(marquee_regex, html, re.DOTALL)

if match:
    marquee_html = match.group(0)
    
    # 2. Remove it from its current position
    html = html.replace(marquee_html, '')
    
    # 3. Add inline style to adjust margins for the listing page header
    # We want to remove the large margin-top and add some bottom margin to separate from date pills
    adjusted_marquee = marquee_html.replace(
        '<div class="offers-marquee-wrapper">',
        '<div class="offers-marquee-wrapper" style="margin-top: 8px; margin-bottom: 12px; background: #fff; border-top: 1px dashed rgba(0,0,0,0.05); border-bottom: 1px dashed rgba(0,0,0,0.05); padding: 6px 0;">'
    )
    
    # 4. Insert it into #screenResults between .results-nav-bar and .results-date-pills
    insertion_point = '<!-- Date Pills Row -->'
    if insertion_point in html:
        html = html.replace(insertion_point, adjusted_marquee + '\n                        ' + insertion_point)
        print("Marquee successfully moved to flight listing page!")
    else:
        print("Could not find insertion point!")
        
    with open('index.html', 'w') as f:
        f.write(html)
else:
    print("Could not find marquee to extract!")
