with open('index.html', 'r') as f:
    html = f.read()

html = html.replace('>Bag lite<', '>BAG LITE<')

with open('index.html', 'w') as f:
    f.write(html)
