import re

with open('style.css', 'r') as f:
    css = f.read()

# Fix compare modal z-index so it sits on top of the fare popup
css = css.replace('z-index: 2000;', 'z-index: 3000;')

with open('style.css', 'w') as f:
    f.write(css)

with open('app.js', 'r') as f:
    js = f.read()

# 1. Remove closeFarePopup from openCompareFaresModal
js = js.replace('closeFarePopup();\n    \n    const modal', 'const modal')

# 2. Add mouse drag scrolling logic for desktop users
drag_logic = """
// Add mouse drag scrolling to the carousel for desktop testing
document.addEventListener('DOMContentLoaded', () => {
    // We need a mutation observer or delegated events because the carousel content might be injected,
    // but the container #cp-carousel itself is static in index.html!
    const slider = document.getElementById('cp-carousel');
    if (!slider) return;

    let isDown = false;
    let startX;
    let scrollLeft;

    slider.addEventListener('mousedown', (e) => {
        isDown = true;
        startX = e.pageX - slider.offsetLeft;
        scrollLeft = slider.scrollLeft;
        // Pause scroll-snap while dragging for smoother feel
        slider.style.scrollSnapType = 'none';
    });
    slider.addEventListener('mouseleave', () => {
        isDown = false;
        slider.style.scrollSnapType = 'x mandatory';
        handleCarouselScroll();
    });
    slider.addEventListener('mouseup', () => {
        isDown = false;
        slider.style.scrollSnapType = 'x mandatory';
        handleCarouselScroll();
    });
    slider.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - slider.offsetLeft;
        const walk = (x - startX) * 1.5; 
        slider.scrollLeft = scrollLeft - walk;
    });
});
"""

if 'slider.addEventListener(\'mousedown\'' not in js:
    js += '\n' + drag_logic

with open('app.js', 'w') as f:
    f.write(js)

print("Fixed scrolling and compare modal stacking")
