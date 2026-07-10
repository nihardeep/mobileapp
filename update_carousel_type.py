with open('app.js', 'r') as f:
    js = f.read()

target = "init3DSwipingStack('trendingInstaCarousel', 'trendingInstaDots', 140, 200);"
replacement = "init3DCurvedCoverflow('trendingInstaCarousel', 'trendingInstaDots', 140, 200);"

js = js.replace(target, replacement)

with open('app.js', 'w') as f:
    f.write(js)
print("Updated successfully")
