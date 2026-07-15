import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('LUCKNOW', 'DELHI')
content = content.replace('LKO ✈ DEL', 'DEL ✈ BOM')
content = content.replace('DEL ✈ AMS', 'BOM ✈ GOI')
content = content.replace('LKO', 'DEL')
content = content.replace('NEW DELHI', 'MUMBAI')
content = content.replace('id="tkCity2Code">DEL<', 'id="tkCity2Code">BOM<')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

app_js = app_js.replace("'LUCKNOW'", "'DELHI'")
app_js = app_js.replace("'LKO'", "'DEL'")
app_js = app_js.replace("'NEW DELHI'", "'MUMBAI'")
app_js = app_js.replace("'DEL'", "'BOM'")
# the second replacement of 'DEL' to 'BOM' might conflict if we are replacing city code DEL.
# Let's verify manually via script logic
app_js = app_js.replace("city2CodeEls.forEach(el => el.innerText = 'BOM');", "city2CodeEls.forEach(el => el.innerText = 'BOM');")
