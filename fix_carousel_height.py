with open('app.js', 'r') as f:
    js = f.read()

target = """    viewport.style.perspective = '1000px';
    viewport.style.perspectiveOrigin = '50% 50%';
    viewport.style.overflow = 'visible';
    viewport.style.position = 'relative';
    viewport.style.touchAction = 'none';"""

replacement = """    viewport.style.perspective = '1000px';
    viewport.style.perspectiveOrigin = '50% 50%';
    viewport.style.overflow = 'visible';
    viewport.style.position = 'relative';
    viewport.style.touchAction = 'none';
    viewport.style.height = `${cardHeight}px`;"""

js = js.replace(target, replacement)

with open('app.js', 'w') as f:
    f.write(js)
