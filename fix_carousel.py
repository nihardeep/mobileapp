import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I will find the end of Hotel Card 1 inside companionHotelDeals
# We know the container is:
# <div style="display: flex; gap: 16px; overflow-x: auto; scroll-snap-type: x mandatory; padding: 0 20px 20px 20px; margin: 0; scrollbar-width: none;">

card2 = """
        <!-- Hotel Card 2 -->
        <div style="flex: 0 0 75%; scroll-snap-align: center; background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.9); border-radius: 16px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,31,84,0.06);">
            <div style="height: 100px; background: url('https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80') center/cover; position: relative;">
                <div style="position: absolute; top: 12px; left: 12px; background: rgba(0,0,0,0.6); backdrop-filter: blur(4px); color: #fff; padding: 4px 8px; border-radius: 8px; font-size: 11px; font-weight: 700;">⭐ 4.5 Very Good</div>
            </div>
            <div style="padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <div>
                        <h4 style="margin: 0 0 2px 0; font-size: 16px; font-weight: 800; color: #0f172a;">Trident Nariman Point</h4>
                        <span style="font-size: 12px; color: #64748b;">Nariman Point, Mumbai</span>
                    </div>
                    <div style="display: inline-block; background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 4px 8px; border-radius: 8px; font-size: 10px; font-weight: 800; text-transform: uppercase;">25% OFF • USE TRI25</div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: flex-end;">
                    <div>
                        <div style="font-size: 11px; color: #94a3b8; text-decoration: line-through;">₹15,000</div>
                        <div style="font-size: 18px; font-weight: 800; color: #0f172a;">₹11,250 <span style="font-size: 11px; font-weight: 600; color: #64748b;">/night</span></div>
                    </div>
                    <button style="background: #005eb8; color: #fff; border: none; padding: 8px 16px; border-radius: 10px; font-weight: 700; font-size: 13px;">Book</button>
                </div>
            </div>
        </div>
        
        <!-- Hotel Card 3 -->
        <div style="flex: 0 0 75%; scroll-snap-align: center; background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.9); border-radius: 16px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,31,84,0.06);">
            <div style="height: 100px; background: url('https://images.unsplash.com/photo-1542314831-c6a4d27a658d?w=600&q=80') center/cover; position: relative;">
                <div style="position: absolute; top: 12px; left: 12px; background: rgba(59, 130, 246, 0.95); color: #fff; padding: 4px 10px; border-radius: 8px; font-size: 10px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.5px;">NEW</div>
            </div>
            <div style="padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <div>
                        <h4 style="margin: 0 0 2px 0; font-size: 16px; font-weight: 800; color: #0f172a;">JW Marriott</h4>
                        <span style="font-size: 12px; color: #64748b;">Juhu, Mumbai</span>
                    </div>
                    <div style="display: inline-block; background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 4px 8px; border-radius: 8px; font-size: 10px; font-weight: 800; text-transform: uppercase;">12% OFF • USE JW12</div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: flex-end;">
                    <div>
                        <div style="font-size: 11px; color: #94a3b8; text-decoration: line-through;">₹21,000</div>
                        <div style="font-size: 18px; font-weight: 800; color: #0f172a;">₹18,500 <span style="font-size: 11px; font-weight: 600; color: #64748b;">/night</span></div>
                    </div>
                    <button style="background: #005eb8; color: #fff; border: none; padding: 8px 16px; border-radius: 10px; font-weight: 700; font-size: 13px;">Book</button>
                </div>
            </div>
        </div>
"""

# Find the end of Hotel Card 1
# It's inside companionHotelDeals
# Let's search for "Book</button>\n                </div>\n            </div>\n        </div>\n    </div>"
# and insert card2 before the last `</div>`

target = """Book</button>
                </div>
            </div>
        </div>"""

if target in html:
    idx = html.find(target, html.find('id="companionHotelDeals"'))
    if idx != -1:
        insert_pos = idx + len(target)
        html_new = html[:insert_pos] + '\n' + card2 + html[insert_pos:]
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_new)
        print("Carousel restored successfully")
    else:
        print("Could not find target after companionHotelDeals")
else:
    print("Could not find target")

