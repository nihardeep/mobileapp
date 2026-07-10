with open('style.css', 'r') as f:
    css = f.read()

target = """.passenger-card {
    background: #E6EAF0;
    border-radius: 16px;
    padding: 8px 16px;
    box-shadow: 5px 5px 10px rgba(163,177,198,0.5), -5px -5px 10px rgba(255,255,255,0.8);
    transition: all 0.3s ease;"""

replacement = """.passenger-card {
    background: #E6EAF0;
    border-radius: 16px;
    padding: 8px 16px;
    box-shadow: 5px 5px 10px rgba(163,177,198,0.5), -5px -5px 10px rgba(255,255,255,0.8);
    transition: all 0.3s ease;
    cursor: pointer;"""

css = css.replace(target, replacement)

with open('style.css', 'w') as f:
    f.write(css)

with open('index.html', 'r') as f:
    html = f.read()

html = html.replace('app.js?v=17', 'app.js?v=18')

with open('index.html', 'w') as f:
    f.write(html)
