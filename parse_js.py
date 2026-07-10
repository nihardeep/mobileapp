import esprima
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()
try:
    esprima.parseScript(js)
    print("JS OK")
except Exception as e:
    print(f"JS ERROR: {e}")
