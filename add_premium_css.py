with open('style.css', 'r') as f:
    css = f.read()

premium_css = """
/* ==========================================================================
   PREMIUM UPFRONT CARD (Dark Theme)
   ========================================================================== */
.upgrade-promo-card.premium-dark {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-left: none; /* remove old accent */
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2), inset 0 1px 1px rgba(255,255,255,0.1);
    position: relative;
    overflow: hidden;
    color: white;
}

/* Shimmer Animation */
.shimmer-overlay {
    position: absolute;
    top: 0;
    left: -100%;
    width: 50%;
    height: 100%;
    background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0) 100%);
    transform: skewX(-20deg);
    animation: shimmerSweep 4s infinite;
    z-index: 1;
    pointer-events: none;
}

@keyframes shimmerSweep {
    0% { left: -100%; }
    20% { left: 200%; }
    100% { left: 200%; }
}

.premium-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    position: relative;
    z-index: 2;
}

.premium-tag {
    font-size: 9px;
    font-weight: 800;
    color: #eab308; /* Premium gold accent */
    letter-spacing: 0.5px;
    background: rgba(234, 179, 8, 0.15);
    padding: 3px 8px;
    border-radius: 12px;
    display: flex;
    align-items: center;
}

.premium-price {
    font-size: 16px;
    font-weight: 800;
    color: #fff;
}

.premium-promo-title {
    font-size: 18px;
    color: rgba(255, 255, 255, 0.9);
    line-height: 1.2;
    margin-bottom: 4px;
    position: relative;
    z-index: 2;
}

.premium-promo-subtitle {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
    line-height: 1.4;
    margin-bottom: 12px;
    position: relative;
    z-index: 2;
}

.premium-benefits-row {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
    position: relative;
    z-index: 2;
}

.premium-benefit-tag {
    font-size: 10px;
    font-weight: 500;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(4px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 6px 10px;
    border-radius: 8px;
    color: #fff;
    display: flex;
    align-items: center;
}

.premium-action-btn {
    width: 100%;
    padding: 12px;
    border-radius: 12px;
    background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    font-size: 14px;
    font-weight: 700;
    border: none;
    cursor: pointer;
    position: relative;
    z-index: 2;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.premium-action-btn:active {
    box-shadow: 0 2px 6px rgba(37, 99, 235, 0.4);
}
"""

if "PREMIUM UPFRONT CARD (Dark Theme)" not in css:
    with open('style.css', 'a') as f:
        f.write("\n" + premium_css)
    print("Added premium CSS")
else:
    print("Already added")
