import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

warning_html = """
    <!-- Scroll Warning Overlay -->
    <div id="mapScrollWarning" style="position: absolute; inset: 0; background: rgba(0,0,0,0.5); color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 60; opacity: 0; pointer-events: none; transition: opacity 0.3s ease;">
        <svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="currentColor" stroke-width="2" style="margin-bottom: 12px;"><path d="M7 11V7a5 5 0 0 1 10 0v4"></path><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect></svg>
        <div style="font-size: 18px; font-weight: 700;">Use two fingers to pan</div>
    </div>
"""

# Insert warning right before <div class="flat-map-wrapper"
if '<div class="flat-map-wrapper"' in content and 'id="mapScrollWarning"' not in content:
    content = content.replace('<div class="flat-map-wrapper"', warning_html + '\n    <div class="flat-map-wrapper"')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added mapScrollWarning")
else:
    print("Failed or already added")

