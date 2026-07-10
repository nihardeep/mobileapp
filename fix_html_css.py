import re

with open('index.html', 'r') as f:
    html = f.read()

# Fix the sticky footer so it stays inside the iPhone frame
html = html.replace('style="position: fixed; bottom: 0; left: 0; right: 0; padding: 16px 24px; background: #E6EAF0; box-shadow: 0 -4px 20px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; z-index: 10; border-top: 1px solid rgba(255,255,255,0.5);"',
                    'style="position: sticky; bottom: 0; left: 0; right: 0; padding: 16px 24px; background: #E6EAF0; box-shadow: 0 -4px 20px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; z-index: 10; border-top: 1px solid rgba(255,255,255,0.5);"')

with open('index.html', 'w') as f:
    f.write(html)
