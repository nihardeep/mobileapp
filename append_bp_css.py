css_code = """
/* ==========================================================================
   DIGITAL BOARDING PASS UI (My Trips Tab)
   ========================================================================== */
   
.bp-demo-panel {
    display: flex;
    justify-content: center;
    gap: 10px;
    padding: 20px 20px 10px;
    background: #f4f6f8;
}

.bp-demo-btn {
    padding: 8px 12px;
    border: 1px solid #cbd5e1;
    background: #fff;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    color: #475569;
    cursor: pointer;
    transition: all 0.2s;
}

.bp-demo-btn.active {
    background: var(--xairline-blue);
    color: #fff;
    border-color: var(--xairline-blue);
}

.bp-carousel-container {
    width: 100%;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    scroll-behavior: smooth;
    padding: 20px 0;
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.bp-carousel-container::-webkit-scrollbar {
    display: none;
}

.bp-carousel-track {
    display: flex;
    width: max-content;
    padding: 0 20px;
}

.bp-slide {
    width: calc(385px - 40px);
    flex-shrink: 0;
    scroll-snap-align: center;
    margin-right: 20px;
}

.bp-slide:last-child {
    margin-right: 0;
}

/* Skeuomorphic Boarding Pass */
.digital-bp {
    background: #ffffff;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08), 0 1px 3px rgba(0,0,0,0.03);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.bp-header {
    background: #f8fafc;
    padding: 16px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e2e8f0;
}

.bp-airline {
    font-weight: 900;
    font-style: italic;
    font-size: 16px;
    color: var(--xairline-blue);
    letter-spacing: -0.5px;
}

.bp-pnr {
    font-size: 11px;
    font-weight: 600;
    color: #64748b;
}

.bp-mono {
    font-family: monospace;
    font-size: 14px;
    font-weight: 700;
    color: #0f172a;
    background: #e2e8f0;
    padding: 2px 6px;
    border-radius: 4px;
    margin-left: 4px;
}

.bp-leg {
    padding: 20px;
    position: relative;
    transition: opacity 0.3s ease;
}

.bp-leg.dimmed {
    opacity: 0.4;
    pointer-events: none;
}

.bp-route {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
}

.bp-route.small .bp-code {
    font-size: 28px;
}
.bp-route.small .bp-time {
    font-size: 11px;
}

.bp-city {
    display: flex;
    flex-direction: column;
}

.bp-city.right {
    text-align: right;
}

.bp-time {
    font-size: 12px;
    font-weight: 700;
    color: #64748b;
    margin-bottom: 2px;
}

.bp-code {
    font-size: 36px;
    font-weight: 900;
    color: #0f172a;
    line-height: 1;
    letter-spacing: -1px;
}

.bp-flight-icon {
    font-size: 24px;
    color: #cbd5e1;
    transform: rotate(90deg);
}

.bp-details-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
}

.bp-detail-item label {
    font-size: 9px;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    display: block;
    margin-bottom: 4px;
}

.bp-detail-item .val {
    font-size: 13px;
    font-weight: 800;
    color: #0f172a;
}

.bp-detail-item .text-red {
    color: #ef4444;
}

.bp-detail-item.highlight .val {
    color: var(--xairline-blue);
    font-size: 18px;
}

/* Perforation Divider */
.bp-divider {
    height: 2px;
    background-image: linear-gradient(to right, #cbd5e1 50%, transparent 50%);
    background-size: 12px 2px;
    background-repeat: repeat-x;
    position: relative;
    margin: 0;
}

.bp-divider .notch {
    position: absolute;
    width: 24px;
    height: 24px;
    background: #f4f6f8; /* Matches page background */
    border-radius: 50%;
    top: -12px;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
}

.bp-divider .notch.left {
    left: -12px;
}

.bp-divider .notch.right {
    right: -12px;
}

/* Completed Overlay */
.bp-completed-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255,255,255,0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
    z-index: 2;
}

.bp-completed-overlay.show {
    opacity: 1;
}

.completed-stamp {
    border: 3px solid #10b981;
    color: #10b981;
    font-size: 14px;
    font-weight: 900;
    padding: 8px 16px;
    border-radius: 8px;
    transform: rotate(-15deg);
    letter-spacing: 1px;
}

/* Footer / QR */
.bp-footer {
    background: #f8fafc;
    padding: 24px 20px;
    display: flex;
    justify-content: center;
    border-top: 1px solid #e2e8f0;
}

.bp-qr-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
}

.bp-qr {
    width: 120px;
    height: 120px;
    border-radius: 8px;
    margin-bottom: 8px;
    background: #fff;
    padding: 8px;
    border: 1px solid #e2e8f0;
}

.bp-scan-hint {
    font-size: 10px;
    font-weight: 700;
    color: #64748b;
    letter-spacing: 0.5px;
}

.bp-dots {
    display: flex;
    justify-content: center;
    gap: 8px;
    padding-bottom: 30px;
}

.bp-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #cbd5e1;
    transition: all 0.3s;
    cursor: pointer;
}

.bp-dot.active {
    background: var(--xairline-blue);
    width: 16px;
    border-radius: 4px;
}
"""

with open('style.css', 'a', encoding='utf-8') as f:
    f.write(css_code)

print("CSS added.")
