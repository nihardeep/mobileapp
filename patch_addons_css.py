with open('style.css', 'a') as f:
    f.write('''

/* ==========================================================================
   ADD-ONS SCREEN
   ========================================================================== */

.addon-sector-container {
    display: flex;
    gap: 12px;
    padding: 16px 24px;
    overflow-x: auto;
    -ms-overflow-style: none;
    scrollbar-width: none;
}
.addon-sector-container::-webkit-scrollbar { display: none; }

.addon-sector-pill {
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 8px;
}
.addon-sector-pill.active {
    background: var(--indigo-blue);
    color: white;
}
.addon-sector-pill.inactive {
    background: #ffffff;
    color: #64748b;
    border: 1px solid #cbd5e1;
}

.addon-pax-section {
    padding: 0 24px 16px;
}
.addon-pax-title {
    font-size: 12px;
    font-weight: 700;
    color: #64748b;
    margin-bottom: 8px;
}
.addon-pax-chips {
    display: flex;
    gap: 12px;
    overflow-x: auto;
    -ms-overflow-style: none;
    scrollbar-width: none;
    padding-bottom: 4px;
}
.addon-pax-chips::-webkit-scrollbar { display: none; }

.addon-pax-chip {
    flex: 0 0 auto;
    padding: 10px 16px;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 120px;
    cursor: pointer;
    transition: all 0.2s ease;
}
.addon-pax-chip.active {
    border-color: var(--indigo-blue);
    background: #f0f9ff;
    box-shadow: 0 4px 12px rgba(0, 27, 148, 0.05);
}
.addon-pax-chip .pax-name {
    font-size: 13px;
    font-weight: 800;
    color: #1e293b;
    display: flex;
    align-items: center;
    gap: 4px;
}
.addon-pax-chip.active .pax-name {
    color: var(--indigo-blue);
}
.addon-pax-chip .pax-type {
    font-size: 10px;
    font-weight: 600;
    color: #64748b;
}

.addon-category-tabs {
    display: flex;
    gap: 24px;
    padding: 0 24px;
    border-bottom: 1px solid #cbd5e1;
    overflow-x: auto;
    -ms-overflow-style: none;
    scrollbar-width: none;
}
.addon-category-tabs::-webkit-scrollbar { display: none; }

.addon-tab {
    padding: 12px 0;
    font-size: 12px;
    font-weight: 700;
    color: #64748b;
    position: relative;
    white-space: nowrap;
    cursor: pointer;
}
.addon-tab.active {
    color: var(--indigo-blue);
}
.addon-tab.active::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    right: 0;
    height: 2px;
    background: var(--indigo-blue);
}

.addon-bundles-section {
    padding: 20px 0;
}
.addon-section-title {
    font-size: 12px;
    font-weight: 700;
    color: #64748b;
    padding: 0 24px 12px;
}
.addon-bundles-scroll {
    display: flex;
    gap: 16px;
    padding: 0 24px;
    overflow-x: auto;
    -ms-overflow-style: none;
    scrollbar-width: none;
    scroll-snap-type: x mandatory;
}
.addon-bundles-scroll::-webkit-scrollbar { display: none; }

.addon-bundle-card {
    flex: 0 0 85%;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px;
    position: relative;
    scroll-snap-align: center;
}
.addon-bundle-card.added {
    border-color: #22c55e;
    background: #f0fdf4;
}

.bundle-discount-badge {
    position: absolute;
    top: 0;
    right: 0;
    background: #22c55e;
    color: white;
    font-size: 10px;
    font-weight: 800;
    padding: 4px 8px;
    border-radius: 0 12px 0 8px;
}
.bundle-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}
.bundle-title {
    font-size: 16px;
    font-weight: 800;
    color: #1e293b;
}
.addon-bundle-card.added .bundle-title::after {
    content: 'Added';
    background: #22c55e;
    color: white;
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 4px;
    margin-left: 8px;
    vertical-align: middle;
}

.bundle-features ul {
    margin: 0;
    padding-left: 16px;
    font-size: 11px;
    color: #475569;
    line-height: 1.6;
}
.bundle-images {
    display: flex;
    gap: 8px;
    margin-top: 12px;
    margin-bottom: 16px;
}
.bundle-images img {
    width: calc(33% - 5px);
    height: 60px;
    object-fit: cover;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
}
.bundle-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 12px;
    border-top: 1px solid #f1f5f9;
}
.bundle-price .old-price {
    font-size: 12px;
    color: #94a3b8;
    text-decoration: line-through;
    margin-right: 4px;
}
.bundle-price .new-price {
    font-size: 16px;
    font-weight: 800;
    color: #0f172a;
}
.bundle-add-btn {
    background: #ffffff;
    border: 1px solid var(--indigo-blue);
    color: var(--indigo-blue);
    font-size: 12px;
    font-weight: 800;
    padding: 6px 20px;
    border-radius: 6px;
    cursor: pointer;
}
.addon-bundle-card.added .bundle-add-btn, .addon-meal-card.added .bundle-add-btn {
    background: #fee2e2;
    border-color: #ef4444;
    color: #ef4444;
}

/* Meal Cards */
.addon-meal-card {
    flex: 0 0 45%;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    position: relative;
    scroll-snap-align: center;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}
.addon-meal-card.added {
    border-color: #22c55e;
    background: #f0fdf4;
}
.meal-discount-badge {
    position: absolute;
    top: 0;
    right: 0;
    background: var(--sky-blue);
    color: white;
    font-size: 8px;
    font-weight: 800;
    padding: 4px 8px;
    border-radius: 0 12px 0 8px;
    z-index: 2;
}
.meal-tag {
    position: absolute;
    top: 8px;
    left: 8px;
    background: white;
    border: 1px solid #e2e8f0;
    padding: 2px 4px;
    border-radius: 4px;
    font-size: 8px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 4px;
    z-index: 2;
}
.veg-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #22c55e;
}
.meal-image {
    width: 100%;
    height: 120px;
    position: relative;
}
.meal-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.meal-details {
    padding: 12px;
    flex: 1;
    display: flex;
    flex-direction: column;
}
.meal-title {
    font-size: 11px;
    font-weight: 700;
    color: #1e293b;
    line-height: 1.4;
    flex: 1;
}
.meal-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
}
.meal-price .old-price {
    display: block;
    font-size: 10px;
    color: #94a3b8;
    text-decoration: line-through;
}
.meal-price .new-price {
    font-size: 14px;
    font-weight: 800;
    color: #0f172a;
}
.meal-nutrition {
    font-size: 10px;
    font-weight: 600;
    color: var(--indigo-blue);
    margin-top: 12px;
    border-top: 1px solid #f1f5f9;
    padding-top: 8px;
}

''')
