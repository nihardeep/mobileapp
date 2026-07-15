css_code = """
/* ==========================================================================
   TIMELINE DIGITAL BOARDING PASS (Redesign)
   ========================================================================== */

/* Fullscreen QR Modal */
.bp-qr-fullscreen {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(255,255,255,0.98);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(10px);
}
.bp-qr-modal-content {
    text-align: center;
    position: relative;
    padding: 40px;
}
.bp-qr-close {
    position: absolute;
    top: -40px; right: 0;
    font-size: 24px; color: #0f172a;
    cursor: pointer; font-weight: 700;
}
.bp-qr-modal-title {
    font-size: 24px; font-weight: 900; color: #0f172a; margin-bottom: 30px;
}
.bp-qr-modal-img {
    width: 250px; height: 250px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    border-radius: 12px;
}
.bp-qr-modal-subtitle {
    margin-top: 20px; font-size: 14px; font-weight: 700; color: #64748b;
}

/* Header & Typography */
.bp-top-section {
    padding: 24px 20px 16px;
    border-bottom: 1px solid #e2e8f0;
    text-align: center;
}
.bp-header {
    display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;
}
.bp-title-small {
    font-size: 13px; color: #64748b; font-weight: 500;
}
.bp-pnr-tag {
    font-size: 11px; font-weight: 800; background: #f1f5f9; color: #0f172a;
    padding: 4px 8px; border-radius: 4px; letter-spacing: 0.5px;
}
.bp-passenger-name {
    font-size: 26px; font-weight: 900; color: #001b94;
    text-align: left; margin-top: 24px; letter-spacing: -0.5px;
}

/* 3D QR Flipper */
.bp-qr-flipper-wrapper {
    perspective: 1000px;
    cursor: pointer;
    margin: 0 auto;
    width: 100%;
}
.bp-qr-flipper {
    width: 100%;
    height: 120px;
    position: relative;
    transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    transform-style: preserve-3d;
}
.bp-qr-flipper.flipped {
    transform: rotateY(180deg);
}
.bp-qr-front, .bp-qr-back {
    width: 100%; height: 100%;
    position: absolute;
    backface-visibility: hidden;
    display: flex; flex-direction: column; align-items: center;
}
.bp-qr-back {
    transform: rotateY(180deg);
}
.bp-barcode-img {
    height: 80px; width: 100%; object-fit: cover; object-position: center;
    border-radius: 4px;
}
.bp-qr-subtitle {
    font-size: 10px; font-weight: 700; color: #64748b; margin-top: 8px; letter-spacing: 1px;
}

/* Toggle */
.bp-leg-toggle {
    display: flex; margin: 16px 20px; background: #f1f5f9; border-radius: 8px; padding: 4px;
}
.bp-toggle-btn {
    flex: 1; text-align: center; padding: 8px 0; font-size: 12px; font-weight: 800;
    color: #64748b; border-radius: 6px; cursor: pointer; transition: 0.3s;
}
.bp-toggle-btn.active {
    background: #fff; color: #001b94; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Timeline Layout */
.bp-timeline-wrapper {
    overflow: hidden;
    width: 100%;
}
.bp-timeline-slider {
    display: flex;
    width: 200%;
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.bp-timeline-leg {
    width: 50%;
    padding: 0 20px 24px;
}

.bp-timeline-header {
    display: flex; justify-content: space-between; align-items: flex-end;
    margin-bottom: 24px; margin-top: 16px;
}
.bp-tl-flight .lbl { font-size: 10px; color: #64748b; font-weight: 600; margin-bottom: 2px; }
.bp-tl-flight .val { font-size: 16px; font-weight: 900; color: #0f172a; margin-bottom: 4px; }
.bp-tl-route { display: flex; align-items: center; gap: 8px; }
.bp-tl-route .city { font-size: 24px; font-weight: 300; color: var(--xairline-blue); }
.bp-tl-route .icon { font-size: 16px; color: #001b94; transform: rotate(90deg); }

/* Vertical Timeline Lines */
.bp-timeline-line {
    position: relative;
    padding-left: 20px;
}
.bp-timeline-line::before {
    content: ''; position: absolute; top: 12px; bottom: 24px; left: 6px;
    width: 2px; background: #001b94;
}

.bp-tl-node {
    position: relative; margin-bottom: 24px;
    display: grid; grid-template-columns: 1fr 60px 80px; gap: 8px; align-items: center;
}
.bp-tl-node:last-child { margin-bottom: 0; }

.bp-tl-node .dot {
    position: absolute; left: -21.5px; top: 12px; transform: translateY(-50%);
    width: 14px; height: 14px; border-radius: 50%; background: #fff;
    border: 3px solid #001b94; z-index: 2;
}
.bp-tl-node .dot.solid { background: #001b94; }
.bp-tl-node .dot.red-dot { border-color: #ef4444; }

.bp-tl-node .title { font-size: 14px; font-weight: 800; color: #001b94; }
.bp-tl-node .time { font-size: 13px; font-weight: 500; color: #475569; text-align: right; }
.bp-tl-node .time.bold { font-weight: 900; font-size: 15px; color: #0f172a; }
.bp-tl-node .desc { font-size: 11px; color: #64748b; text-align: right; }

.bp-tl-node.active {
    background: #001b94;
    margin-left: -32px; padding-left: 32px; padding-right: 12px; padding-top: 16px; padding-bottom: 16px;
    border-radius: 20px; width: calc(100% + 32px + 12px);
}
.bp-tl-node.active .title, .bp-tl-node.active .time, .bp-tl-node.active .desc { color: #fff; }
.bp-tl-node.active .dot { left: 10.5px; border-color: #fff; top: 50%; }

.bp-tl-warning {
    display: flex; align-items: center; gap: 6px; font-size: 9px; color: #64748b; font-weight: 600;
    margin-top: 24px; padding-top: 16px; border-top: 1px solid #e2e8f0;
}
.red-dot-small { width: 6px; height: 6px; background: #ef4444; border-radius: 50%; }

"""

with open('style.css', 'a', encoding='utf-8') as f:
    f.write(css_code)

print("CSS appended.")
