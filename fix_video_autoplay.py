with open('app.js', 'r') as f:
    js = f.read()

# Remove the old IntersectionObserver for videos since we're using the 3D coverflow now
import re
js = re.sub(r'// ==========================================================================\n// VIDEO SCROLL OBSERVER.*?\}\);\n\}\);\n', '', js, flags=re.DOTALL)

# Add logic inside init3DCurvedCoverflow to play the active card's video
# In init3DCurvedCoverflow, updateSlides(p) is where the cards are transformed.
# It also does `dots.forEach((dot, i) => dot.classList.toggle('active', i === Math.round(p)));`
# We can inject video play/pause there.
video_logic = """        // Update video playback for active slide
        const activeIdx = Math.round(p);
        slides.forEach((s, i) => {
            const vid = s.querySelector('video');
            if (vid) {
                if (i === activeIdx) {
                    vid.play().catch(e => console.log('Autoplay prevented', e));
                } else {
                    vid.pause();
                }
            }
        });
"""

# Find where updateSlides sets dots
dots_logic = "dots.forEach((dot, i) => dot.classList.toggle('active', i === Math.round(p)));"
if dots_logic in js:
    js = js.replace(dots_logic, dots_logic + "\n" + video_logic)

with open('app.js', 'w') as f:
    f.write(js)
print("Updated JS for video autoplay in coverflow")
