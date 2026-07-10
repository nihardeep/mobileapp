import re

with open('index.html', 'r') as f:
    html = f.read()

old_html = """                        <div style="flex: 1; text-align: left;">
                            <div style="font-size: 10px; font-weight: 700; color: #64748b; text-transform: uppercase;">Total Fare</div>
                            <div style="font-size: 20px; font-weight: 800; color: #0f172a;" id="passenger-total-fare">₹ 6,182</div>
                        </div>"""

new_html = """                        <div style="flex: 1; text-align: left; display: flex; flex-direction: column; justify-content: center;">
                            <div style="font-size: 10px; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 2px;">Total Fare</div>
                            <div style="display: flex; align-items: baseline; gap: 8px;">
                                <div style="font-size: 20px; font-weight: 800; color: #0f172a;" id="passenger-total-fare">₹ 6,182</div>
                                <div style="font-size: 12px; font-weight: 600; color: #94a3b8; text-decoration: line-through; display: none;" id="passenger-original-fare">₹ 6,182</div>
                            </div>
                            <div style="font-size: 10px; font-weight: 700; color: var(--indigo-blue); display: none; margin-top: 2px;" id="passenger-student-badge">Student Fare Applied</div>
                        </div>"""

html = html.replace(old_html, new_html)

with open('index.html', 'w') as f:
    f.write(html)
