with open('index.html', 'r') as f:
    html = f.read()

font_links = """    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">"""

html = html.replace('<link rel="stylesheet" href="style.css">', font_links)

with open('index.html', 'w') as f:
    f.write(html)
