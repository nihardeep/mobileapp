import re

with open('style.css', 'r') as f:
    css = f.read()

new_css = """
/* ==========================================================================
   SEAT MAP 3D & PAN/ZOOM
   ========================================================================== */

#screenSeatMap.active {
    display: flex !important;
    flex-direction: column;
}

#screenSeatLoading.active {
    display: flex !important;
}

.is-3d-vertical {
    transform: rotateX(20deg) scale(0.9);
    box-shadow: 
        inset 10px 0 20px rgba(0,0,0,0.03), 
        inset -10px 0 20px rgba(0,0,0,0.03), 
        inset 0 10px 20px rgba(0,0,0,0.05),
        0 40px 60px rgba(0,0,0,0.15) !important;
}

.is-3d-horizontal {
    transform: rotateZ(-90deg) rotateX(15deg) scale(0.8);
    box-shadow: 
        inset 10px 0 20px rgba(0,0,0,0.03), 
        inset -10px 0 20px rgba(0,0,0,0.03), 
        inset 0 10px 20px rgba(0,0,0,0.05),
        -40px 40px 60px rgba(0,0,0,0.15) !important;
}

/* Ensure fuselage has transition when toggling views */
.top-down-fuselage {
    transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.5s;
    transform-origin: center top;
}
"""

css += new_css

with open('style.css', 'w') as f:
    f.write(css)

with open('app.js', 'r') as f:
    js = f.read()

# Update navigateTo logic for 'seatmap_loading'
nav_replacement = """function navigateTo(screenName) {
    const screens = document.querySelectorAll('.screen');
    screens.forEach(s => s.classList.remove('active'));
    
    // Hide footer explicitly for some screens
    const bottomNav = document.querySelector('.bottom-nav');
    if (bottomNav) {
        bottomNav.style.display = (screenName === 'addons' || screenName === 'passenger' || screenName === 'seatmap' || screenName === 'seatmap_loading') ? 'none' : '';
    }

    if (screenName === 'seatmap_loading') {
        const loadingScreen = document.getElementById('screenSeatLoading');
        if (loadingScreen) loadingScreen.classList.add('active');
        
        // Trigger plane animation
        setTimeout(() => {
            const plane = document.getElementById('seatLoadingPlane');
            if (plane) {
                plane.style.opacity = '1';
                plane.style.transform = 'translateY(-100px) scale(1.1)';
            }
        }, 100);
        
        // Navigate to real seatmap after 2.5s
        setTimeout(() => {
            navigateTo('seatmap');
        }, 2500);
        return;
    }
"""

js = js.replace("function navigateTo(screenName) {", nav_replacement, 1)

# Add Pan Zoom logic
pan_zoom_js = """
// ==========================================================================
// SEAT MAP PAN, ZOOM & ROTATE
// ==========================================================================

let seatMapPanState = {
    isDragging: false,
    startX: 0,
    startY: 0,
    x: 0,
    y: 0,
    scale: 1,
    is3DHorizontal: false
};

function initSeatMapPanZoom() {
    const container = document.getElementById('seatMapTransformContainer');
    const wrapper = document.getElementById('seatMapPanZoomArea');
    if (!container || !wrapper) return;
    
    // Reset state
    seatMapPanState.x = 0;
    seatMapPanState.y = 0;
    seatMapPanState.scale = 1;
    updateSeatMapTransform();

    // Touch events for drag
    wrapper.addEventListener('touchstart', (e) => {
        if (e.touches.length === 1) {
            seatMapPanState.isDragging = true;
            seatMapPanState.startX = e.touches[0].clientX - seatMapPanState.x;
            seatMapPanState.startY = e.touches[0].clientY - seatMapPanState.y;
        }
    }, { passive: false });

    wrapper.addEventListener('touchmove', (e) => {
        if (!seatMapPanState.isDragging || e.touches.length !== 1) return;
        e.preventDefault(); // Prevent native scroll
        seatMapPanState.x = e.touches[0].clientX - seatMapPanState.startX;
        seatMapPanState.y = e.touches[0].clientY - seatMapPanState.startY;
        
        // Constrain Y to prevent dragging off screen entirely
        if (seatMapPanState.y > 200) seatMapPanState.y = 200;
        if (seatMapPanState.y < -1500) seatMapPanState.y = -1500;
        
        updateSeatMapTransform();
    }, { passive: false });

    wrapper.addEventListener('touchend', () => {
        seatMapPanState.isDragging = false;
    });
}

function updateSeatMapTransform() {
    const container = document.getElementById('seatMapTransformContainer');
    if (container) {
        container.style.transform = `translate(${seatMapPanState.x}px, ${seatMapPanState.y}px) scale(${seatMapPanState.scale})`;
    }
}

function toggleSeatMap3DView() {
    triggerHaptic('medium', 'Toggle 3D View');
    seatMapPanState.is3DHorizontal = !seatMapPanState.is3DHorizontal;
    const fuselage = document.getElementById('seatMapFuselage');
    if (fuselage) {
        if (seatMapPanState.is3DHorizontal) {
            fuselage.classList.remove('is-3d-vertical');
            fuselage.classList.add('is-3d-horizontal');
        } else {
            fuselage.classList.remove('is-3d-horizontal');
            fuselage.classList.add('is-3d-vertical');
        }
    }
}

// Hook it into initSeatMapScreen
const oldInitSeatMapScreen = initSeatMapScreen;
initSeatMapScreen = function() {
    oldInitSeatMapScreen();
    initSeatMapPanZoom();
};

"""

js += pan_zoom_js

with open('app.js', 'w') as f:
    f.write(js)

