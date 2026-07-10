import re

# 1. Update style.css
with open('style.css', 'r') as f:
    css = f.read()

# Fix banner width
css = css.replace("""    margin: 0 -16px;
    padding: 52px 20px 30px 20px;""", """    margin: 0 -16px;
    width: calc(100% + 32px);
    padding: 52px 20px 30px 20px;""")

# Fix benefit items visibility
css = css.replace(""".sh-benefit-item {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);""", """.sh-benefit-item {
    background: #ffffff;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    color: #0f172a;
    border: none;""")

with open('style.css', 'w') as f:
    f.write(css)


# 2. Update index.html
with open('index.html', 'r') as f:
    html = f.read()

# Find the search widget container inside screenStudentHub
start_marker = '<!-- Embedded Flight Search Widget Replica -->'
end_marker = '</div>\n                        </div>'
# We need to use regex to find the end of the widget
pattern = re.compile(r'<!-- Embedded Flight Search Widget Replica -->.*?<button class="riyadh-search-btn".*?</button>\s*</div>\s*</div>', re.DOTALL)

replacement = """<!-- Mini Search Widget -->
                        <div class="student-hub-search-context" onclick="navigateTo('home')" style="display: flex; justify-content: space-between; align-items: center; background: #fff; padding: 16px; margin: -16px 0 24px 0; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); font-size: 14px; color: #0f172a; position: relative; z-index: 10; cursor: pointer;">
                            <span><strong>DEL</strong> to <strong>BOM</strong> • 1 Student</span>
                            <div style="color: var(--indigo-blue); display: flex; align-items: center; gap: 4px;">
                                <span style="font-size: 12px; font-weight: 700;">Edit</span>
                                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                            </div>
                        </div>"""

if pattern.search(html):
    html = pattern.sub(replacement, html)
else:
    print("Could not find the widget to replace")

# Also add the edit interaction to the destination page search bar
dest_target = """<div class="ai-dest-edit-icon">"""
dest_repl = """<div class="ai-dest-edit-icon" onclick="navigateTo('home')">"""
html = html.replace(dest_target, dest_repl)

# Update cache buster
html = html.replace('app.js?v=21', 'app.js?v=22')

with open('index.html', 'w') as f:
    f.write(html)

print("Done")
