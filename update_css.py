import re

with open('style.css', 'r') as f:
    content = f.read()

# Replace the 3D Seat Map Experience block
new_css = """
/* ==========================================================================
   TOP-DOWN 3D SEAT MAP EXPERIENCE
   ========================================================================== */

#screenSeatMap.active {
    display: flex !important;
    flex-direction: column;
}

.top-down-fuselage {
    background: #f8fafc;
    border: 8px solid #cbd5e1;
    border-radius: 60px;
    padding: 30px 20px;
    box-shadow: 
        inset 10px 0 20px rgba(0,0,0,0.03), 
        inset -10px 0 20px rgba(0,0,0,0.03), 
        inset 0 10px 20px rgba(0,0,0,0.05),
        0 20px 40px rgba(0,0,0,0.1);
    position: relative;
    width: 320px;
    margin: 0 auto;
}

/* Give the fuselage walls a 3D curved rim effect */
.top-down-fuselage::before {
    content: '';
    position: absolute;
    top: -8px; left: -8px; right: -8px; bottom: -8px;
    border-radius: 68px;
    border: 2px solid rgba(255,255,255,0.8);
    pointer-events: none;
}

.top-down-nose {
    position: absolute;
    top: -80px;
    left: -8px;
    right: -8px;
    height: 120px;
    background: #f8fafc;
    border: 8px solid #cbd5e1;
    border-bottom: none;
    border-radius: 160px 160px 0 0;
    box-shadow: inset 10px 10px 20px rgba(0,0,0,0.03), inset -10px 10px 20px rgba(0,0,0,0.03);
    z-index: 0;
}

.top-down-nose::after {
    content: '';
    position: absolute;
    top: 20px;
    left: 40px;
    right: 40px;
    height: 40px;
    background: #0f172a;
    border-radius: 20px 20px 10px 10px;
    opacity: 0.8;
}

.top-down-tail {
    position: absolute;
    bottom: -60px;
    left: -8px;
    right: -8px;
    height: 80px;
    background: #f8fafc;
    border: 8px solid #cbd5e1;
    border-top: none;
    border-radius: 0 0 160px 160px;
    box-shadow: inset 10px -10px 20px rgba(0,0,0,0.03), inset -10px -10px 20px rgba(0,0,0,0.03);
    z-index: 0;
}

.seat-grid {
    display: flex;
    flex-direction: column;
    gap: 12px;
    position: relative;
    z-index: 2;
}

.seat-row {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 6px;
    position: relative;
}

/* Wing exit indicator */
.seat-row.exit-row {
    margin-top: 16px;
    margin-bottom: 16px;
}
.seat-row.exit-row::before, .seat-row.exit-row::after {
    content: 'EXIT';
    position: absolute;
    font-size: 8px;
    font-weight: 800;
    color: #ef4444;
    letter-spacing: 1px;
}
.seat-row.exit-row::before { left: -16px; }
.seat-row.exit-row::after { right: -16px; }

.seat-aisle {
    width: 24px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 10px;
    font-weight: 800;
    color: #cbd5e1;
    letter-spacing: 1px;
}

/* Flat Seat Styling (Mockup inspired, but with subtle 3D lift) */
.seat-3d {
    width: 36px;
    height: 48px;
    border-radius: 6px;
    position: relative;
    cursor: pointer;
    background: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
    transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 4px 6px rgba(0,0,0,0.05), inset 0 2px 4px rgba(255,255,255,0.8);
    border: 1px solid #e2e8f0;
}

.seat-3d:active {
    transform: scale(0.95);
}

.seat-label {
    font-size: 12px;
    font-weight: 800;
    color: #0f172a;
    line-height: 1;
}

.seat-price {
    font-size: 8px;
    font-weight: 700;
    color: #64748b;
    margin-top: 4px;
}

/* Upfront Style */
.seat-upfront {
    background: #e0e7ff;
    border: 1px solid #a5b4fc;
}
.seat-upfront .seat-label { color: #3730a3; }
.seat-upfront .seat-price { color: #4f46e5; }

/* Emergency XL Style */
.seat-stretch {
    background: #ffedd5;
    border: 1px solid #fdba74;
}
.seat-stretch .seat-label { color: #9a3412; }
.seat-stretch .seat-price { color: #ea580c; }

/* Standard Style */
.seat-standard {
    background: #e0f2fe;
    border: 1px solid #7dd3fc;
}
.seat-standard .seat-label { color: #0369a1; }
.seat-standard .seat-price { color: #0284c7; }

/* Free Style */
.seat-free {
    background: #ffffff;
    border: 1px solid #86efac;
}
.seat-free .seat-label { color: #166534; }
.seat-free .seat-price { color: #22c55e; }

/* Occupied Style */
.seat-occupied {
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    cursor: not-allowed;
    opacity: 0.7;
}
.seat-occupied .seat-label { color: #94a3b8; }
.seat-occupied .seat-price { display: none; }

/* Selected State */
.seat-selected {
    background: #0066FF !important;
    border: 1px solid #0052cc !important;
    box-shadow: 0 8px 15px rgba(0, 102, 255, 0.3) !important;
    transform: translateY(-4px);
}
.seat-selected .seat-label { color: #ffffff !important; }
.seat-selected .seat-price { color: rgba(255,255,255,0.8) !important; }

.seat-pax-avatar {
    position: absolute;
    top: -10px;
    right: -10px;
    width: 22px;
    height: 22px;
    background: #0f172a;
    color: #fff;
    border-radius: 50%;
    font-size: 10px;
    font-weight: 800;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 2px solid #fff;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    z-index: 15;
    animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}

/* Quick Filter Pills */
.filter-pill {
    white-space: nowrap;
    padding: 8px 16px;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    color: #0f172a;
    display: flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
    transition: all 0.2s;
}
.filter-pill.active {
    background: #0f172a;
    color: #fff;
    border-color: #0f172a;
}
"""

start_str = "/* ==========================================================================\n   3D SEAT MAP EXPERIENCE\n   ========================================================================== */"
end_str = "/* Wing Overlay */"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    # Find the end of the Wing Overlay block to remove it entirely
    wing_overlay_end = content.find("}", end_idx)
    wing_overlay_end = content.find("}", wing_overlay_end + 1)
    wing_overlay_end = content.find("}", wing_overlay_end + 1) + 1 # 3 rules under Wing Overlay
    
    final_content = content[:start_idx] + new_css + content[wing_overlay_end:]
    with open('style.css', 'w') as f:
        f.write(final_content)
    print("CSS Updated Successfully")
else:
    print("Could not find CSS boundaries")

