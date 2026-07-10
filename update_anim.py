import re

with open('style.css', 'r') as f:
    css = f.read()

# 1. Clean up dangling keyframes junk from previous run
css = re.sub(r'\s*10%, 40% \{ opacity: 1; transform: translateY\(0\); \}\s*45%, 100% \{ opacity: 0; transform: translateY\(-8px\); \}\s*\}', '', css)

# 2. Make text bigger
css = css.replace('font-size: 11px;\n    color: #b5c7ec;', 'font-size: 13px;\n    color: #ffffff;\n    font-weight: 500;')

# 3. Update the animations for the 4 frames
old_animations = """
.z-frame-1 { animation: zeroFlash4 12s infinite 0s; }
.z-frame-2 { animation: zeroFlash4 12s infinite 3s; }
.z-frame-3 { animation: zeroFlash4 12s infinite 6s; }
.z-frame-4 { animation: zeroFlash4 12s infinite 9s; }

@keyframes zeroFlash4 {
    0%, 3% { opacity: 0; transform: translateY(10px); }
    8%, 20% { opacity: 1; transform: translateY(0); }
    25%, 100% { opacity: 0; transform: translateY(-10px); }
}
"""

new_animations = """
.z-frame-1 { animation: zeroFlashSlide 12s infinite 0s; }
.z-frame-2 { animation: zeroFlashFlip 12s infinite 3s; }
.z-frame-3 { animation: zeroFlashZoom 12s infinite 6s; }
.z-frame-4 { animation: zeroFlashBounce 12s infinite 9s; }

@keyframes zeroFlashSlide {
    0%, 3% { opacity: 0; transform: translateX(-15px); }
    8%, 20% { opacity: 1; transform: translateX(0); }
    25%, 100% { opacity: 0; transform: translateX(15px); }
}

@keyframes zeroFlashFlip {
    0%, 3% { opacity: 0; transform: rotateX(90deg); }
    8%, 20% { opacity: 1; transform: rotateX(0deg); }
    25%, 100% { opacity: 0; transform: rotateX(-90deg); }
}

@keyframes zeroFlashZoom {
    0%, 3% { opacity: 0; transform: scale(0.85); }
    8%, 20% { opacity: 1; transform: scale(1); }
    25%, 100% { opacity: 0; transform: scale(1.15); }
}

@keyframes zeroFlashBounce {
    0%, 3% { opacity: 0; transform: translateY(-15px); }
    7% { opacity: 1; transform: translateY(0); }
    11% { transform: translateY(-4px); }
    15% { transform: translateY(0); }
    20% { opacity: 1; transform: translateY(0); }
    25%, 100% { opacity: 0; transform: translateY(15px); }
}
"""

css = css.replace(old_animations, new_animations)

# Also remove animation: zeroFlash 6s infinite; from .zero-flash-frame if it exists
css = css.replace('animation: zeroFlash 6s infinite;', '')

with open('style.css', 'w') as f:
    f.write(css)

print("Updated animations and font size!")
