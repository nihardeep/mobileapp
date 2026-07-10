with open('style.css', 'a') as f:
    f.write('''

/* ==========================================================================
   ADD-ONS: RADICAL REDESIGN CSS
   ========================================================================== */

/* Passenger Dynamic Island */
#addonPaxCartContainer {
    scroll-behavior: smooth;
}
.dynamic-pax-chip {
    flex: 0 0 auto;
    padding: 10px 16px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    min-width: 130px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}
.dynamic-pax-chip.active {
    border-color: var(--indigo-blue);
    background: #f8fafc;
    transform: scale(1.05);
    box-shadow: 0 10px 20px -5px rgba(0, 27, 148, 0.15);
}
.dynamic-pax-chip .pax-name {
    font-size: 13px;
    font-weight: 800;
    color: #0f172a;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.dynamic-pax-chip .pax-subtotal {
    font-size: 11px;
    font-weight: 700;
    color: var(--indigo-blue);
    margin-top: 4px;
}

/* Scroll Spy Tabs */
.addon-spy-tabs {
    display: flex;
    gap: 24px;
    padding: 16px 24px 0;
    overflow-x: auto;
    -ms-overflow-style: none;
    scrollbar-width: none;
    position: relative;
}
.addon-spy-tabs::-webkit-scrollbar { display: none; }

.spy-tab {
    padding-bottom: 12px;
    font-size: 13px;
    font-weight: 700;
    color: #64748b;
    position: relative;
    white-space: nowrap;
    cursor: pointer;
    transition: color 0.2s ease;
}
.spy-tab.active {
    color: var(--indigo-blue);
}
.spy-tab.active::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--indigo-blue);
    border-radius: 3px 3px 0 0;
}

/* Premium Dark Mode Bundle */
.premium-bundle-card {
    background: #0f172a;
    border-radius: 16px;
    padding: 24px;
    position: relative;
    overflow: hidden;
    margin-bottom: 20px;
    box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.5);
    border: 1px solid #1e293b;
}
.bundle-glow {
    position: absolute;
    top: -50px;
    right: -50px;
    width: 150px;
    height: 150px;
    background: radial-gradient(circle, rgba(59,130,246,0.3) 0%, rgba(15,23,42,0) 70%);
    border-radius: 50%;
    z-index: 1;
}
.bundle-icon-pill {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    color: #e2e8f0;
    display: flex;
    align-items: center;
    gap: 6px;
}
.neon-add-btn {
    background: #3b82f6;
    color: white;
    border: none;
    padding: 10px 24px;
    border-radius: 30px;
    font-size: 13px;
    font-weight: 800;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    transition: all 0.2s ease;
}
.neon-add-btn.added {
    background: rgba(255,255,255,0.1);
    color: #e2e8f0;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: none;
}

/* Smart Bundle */
.smart-bundle-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.05);
}
.standard-add-btn {
    background: #ffffff;
    color: var(--indigo-blue);
    border: 1.5px solid var(--indigo-blue);
    padding: 8px 24px;
    border-radius: 30px;
    font-size: 13px;
    font-weight: 800;
    cursor: pointer;
}
.standard-add-btn.added {
    background: #f1f5f9;
    color: #64748b;
    border-color: #cbd5e1;
}

/* Immersive Meals */
.meal-filter {
    padding: 6px 16px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    color: #64748b;
    cursor: pointer;
}
.meal-filter.active {
    background: #ffffff;
    color: #0f172a;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.meal-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}
.immersive-meal-card {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    height: 200px;
    box-shadow: 0 10px 20px -5px rgba(0,0,0,0.1);
}
.meal-bg {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}
.immersive-meal-card:active .meal-bg {
    transform: scale(1.05);
}
.meal-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.8) 100%);
    padding: 12px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.meal-diet-tag {
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(4px);
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 10px;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 4px;
}
.meal-diet-tag.veg { color: #15803d; }
.meal-diet-tag.nonveg { color: #b91c1c; }
.veg-dot { width: 6px; height: 6px; border-radius: 50%; background: #22c55e; }
.nonveg-dot { width: 6px; height: 6px; border-radius: 50%; background: #ef4444; }

.glass-price {
    font-size: 16px;
    font-weight: 900;
    color: #ffffff;
}
.glass-add-btn {
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.4);
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 800;
    cursor: pointer;
}
.glass-add-btn.added {
    background: #22c55e;
    border-color: #22c55e;
}

/* Celebration Banners */
.celebration-banner {
    display: none;
    background: linear-gradient(to right, #f0fdf4, #dcfce7);
    border: 1px solid #bbf7d0;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 20px;
    align-items: center;
    gap: 16px;
    box-shadow: 0 4px 12px rgba(34, 197, 94, 0.1);
}
.celebration-icon {
    font-size: 24px;
    background: white;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    box-shadow: 0 4px 8px rgba(0,0,0,0.05);
}

/* Stepper */
.stepper-btn {
    width: 40px;
    height: 40px;
    background: #ffffff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: 500;
    color: var(--indigo-blue);
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.stepper-btn:active {
    transform: scale(0.95);
}

''')
