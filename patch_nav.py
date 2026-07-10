import re

with open('app.js', 'r') as f:
    content = f.read()

# Let's find the navigateTo function
if "function navigateTo(" in content:
    replacement = """function navigateTo(screenId) {
    if (typeof triggerHaptic === 'function') triggerHaptic('light', 'Navigation');
    
    // Close all drawers first
    if (typeof closeAllDrawers === 'function') closeAllDrawers();
    
    // Check upfront state for addon CTA button
    if (screenId === 'addons' && window.appState && window.appState.upfrontUnlocked) {
        const btn = document.getElementById('addonChooseSeatBtn');
        if (btn) btn.innerText = 'Next: Choose Free Seat';
    }
"""
    content = re.sub(r'function navigateTo\([^)]+\)\s*\{[\s\S]*?(?=// Remove active class)', replacement + '\n    // Remove active class', content, count=1)
    
    with open('app.js', 'w') as f:
        f.write(content)
    print("Patched navigateTo")
else:
    print("navigateTo not found")
