import re

with open('app.js', 'r') as f:
    content = f.read()

# Replace navigateToSeatmapAndMakeFree
pattern = re.compile(r'function navigateToSeatmapAndMakeFree\(\) \{.*?\n\}', re.DOTALL)
replacement = """function navigateToSeatmapAndMakeFree() {
    if(typeof triggerHaptic === 'function') triggerHaptic('medium', 'Addons');
    if(typeof navigateTo === 'function') navigateTo('addons');
}"""

# Find the start and end of navigateToSeatmapAndMakeFree correctly
# Since it might have a settimeout inside it, regex might not catch the closing brace properly if there are nested braces.
