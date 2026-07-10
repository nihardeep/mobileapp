import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_grid = """                                            <div class="pass-details-grid">
                                                <div class="pass-detail-col">
                                                    <span class="pass-detail-label">FLIGHT</span>
                                                    <span class="pass-detail-val">6E 2015</span>
                                                </div>
                                                <div class="pass-detail-col">
                                                    <span class="pass-detail-label">CLASS</span>
                                                    <span class="pass-detail-val" style="color: #ffffff;">STRETCH</span>
                                                </div>
                                                <div class="pass-detail-col">
                                                    <span class="pass-detail-label">SEAT</span>
                                                    <span class="pass-detail-val">12A</span>
                                                </div>
                                                <div class="pass-detail-col align-right">
                                                    <span class="pass-detail-label">MEAL</span>
                                                    <span class="pass-detail-val">Veg Club</span>
                                                </div>
                                            </div>"""

new_grid = """                                            <div class="pass-details-grid" style="grid-template-columns: 1.1fr 1.3fr 0.6fr 1fr;">
                                                <div class="pass-detail-col">
                                                    <span class="pass-detail-label">FLIGHT</span>
                                                    <span class="pass-detail-val">6E 2015</span>
                                                </div>
                                                <div class="pass-detail-col">
                                                    <span class="pass-detail-label">CLASS</span>
                                                    <span class="pass-detail-val" style="color: #ffffff;">STRETCH</span>
                                                </div>
                                                <div class="pass-detail-col">
                                                    <span class="pass-detail-label">SEAT</span>
                                                    <span class="pass-detail-val">12A</span>
                                                </div>
                                                <div class="pass-detail-col align-right">
                                                    <span class="pass-detail-label">MEAL</span>
                                                    <span class="pass-detail-val">Veg Club</span>
                                                </div>
                                            </div>"""

content = content.replace(old_grid, new_grid)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Grid aligned")
