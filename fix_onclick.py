with open('index.html', 'r') as f:
    content = f.read()

# Replace <div class="zero-balance-flash-container" style="..."> with onclick
target = '<div class="zero-balance-flash-container" style="position: relative; height: 20px; width: 100%; display: flex; justify-content: center;">'
replacement = '<div class="zero-balance-flash-container" onclick="openGame()" style="position: relative; height: 20px; width: 100%; display: flex; justify-content: center; cursor: pointer;">'

if target in content:
    content = content.replace(target, replacement)
    with open('index.html', 'w') as f:
        f.write(content)
    print("Added onclick to game banner!")
else:
    print("Could not find banner target")
