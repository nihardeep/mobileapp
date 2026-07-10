import sys

with open('app.js', 'r') as f:
    content = f.read()

zoom_code = """
// --- Zoom Controls ---
function handleZoomIn() {
    if (typeof seatMapPanState !== 'undefined') {
        seatMapPanState.scale += 0.1;
        if (seatMapPanState.scale > 2.5) seatMapPanState.scale = 2.5;
        if (typeof updateSeatMapTransform === 'function') {
            updateSeatMapTransform();
        }
        if (typeof triggerHaptic === 'function') {
            triggerHaptic('light', 'Zoom In');
        }
    }
}

function handleZoomOut() {
    if (typeof seatMapPanState !== 'undefined') {
        seatMapPanState.scale -= 0.1;
        if (seatMapPanState.scale < 0.4) seatMapPanState.scale = 0.4;
        if (typeof updateSeatMapTransform === 'function') {
            updateSeatMapTransform();
        }
        if (typeof triggerHaptic === 'function') {
            triggerHaptic('light', 'Zoom Out');
        }
    }
}
"""

if "handleZoomIn" not in content:
    with open('app.js', 'a') as f:
        f.write(zoom_code)
    print("Zoom code added to app.js")
else:
    print("Zoom code already exists")
