with open('index.html', 'r') as f:
    html = f.read()

target = """                                        <div class="partner-stock-ticker-wrapper" style="background: transparent; border: none; padding: 0; margin-top: 0; position: relative;">
                                            <!-- Masking gradients to fade out left/right edges -->
                                            <div style="position: absolute; top: 0; left: 0; width: 24px; height: 100%; background: linear-gradient(to right, #0a0f18 0%, transparent 100%); z-index: 2; pointer-events: none;"></div>
                                            <div style="position: absolute; top: 0; right: 0; width: 24px; height: 100%; background: linear-gradient(to left, #0a0f18 0%, transparent 100%); z-index: 2; pointer-events: none;"></div>
                                            
                                            <div class="partner-stock-ticker-track" style="gap: 8px;">"""

replacement = """                                        <div class="partner-carousel-wrapper" style="background: transparent; border: none; padding: 0; margin-top: 0; position: relative; width: 100%;">
                                            <!-- Masking gradients to fade out left/right edges -->
                                            <div style="position: absolute; top: 0; left: 0; width: 24px; height: 100%; background: linear-gradient(to right, #0a0f18 0%, transparent 100%); z-index: 2; pointer-events: none;"></div>
                                            <div style="position: absolute; top: 0; right: 0; width: 24px; height: 100%; background: linear-gradient(to left, #0a0f18 0%, transparent 100%); z-index: 2; pointer-events: none;"></div>
                                            
                                            <div id="partnersCarouselTrack" style="display: flex; gap: 8px; overflow-x: auto; scroll-snap-type: x mandatory; scroll-behavior: smooth; width: 100%; padding-bottom: 4px; padding-right: 24px;">
                                                <style>
                                                    #partnersCarouselTrack::-webkit-scrollbar { display: none; }
                                                    #partnersCarouselTrack .partner-box { scroll-snap-align: start; flex-shrink: 0; }
                                                </style>"""

html = html.replace(target, replacement)

# We also need to do it for STATE 2 (newUserCard) which we replaced recently?
# Ah, in my fix script, I might have replaced BOTH cards with the same HTML. Let's see if the replacement occurs twice.
count = html.count(replacement)
if count == 0:
    count_target = html.count(target)
    print(f"Target found {count_target} times")

with open('index.html', 'w') as f:
    f.write(html)

# Add JS logic
js_logic = """
// Partners Carousel Auto-Scroll Logic
function initPartnersCarousel() {
    const track = document.getElementById('partnersCarouselTrack');
    if (!track) return;
    
    setInterval(() => {
        const maxScroll = track.scrollWidth - track.clientWidth;
        
        // If reached the end of the original set, snap back to start
        if (track.scrollLeft >= maxScroll - 10) {
            track.style.scrollBehavior = 'auto';
            track.scrollLeft = 0;
            // Force reflow
            void track.offsetHeight;
            track.style.scrollBehavior = 'smooth';
        }
        
        // Find next snap point
        const cards = track.querySelectorAll('.partner-box');
        let nextScroll = 0;
        let trackRect = track.getBoundingClientRect();
        
        for (let card of cards) {
            let cardLeft = card.offsetLeft;
            // Add a small threshold (5px) to skip the currently visible first card
            if (cardLeft > track.scrollLeft + 5) {
                nextScroll = cardLeft;
                break;
            }
        }
        
        if (nextScroll > 0) {
            track.scrollTo({ left: nextScroll, behavior: 'smooth' });
        }
    }, 3000); // Scroll every 3 seconds
}

// Ensure it starts
document.addEventListener('DOMContentLoaded', () => {
    initPartnersCarousel();
});
"""

with open('app.js', 'a') as f:
    f.write(js_logic)

