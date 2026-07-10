with open('style.css', 'r') as f:
    css = f.read()

spacing_css = """
#trendingInstaContainer {
    height: 230px;
    margin-top: 10px;
}
"""

if "#trendingInstaContainer" not in css:
    with open('style.css', 'a') as f:
        f.write("\n" + spacing_css)
    print("Added spacing CSS")
else:
    print("Already added")
