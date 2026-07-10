import re

with open('index.html', 'r') as f:
    html = f.read()

# Add active class to studentBannerWrapper
html = html.replace('id="studentBannerWrapper">', 'id="studentBannerWrapper" class="student-hyper-banner-wrapper active">')

# Also remove the developer toggle since we are making it standard
html = re.sub(r'<button class="dev-trigger-btn" id="btnStateStudentPersona".*?</button>', '', html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
print("Activated student banner in HTML natively!")
