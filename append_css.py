css_content = """
/* Addons Immersive Person Card */
.immersive-person-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    min-width: 200px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    box-shadow: 0 4px 6px rgba(0,0,0,0.02);
}

.immersive-person-card.active {
    border: 2px solid var(--indigo-blue);
    background: rgba(14, 165, 233, 0.03);
    box-shadow: 0 8px 16px rgba(14, 165, 233, 0.1);
    transform: translateY(-2px);
}

.person-avatar {
    width: 36px;
    height: 36px;
    border-radius: 12px;
    background: rgba(15, 23, 42, 0.05);
    color: #0f172a;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 800;
}

.immersive-person-card.active .person-avatar {
    background: var(--indigo-blue);
    color: #ffffff;
}

.person-details {
    display: flex;
    flex-direction: column;
}

.person-name {
    font-size: 14px;
    font-weight: 800;
    color: #0f172a;
    white-space: nowrap;
}

.person-cart-status {
    font-size: 11px;
    font-weight: 700;
    color: #64748b;
    margin-top: 2px;
}

.addon-badge {
    color: var(--indigo-blue);
}
"""
with open('style.css', 'a') as f:
    f.write(css_content)
