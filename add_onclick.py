with open('index.html', 'r') as f:
    text = f.read()

target = '<div class="zero-balance-flash-container" style="position: relative; height: 20px; width: 100%; display: flex; justify-content: center;">'
replacement = '<div class="zero-balance-flash-container" onclick="openGame()" style="position: relative; height: 20px; width: 100%; display: flex; justify-content: center; cursor: pointer;">'

if target in text:
    text = text.replace(target, replacement)
    with open('index.html', 'w') as f:
        f.write(text)
    print("Added onclick to game banner!")
else:
    print("Could not find banner target string")
