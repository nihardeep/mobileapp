with open('index.html', 'r') as f:
    html = f.read()

target = "                </div> <!-- End appContent -->\n\n                <div class=\"screen\" id=\"screenResults\">"
replacement = "\n                <div class=\"screen\" id=\"screenResults\">"

html = html.replace(target, replacement)

with open('index.html', 'w') as f:
    f.write(html)
