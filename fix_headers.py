with open('style.css', 'r') as f:
    css = f.read()

target_ai = """.ai-dest-header {
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;"""

replacement_ai = """.ai-dest-header {
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 52px 20px 16px 20px;"""

css = css.replace(target_ai, replacement_ai)

target_student = """.student-hub-header {
    background: linear-gradient(135deg, #FF9900 0%, #FF5E00 100%);
    margin: 0 -16px;
    padding: 30px 20px 30px 20px;"""

replacement_student = """.student-hub-header {
    background: linear-gradient(135deg, #FF9900 0%, #FF5E00 100%);
    margin: 0 -16px;
    padding: 52px 20px 30px 20px;"""

css = css.replace(target_student, replacement_student)

with open('style.css', 'w') as f:
    f.write(css)

with open('index.html', 'r') as f:
    html = f.read()
html = html.replace('app.js?v=20', 'app.js?v=21')
with open('index.html', 'w') as f:
    f.write(html)
