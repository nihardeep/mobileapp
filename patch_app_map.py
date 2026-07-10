import re

with open('app.js', 'r') as f:
    content = f.read()

# Add Map Interaction JS to app.js
map_js = """
// ==========================================================================
// INTERACTIVE MAP CONTROLLER (Pan, Zoom, Search)
// ==========================================================================

const mapCities = [
    { name: "London", country: "UK", x: 450, y: 150 },
    { name: "Paris", country: "France", x: 460, y: 165 },
    { name: "New York", country: "USA", x: 260, y: 190 },
    { name: "Tokyo", country: "Japan", x: 820, y: 200 },
    { name: "Dubai", country: "UAE", x: 570, y: 240 },
    { name: "Mumbai", country: "India", x: 650, y: 260 },
    { name: "Delhi", country: "India", x: 655, y: 235 },
    { name: "Singapore", country: "Singapore", x: 730, y: 340 },
    { name: "Sydney", country: "Australia", x: 850, y: 480 },
    { name: "Cape Town", country: "South Africa", x: 500, y: 470 },
    { name: "Rio de Janeiro", country: "Brazil", x: 330, y: 420 },
    { name: "Los Angeles", country: "USA", x: 140, y: 210 }
];

let mapScale = 1;
let mapTx = 0;
let mapTy = 0;
let isPanning = false;
let startPanX = 0;
let startPanY = 0;
let initialDist = 0;
let touchMode = 'none'; // none, scroll, pan, zoom

function initMapInteractions() {
    const wrapper = document.getElementById('mapWrapper');
    const transformLayer = document.getElementById('mapTransformLayer');
    const warning = document.getElementById('mapScrollWarning');
    if (!wrapper || !transformLayer) return;

    // Center map initially (assuming 950x620 SVG in a ~360x220 container)
    // We want to scale it down to fit or start zoomed into a specific area (e.g. Europe/Asia)
    mapScale = 0.6;
    mapTx = -100;
    mapTy = -50;
    updateMapTransform(false);

    wrapper.addEventListener('touchstart', (e) => {
        if (e.touches.length === 1) {
            touchMode = 'scroll';
            // Allow vertical scroll, but warn user if they try to drag horizontally
            startPanX = e.touches[0].clientX;
            startPanY = e.touches[0].clientY;
        } else if (e.touches.length === 2) {
            e.preventDefault();
            touchMode = 'zoom';
            isPanning = true;
            initialDist = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
            startPanX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
            startPanY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
            warning.style.opacity = '0';
        }
    }, { passive: false });

    wrapper.addEventListener('touchmove', (e) => {
        if (touchMode === 'scroll') {
            const dx = Math.abs(e.touches[0].clientX - startPanX);
            const dy = Math.abs(e.touches[0].clientY - startPanY);
            if (dx > 10 && dy < 30) {
                // User is trying to pan horizontally with one finger
                warning.style.opacity = '1';
                e.preventDefault();
            } else {
                warning.style.opacity = '0';
            }
        } else if (touchMode === 'zoom' && e.touches.length === 2) {
            e.preventDefault();
            
            // Handle Zoom
            const newDist = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
            const scaleChange = newDist / initialDist;
            let newScale = mapScale * scaleChange;
            newScale = Math.max(0.3, Math.min(newScale, 3)); // clamp scale
            
            // Handle Pan
            const currentX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
            const currentY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
            
            mapTx += (currentX - startPanX);
            mapTy += (currentY - startPanY);
            
            mapScale = newScale;
            initialDist = newDist;
            startPanX = currentX;
            startPanY = currentY;
            
            updateMapTransform(false);
        }
    }, { passive: false });

    wrapper.addEventListener('touchend', (e) => {
        if (e.touches.length < 2) {
            isPanning = false;
            touchMode = 'none';
        }
        warning.style.opacity = '0';
    });
    
    // Mouse fallback for desktop testing
    wrapper.addEventListener('mousedown', (e) => {
        isPanning = true;
        startPanX = e.clientX;
        startPanY = e.clientY;
        transformLayer.style.transition = 'none';
    });
    window.addEventListener('mousemove', (e) => {
        if (!isPanning) return;
        mapTx += (e.clientX - startPanX);
        mapTy += (e.clientY - startPanY);
        startPanX = e.clientX;
        startPanY = e.clientY;
        updateMapTransform(false);
    });
    window.addEventListener('mouseup', () => {
        isPanning = false;
        transformLayer.style.transition = 'transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1)';
    });
}

function updateMapTransform(animate = true) {
    const layer = document.getElementById('mapTransformLayer');
    if (layer) {
        if (animate) layer.style.transition = 'transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1)';
        else layer.style.transition = 'none';
        layer.style.transform = `translate(${mapTx}px, ${mapTy}px) scale(${mapScale})`;
    }
}

window.handleMapSearch = function(query) {
    const resultsDiv = document.getElementById('mapSearchResults');
    if (!query || query.length < 2) {
        resultsDiv.style.display = 'none';
        return;
    }
    
    const q = query.toLowerCase();
    const matches = mapCities.filter(c => c.name.toLowerCase().includes(q) || c.country.toLowerCase().includes(q));
    
    if (matches.length > 0) {
        resultsDiv.style.display = 'block';
        resultsDiv.innerHTML = matches.map(c => `
            <div style="padding: 12px 16px; border-bottom: 1px solid #f1f5f9; display: flex; align-items: center; gap: 12px; cursor: pointer;" onclick="zoomToMapCity('${c.name}')">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#0f172a" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                <div>
                    <div style="font-weight: 700; font-size: 14px; color: #0f172a;">${c.name}</div>
                    <div style="font-weight: 600; font-size: 11px; color: #64748b;">${c.country}</div>
                </div>
            </div>
        `).join('');
    } else {
        resultsDiv.style.display = 'none';
    }
}

window.zoomToMapCity = function(cityName) {
    const city = mapCities.find(c => c.name === cityName);
    if (!city) return;
    
    document.getElementById('mapSearchInput').value = cityName;
    document.getElementById('mapSearchResults').style.display = 'none';
    
    // Zoom in logic
    mapScale = 1.8;
    
    // Viewport dimensions (roughly 360x220 for mobile embedded view)
    const vw = document.getElementById('mapWrapper').offsetWidth || 360;
    const vh = document.getElementById('mapWrapper').offsetHeight || 220;
    
    // Center the targeted X,Y coordinates
    mapTx = (vw / 2) - (city.x * mapScale);
    mapTy = (vh / 2) - (city.y * mapScale);
    
    updateMapTransform(true);
    triggerHaptic('heavy', `Zoomed to ${cityName}`);
    
    // Drop Pin
    const pinsLayer = document.getElementById('mapPinsLayer');
    if (pinsLayer) {
        pinsLayer.innerHTML = `
            <div style="position: absolute; left: ${city.x}px; top: ${city.y}px; transform: translate(-50%, -100%); width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; animation: dropPin 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;">
                <svg viewBox="0 0 24 24" width="32" height="32" fill="#e84b38" stroke="#fff" stroke-width="1.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3" fill="#fff"></circle></svg>
            </div>
        `;
    }
}

// Add dropPin animation to document
const style = document.createElement('style');
style.textContent = `
    @keyframes dropPin {
        0% { transform: translate(-50%, -150%) scale(0); opacity: 0; }
        100% { transform: translate(-50%, -100%) scale(1); opacity: 1; }
    }
`;
document.head.appendChild(style);

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(initMapInteractions, 500);
});
"""

if "initMapInteractions" not in content:
    with open('app.js', 'a') as f:
        f.write("\n" + map_js)
    print("app.js patched!")
else:
    print("Already patched.")

