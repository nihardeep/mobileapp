import re

with open('index.html', 'r') as f:
    html = f.read()

# Isolate cards container
start = html.find('id="passenger-cards-container"')
end = html.find('<!-- Contact Details -->')

if start != -1 and end != -1:
    cards_html = html[start:end]
    
    # Revert avatars
    cards_html = cards_html.replace('width: 32px; height: 32px; font-size: 12px;', 'width: 40px; height: 40px;')
    
    # Revert gaps
    cards_html = cards_html.replace('gap: 12px;', 'gap: 16px;')
    
    html = html[:start] + cards_html + html[end:]

    with open('index.html', 'w') as f:
        f.write(html)
