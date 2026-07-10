import re

# 1. Fix style.css
with open('style.css', 'r') as f:
    css = f.read()

# Update .student-hyper-banner padding
banner_regex = r'(\.student-hyper-banner \{[^}]+)\}'
match = re.search(banner_regex, css)
if match:
    old_banner = match.group(0)
    # replace padding
    new_banner = re.sub(r'padding:\s*12px 16px;', 'padding: 56px 16px 16px 16px;', old_banner)
    css = css.replace(old_banner, new_banner)

# Update .student-hyper-banner-wrapper margin and max-height
wrapper_regex = r'(\.student-hyper-banner-wrapper \{[^}]+)\}'
match = re.search(wrapper_regex, css)
if match:
    old_wrapper = match.group(0)
    new_wrapper = re.sub(r'margin-top:\s*16px;', 'margin-top: 0;', old_wrapper)
    css = css.replace(old_wrapper, new_wrapper)

wrapper_active_regex = r'(\.student-hyper-banner-wrapper\.active \{[^}]+)\}'
match = re.search(wrapper_active_regex, css)
if match:
    old_wrapper_act = match.group(0)
    new_wrapper_act = re.sub(r'max-height:\s*120px;', 'max-height: 180px;', old_wrapper_act)
    css = css.replace(old_wrapper_act, new_wrapper_act)

with open('style.css', 'w') as f:
    f.write(css)

# 2. Fix app.js
with open('app.js', 'r') as f:
    js = f.read()

toggle_regex = r'(wrapper\.classList\.add\(\'active\'\);)'
if toggle_regex not in js:
    js = re.sub(r'(wrapper\.classList\.add\(\'active\'\);)', r'\1\n            const header = document.getElementById("homeHeaderSection");\n            if (header) header.style.paddingTop = "8px";', js)
    js = re.sub(r'(wrapper\.classList\.remove\(\'active\'\);)', r'\1\n            const header = document.getElementById("homeHeaderSection");\n            if (header) header.style.paddingTop = "52px";', js)

with open('app.js', 'w') as f:
    f.write(js)

# 3. Fix index.html banner content
with open('index.html', 'r') as f:
    html = f.read()

old_shb_html = """                                <div class="student-hyper-banner" onclick="openStudentHub()">
                                    <div class="shb-icon">🎓</div>
                                    <div class="shb-content">
                                        <div class="shb-title">Welcome back, Student!</div>
                                        <div class="shb-desc">10% Off • Free Date Change • +15Kg Extra Baggage</div>
                                    </div>
                                    <div class="shb-cta">Search ➔</div>
                                </div>"""

new_shb_html = """                                <div class="student-hyper-banner" onclick="openStudentHub()">
                                    <div class="shb-content">
                                        <div class="shb-title">Welcome back, Nihar! <span style="font-size: 16px;">🎓</span></div>
                                        <div class="shb-desc-premium">
                                            <span style="color: #005FA9; margin-right: 4px;">✨</span> 
                                            Applying your perks: <strong>10% Off</strong>, <strong>Free Date Change</strong>, & <strong>+15Kg Baggage</strong>.
                                        </div>
                                    </div>
                                    <div class="shb-cta" style="background: rgba(0,0,0,0.05); color: #005FA9; padding: 6px 12px; border-radius: 20px; font-weight: 700; font-size: 12px; display: flex; align-items: center; justify-content: center; height: fit-content; align-self: flex-end; margin-bottom: 4px;">Search ➔</div>
                                </div>"""

if 'Welcome back, Student!' in html:
    html = html.replace(old_shb_html, new_shb_html)

with open('index.html', 'w') as f:
    f.write(html)

print("Updated banner design and notch collision handling.")
