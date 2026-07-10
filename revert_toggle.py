import re

with open('index.html', 'r') as f:
    html = f.read()

# Remove the hardcoded active class
html = html.replace('id="studentBannerWrapper" class="student-hyper-banner-wrapper active">', 'id="studentBannerWrapper" class="student-hyper-banner-wrapper">')

# Restore the developer toggle button.
# Let's find where it used to be. It was inside the .dev-tools-panel
dev_tools_regex = r'(<div class="dev-tools-panel".*?>\s*<div class="dev-tools-title">.*?</div>\s*<div class="dev-tools-grid">)'
match = re.search(dev_tools_regex, html, re.DOTALL)

if match:
    dev_btn_html = """
                    <button class="dev-trigger-btn" id="btnStateStudentPersona" onclick="toggleStudentPersona()">
                        <span class="dev-btn-icon">🎓</span>
                        Student Persona
                    </button>"""
    
    # We will inject it right after the dev-tools-grid opening tag
    html = html.replace(match.group(1), match.group(1) + dev_btn_html)

with open('index.html', 'w') as f:
    f.write(html)

with open('app.js', 'r') as f:
    js = f.read()

# Restore default false
js = js.replace('let isStudentPersonaActive = true;', 'let isStudentPersonaActive = false;')

with open('app.js', 'w') as f:
    f.write(js)

print("Restored developer toggle!")
