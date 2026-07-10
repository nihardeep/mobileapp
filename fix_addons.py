import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Fix screenAddons style
target_screen = '<div class="screen" id="screenAddons" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #f8fafc; z-index: 200;">'
repl_screen = '<div class="screen" id="screenAddons" style="background: #f8fafc; padding-bottom: 24px;">'
html = html.replace(target_screen, repl_screen)

# 2. Fix Sticky Bottom Checkout Bar
target_bar = '<div style="position: absolute; bottom: 0; left: 0; right: 0; background: #ffffff; padding: 16px 24px 24px; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; z-index: 101; box-shadow: 0 -10px 30px rgba(0,0,0,0.05);">'
repl_bar = '<div style="position: sticky; bottom: 0; margin-left: -16px; margin-right: -16px; width: calc(100% + 32px); background: #ffffff; padding: 16px 24px 24px; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; z-index: 101; box-shadow: 0 -10px 30px rgba(0,0,0,0.05);">'
html = html.replace(target_bar, repl_bar)

# 3. Add negative margins to the Ultra-Premium Header in screenAddons to stretch it fully too!
# Currently: <div style="position: sticky; top: 0; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(20px); z-index: 50; padding-top: 16px; border-bottom: 1px solid rgba(0,0,0,0.05);">
target_header = '<div style="position: sticky; top: 0; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(20px); z-index: 50; padding-top: 16px; border-bottom: 1px solid rgba(0,0,0,0.05);">'
repl_header = '<div style="position: sticky; top: 0; margin-left: -16px; margin-right: -16px; width: calc(100% + 32px); background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(20px); z-index: 50; padding-top: 16px; border-bottom: 1px solid rgba(0,0,0,0.05);">'
html = html.replace(target_header, repl_header)

with open('index.html', 'w') as f:
    f.write(html)
print("Addons fixed")
