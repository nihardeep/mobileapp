import re

with open('index.html', 'r') as f:
    html = f.read()

# Re-inject the student persona toggle button
dev_btn_html = """
                    <button class="dev-trigger-btn" id="btnStateStudentPersona" onclick="toggleStudentPersona()">
                        <span class="dev-btn-icon">🎓</span>
                        Student Persona
                        <div class="dev-btn-indicator"></div>
                    </button>"""

# Find btnStateCancelled
regex = r'(<button class="dev-trigger-btn" id="btnStateCancelled".*?</button>)'
html = re.sub(regex, r'\1' + dev_btn_html, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
print("Re-injected toggle button successfully!")
