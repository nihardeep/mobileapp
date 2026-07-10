import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove all `<audio>` nodes, `</body>` and `</html>`
audio_regex = r'<!-- Haptic audio simulation nodes -->.*?</audio>\s*</audio>\s*</audio>'
html = re.sub(audio_regex, '', html, flags=re.DOTALL)
html = html.replace('</body>\n</html>', '')
html = html.replace('</body>', '').replace('</html>', '')
html = html.replace('<!-- Haptic audio simulation nodes -->\n\n\n', '')
html = html.replace('<!-- Haptic audio simulation nodes -->\n', '')
html = html.replace('<!-- Haptic audio simulation nodes -->', '')

# Remove audio tags individually just in case
html = re.sub(r'<audio.*?</audio>', '', html, flags=re.DOTALL)

# Remove all `<!-- ALL BOTTOM SHEET DRAWERS -->` markers
html = html.replace('<!-- ALL BOTTOM SHEET DRAWERS -->', '')

# Remove all empty lines caused by cleanup
html = re.sub(r'\n\s*\n', '\n\n', html)

# 2. Append audio nodes and closing tags to the very end
audio_block = """
<!-- Haptic audio simulation nodes -->
    <audio id="sndTap" src="https://assets.mixkit.co/active_storage/sfx/2568/2568-84.wav" preload="auto"></audio>
    <audio id="sndConfirm" src="https://assets.mixkit.co/active_storage/sfx/2019/2019-84.wav" preload="auto"></audio>
    <audio id="sndAlert" src="https://assets.mixkit.co/active_storage/sfx/911/911-84.wav" preload="auto"></audio>

    <script src="app.js?v=13"></script>
</body>
</html>
"""

# Wait, we need to make sure the wrappers are closed properly before the audio nodes.
# Let's count unclosed divs.
# Actually, the file structure should be:
# ...
# </div> <!-- End iphone-screen -->
# </div> <!-- End phone-container -->
# </div> <!-- End wrapper -->
# audio_block

# Let's just append audio_block for now.
with open('index.html.clean', 'w') as f:
    f.write(html + audio_block)

print("Cleaned up audio tags and markers.")
