import re

with open('app.js', 'r') as f:
    js = f.read()

# Make sure closeAllDrawers closes passengerFormSheet
old_close = """function closeAllDrawers() {
    const backdrop = document.getElementById('bottomSheetBackdrop');
    const drawers = document.querySelectorAll('.bottom-sheet-drawer');
    
    if (backdrop && drawers.length > 0) {
        let anyVisible = backdrop.classList.contains('visible');
        if (anyVisible) {
            triggerHaptic('light', 'Close selection panel');
            backdrop.classList.remove('visible');
            drawers.forEach(dr => dr.classList.remove('visible'));
        }
    }
}"""

new_close = """function closeAllDrawers() {
    const backdrop = document.getElementById('bottomSheetBackdrop');
    const drawers = document.querySelectorAll('.bottom-sheet-drawer');
    
    if (backdrop) backdrop.classList.remove('visible');
    if (drawers.length > 0) {
        drawers.forEach(dr => dr.classList.remove('visible'));
    }
    
    // Explicitly target passenger form just in case
    const paxForm = document.getElementById('passengerFormSheet');
    if (paxForm) paxForm.classList.remove('visible');
}"""

js = js.replace(old_close, new_close)

with open('app.js', 'w') as f:
    f.write(js)
