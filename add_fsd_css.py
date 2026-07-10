import re

with open('style.css', 'r') as f:
    css = f.read()

new_css = """
/* Fare Selection Drawer Styles */
.fsd-segment-control {
    display: flex;
    background: #fff;
    border: 1px solid rgba(0, 95, 169, 0.2);
    border-radius: 8px;
    overflow: hidden;
}

.fsd-segment {
    flex: 1;
    text-align: center;
    padding: 12px 0;
    font-size: 14px;
    font-weight: 700;
    color: var(--indigo-blue);
    cursor: pointer;
    transition: all 0.2s ease;
}

.fsd-segment.active {
    background: rgba(0, 95, 169, 0.05);
}

.fsd-cards-scroll-area {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    gap: 16px;
    padding: 0 20px 20px 20px;
    flex-grow: 1;
    align-items: stretch;
}

.fsd-cards-scroll-area::-webkit-scrollbar {
    display: none;
}

.fsd-fare-card {
    flex: 0 0 240px;
    scroll-snap-align: center;
    border: 1px solid #E0E0E0;
    border-radius: 12px;
    overflow: hidden;
    background: #fff;
    transition: all 0.2s ease;
    cursor: pointer;
    position: relative;
    padding-bottom: 20px;
    display: flex;
    flex-direction: column;
}

.fsd-fare-card.selected {
    border: 2px solid var(--indigo-blue);
    box-shadow: 0 8px 24px rgba(0, 95, 169, 0.15);
}

.fsd-fare-card.selected.stretch-card {
    border: 2px solid #D4AF37;
    box-shadow: 0 8px 24px rgba(212, 175, 55, 0.15);
}

.fsd-fare-header {
    text-align: center;
    padding: 16px 0;
    font-size: 16px;
    font-weight: 700;
    color: #666;
    border-bottom: 1px solid #E0E0E0;
}

.fsd-fare-card.selected .fsd-fare-header {
    color: var(--indigo-blue);
}

.fsd-fare-card.selected.stretch-card .fsd-fare-header {
    color: #D4AF37;
}

.fsd-popular-badge {
    background: #00C3F8;
    color: #fff;
    text-align: center;
    font-size: 11px;
    font-weight: 700;
    padding: 6px 0;
    text-transform: uppercase;
}

.fsd-popular-badge.stretch-badge {
    background: #FDF7E7;
    color: #D4AF37;
}

.fsd-fare-features {
    padding: 16px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
}

.fsd-feature-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 12px;
    font-size: 12px;
    color: #333;
    line-height: 1.4;
}

.fsd-feature-item.highlighted strong {
    color: #000;
}

.fsd-feature-item svg {
    flex-shrink: 0;
    margin-top: 1px;
    color: #4CAF50;
}

.fsd-feature-item.cross {
    color: #999;
}

.fsd-feature-item.cross svg {
    color: #999;
}

.fsd-pricing-block {
    text-align: center;
    margin-top: auto;
    padding-top: 16px;
}

.fsd-sticky-footer {
    position: sticky;
    bottom: 0;
    background: #fff;
    border-top: 1px solid #E0E0E0;
    padding: 16px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-shrink: 0;
    padding-bottom: calc(16px + env(safe-area-inset-bottom, 20px));
}
"""

if "fsd-segment-control" not in css:
    css += "\n" + new_css
    with open('style.css', 'w') as f:
        f.write(css)
    print("Added CSS.")
else:
    print("CSS already exists.")
