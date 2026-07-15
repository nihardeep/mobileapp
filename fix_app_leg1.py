with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

app_js = app_js.replace("el.innerText = 'LUCKNOW'", "el.innerText = 'DELHI'")
app_js = app_js.replace("el.innerText = 'LKO'", "el.innerText = 'DEL'")
app_js = app_js.replace("el.innerText = 'NEW DELHI'", "el.innerText = 'MUMBAI'")
# We need to make sure the second replacement of 'DEL' to 'BOM' doesn't replace the first one
app_js = app_js.replace("city2CodeEls.forEach(el => el.innerText = 'DEL')", "city2CodeEls.forEach(el => el.innerText = 'BOM')")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
