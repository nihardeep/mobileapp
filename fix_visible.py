import re

with open('app.js', 'r') as f:
    js = f.read()

# Fix openPassengerForm
js = js.replace("if (backdrop) backdrop.classList.add('active');\n    if (sheet) sheet.classList.add('active');",
                "if (backdrop) backdrop.classList.add('visible');\n    if (sheet) sheet.classList.add('visible');")

# Fix openBulkAddSheet
js = js.replace("if (backdrop) backdrop.classList.add('active');\n    if (sheet) sheet.classList.add('active');",
                "if (backdrop) backdrop.classList.add('visible');\n    if (sheet) sheet.classList.add('visible');")

with open('app.js', 'w') as f:
    f.write(js)
