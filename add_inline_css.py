import re

with open('style.css', 'r') as f:
    css = f.read()

new_css = """
/* Inline Fare Selection Styles */
.inline-fare-container {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), padding 0.4s ease;
    background: #FAFAFA;
    border-radius: 0 0 16px 16px;
    margin-top: 0;
}

.inline-fare-container.expanded {
    max-height: 600px;
    padding: 16px 0;
    border-top: 1px solid rgba(0,0,0,0.05);
}

.inline-carousel {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    gap: 12px;
    padding: 0 16px;
}

.inline-carousel::-webkit-scrollbar {
    display: none;
}

.inline-fare-card {
    flex: 0 0 220px;
    scroll-snap-align: center;
    background: #fff;
    border: 1px solid #E0E0E0;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.inline-fare-card.stretch-card {
    border-color: rgba(212, 175, 55, 0.3);
}

.inline-fare-header {
    padding: 12px;
    text-align: center;
    font-size: 14px;
    font-weight: 700;
    color: #333;
    border-bottom: 1px solid #E0E0E0;
}

.inline-popular-badge {
    background: #00C3F8;
    color: #fff;
    font-size: 10px;
    font-weight: 700;
    text-align: center;
    padding: 4px 0;
    text-transform: uppercase;
}

.inline-fare-features {
    padding: 12px;
    flex-grow: 1;
}

.inline-feature-item {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    margin-bottom: 8px;
    font-size: 11px;
    color: #333;
}

.inline-feature-item svg {
    flex-shrink: 0;
    color: #4CAF50;
    margin-top: 1px;
}

.inline-feature-item.cross {
    color: #999;
}

.inline-feature-item.cross svg {
    color: #999;
}

.inline-fare-footer {
    padding: 12px;
    text-align: center;
    border-top: 1px solid rgba(0,0,0,0.05);
    background: #F9F9F9;
}

.inline-select-btn {
    background: var(--indigo-blue);
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 10px 16px;
    font-size: 13px;
    font-weight: 700;
    width: 100%;
    margin-top: 8px;
    cursor: pointer;
}

.inline-compare-btn {
    display: block;
    text-align: center;
    color: var(--indigo-blue);
    font-size: 13px;
    font-weight: 700;
    margin-top: 16px;
    padding: 8px;
    cursor: pointer;
}

/* Compare Modal */
.compare-modal-overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.5);
    z-index: 2000;
    display: flex;
    align-items: flex-end;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
}

.compare-modal-overlay.active {
    opacity: 1;
    pointer-events: auto;
}

.compare-modal-content {
    background: #fff;
    width: 100%;
    border-radius: 20px 20px 0 0;
    padding: 24px;
    transform: translateY(100%);
    transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    max-height: 85vh;
    overflow-y: auto;
}

.compare-modal-overlay.active .compare-modal-content {
    transform: translateY(0);
}

.compare-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 16px;
    font-size: 12px;
}

.compare-table th, .compare-table td {
    border: 1px solid #E0E0E0;
    padding: 10px 8px;
    text-align: center;
}

.compare-table th {
    background: #F5F5F5;
    font-weight: 700;
    color: #333;
}

.compare-table td.feature-name {
    text-align: left;
    font-weight: 700;
    color: #555;
    background: #FAFAFA;
}

.compare-highlight {
    background: rgba(76, 175, 80, 0.1) !important;
    color: #2E7D32;
    font-weight: 700;
}
"""

if ".inline-fare-container" not in css:
    css += "\n" + new_css
    with open('style.css', 'w') as f:
        f.write(css)
    print("Added inline fare CSS.")
else:
    print("CSS already exists.")
