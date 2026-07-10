with open('style.css', 'r') as f:
    css = f.read()

# Add standard webkit fixes to .iphone-screen
target = "overflow: hidden;"
replacement = "overflow: hidden;\n    -webkit-mask-image: -webkit-radial-gradient(white, black);\n    mask-image: radial-gradient(white, black);\n    transform: translateZ(0);"

if target in css:
    css = css.replace(target, replacement, 1)
    with open('style.css', 'w') as f:
        f.write(css)
    print("Patched .iphone-screen Safari bug!")
else:
    print("Target not found!")
