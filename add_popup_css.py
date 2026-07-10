import re

with open('style.css', 'r') as f:
    css = f.read()

# Replace inline CSS with Popup CSS
new_css = """
/* Centered Popup 3D Carousel Styles */
.centered-popup-overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.6);
    z-index: 2500;
    display: flex;
    justify-content: center;
    align-items: center;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
}

.centered-popup-overlay.active {
    opacity: 1;
    pointer-events: auto;
}

.centered-popup-content {
    width: 90%;
    max-width: 400px;
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    display: flex;
    flex-direction: column;
    transform: scale(0.95);
    opacity: 0;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    overflow: hidden;
}

.centered-popup-overlay.active .centered-popup-content {
    transform: scale(1);
    opacity: 1;
}

.cp-segment-control {
    display: flex;
    background: #FAFAFA;
    border: 1px solid rgba(0, 95, 169, 0.2);
    border-radius: 8px;
    overflow: hidden;
}

.cp-segment {
    flex: 1;
    text-align: center;
    padding: 10px 0;
    font-size: 13px;
    font-weight: 700;
    color: var(--indigo-blue);
    cursor: pointer;
    transition: all 0.2s ease;
}

.cp-segment.active {
    background: rgba(0, 95, 169, 0.08);
}

.cp-carousel-container {
    width: 100%;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    scroll-behavior: smooth;
    display: flex;
    padding-bottom: 24px;
}

.cp-carousel-container::-webkit-scrollbar {
    display: none;
}

.cp-carousel-track {
    display: flex;
    align-items: center;
    gap: 0px; /* Overlap is handled by margins */
}

/* 
  The padder elements ensure the first and last cards 
  can snap perfectly to the center of the viewport 
*/
.cp-carousel-padder {
    flex: 0 0 calc(50% - 100px); /* Assuming card width ~200px */
}

.cp-3d-card {
    flex: 0 0 200px;
    scroll-snap-align: center;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid #E0E0E0;
    border-radius: 12px;
    margin: 0 -10px; /* Slight overlap */
    transition: transform 0.3s ease, opacity 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease, z-index 0.3s ease;
    transform: scale(0.85);
    opacity: 0.5;
    z-index: 1;
    display: flex;
    flex-direction: column;
}

.cp-3d-card.active-center {
    transform: scale(1.0);
    opacity: 1;
    z-index: 10;
    background: #fff;
    border: 2px solid var(--indigo-blue);
    box-shadow: 0 12px 30px rgba(0, 95, 169, 0.2);
}

.cp-3d-card.stretch-mode.active-center {
    border-color: #D4AF37;
    box-shadow: 0 12px 30px rgba(212, 175, 55, 0.2);
}

.cp-card-header {
    padding: 12px;
    text-align: center;
    font-size: 15px;
    font-weight: 800;
    color: #666;
    border-bottom: 1px solid #E0E0E0;
}

.cp-3d-card.active-center .cp-card-header {
    color: var(--indigo-blue);
}
.cp-3d-card.stretch-mode.active-center .cp-card-header {
    color: #D4AF37;
}

.cp-popular-badge {
    background: #00C3F8;
    color: #fff;
    font-size: 10px;
    font-weight: 800;
    text-align: center;
    padding: 6px 0;
    text-transform: uppercase;
}

.cp-popular-badge.stretch-badge {
    background: #FDF7E7;
    color: #D4AF37;
}

.cp-card-features {
    padding: 12px;
    flex-grow: 1;
}

.cp-feature-item {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    margin-bottom: 8px;
    font-size: 11px;
    color: #333;
}

.cp-feature-item svg {
    flex-shrink: 0;
    color: #4CAF50;
    margin-top: 1px;
}

.cp-feature-item.cross { color: #999; }
.cp-feature-item.cross svg { color: #999; }

.cp-pricing-block {
    text-align: center;
    padding: 12px;
    background: #FAFAFA;
    border-top: 1px solid rgba(0,0,0,0.05);
}

.cp-compare-link {
    display: inline-block;
    color: var(--indigo-blue);
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    text-decoration: underline;
    text-underline-offset: 2px;
}

.cp-sticky-footer {
    padding: 16px 20px;
    background: #FAFAFA;
    border-top: 1px solid #E0E0E0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
"""

if ".centered-popup-overlay" not in css:
    css += "\n" + new_css
    with open('style.css', 'w') as f:
        f.write(css)
    print("Added Popup CSS.")
else:
    print("Popup CSS already present.")
