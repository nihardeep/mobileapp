with open('app.js', 'r') as f:
    js = f.read()

# Replace block with flex for homeFlightStateWrapper
js = js.replace("wrapper.style.display = 'block';", "wrapper.style.display = 'flex';")

with open('app.js', 'w') as f:
    f.write(js)
