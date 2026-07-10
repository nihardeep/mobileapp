import re

with open('style.css', 'r') as f:
    css = f.read()

# First, remove the old premium dark styles
css = re.sub(r'/\* ==========================================================================\n   PREMIUM UPFRONT CARD \(Dark Theme\)\n   ========================================================================== \*/.*?/\*', '/*', css, flags=re.DOTALL)

subtle_css = """
/* ==========================================================================
   SUBTLE ANIMATED UPFRONT CARD
   ========================================================================== */
.upgrade-promo-card.subtle-glass {
    background: rgba(255, 255, 255, 0.4); /* highly transparent glass */
    border: 1px solid rgba(255, 255, 255, 0.8);
    border-radius: 12px;
    padding: 12px 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    position: relative;
    height: 48px; /* Fixed height for the animated frames */
    overflow: hidden;
    display: flex;
    align-items: center;
}

.animated-benefit-frame {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    padding: 0 16px;
    opacity: 0;
    transform: translateY(10px);
    animation: upgradeCycle 6s infinite;
}

/* Stagger the frames (2 seconds each) */
.animated-benefit-frame.frame-1 {
    animation-delay: 0s;
}

.animated-benefit-frame.frame-2 {
    animation-delay: 2s;
}

.animated-benefit-frame.frame-3 {
    animation-delay: 4s;
    justify-content: space-between; /* Space out title and button */
}

@keyframes upgradeCycle {
    0%, 5% {
        opacity: 0;
        transform: translateY(10px);
    }
    10%, 30% {
        opacity: 1;
        transform: translateY(0);
    }
    33%, 100% {
        opacity: 0;
        transform: translateY(-10px);
    }
}

.animated-benefit-frame span {
    font-size: 13px;
    font-weight: 600;
    color: var(--indigo-navy);
}

.subtle-promo-title {
    font-size: 13px;
    color: var(--text-primary);
}
.subtle-promo-title strong {
    color: var(--indigo-blue);
}

.subtle-action-btn {
    padding: 6px 12px;
    border-radius: 8px;
    background: var(--indigo-blue);
    color: white;
    font-size: 11px;
    font-weight: 700;
    border: none;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0, 95, 169, 0.3);
    transition: transform 0.15s ease;
}
"""

if "SUBTLE ANIMATED UPFRONT CARD" not in css:
    with open('style.css', 'a') as f:
        f.write("\n" + subtle_css)
    print("Added subtle CSS")
else:
    print("Already added")
