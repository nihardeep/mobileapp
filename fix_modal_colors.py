import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace color for close button
css = css.replace('font-size: 24px; color: #0f172a;\n    cursor: pointer; font-weight: 700;', 
                  'font-size: 24px; color: #ffffff;\n    cursor: pointer; font-weight: 700;')

# Replace color for title
css = css.replace('font-size: 24px; font-weight: 900; color: #0f172a; margin-bottom: 30px;', 
                  'font-size: 24px; font-weight: 900; color: #ffffff; margin-bottom: 30px;')

# Replace color for subtitle
css = css.replace('margin-top: 20px; font-size: 14px; font-weight: 700; color: #64748b;', 
                  'margin-top: 20px; font-size: 14px; font-weight: 700; color: #94a3b8;')

# Fix img blend mode in modal so the white background of the QR stays if it's a transparent PNG
# Actually, the original CSS had box-shadow, we can leave it. But we should add background: white to the img
css = css.replace('width: 250px; height: 250px;\n    box-shadow: 0 10px 40px rgba(0,0,0,0.1);\n    border-radius: 12px;', 
                  'width: 250px; height: 250px;\n    box-shadow: 0 10px 40px rgba(0,0,0,0.5);\n    border-radius: 12px;\n    background: white;\n    padding: 16px;')

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Updated modal colors")
