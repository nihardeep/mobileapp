with open('index.html', 'r') as f:
    html = f.read()

html = html.replace('id="partnersCarouselTrack"', 'class="partnersCarouselTrack"')
html = html.replace('#partnersCarouselTrack', '.partnersCarouselTrack')

with open('index.html', 'w') as f:
    f.write(html)

with open('app.js', 'r') as f:
    js = f.read()

target_js = """function initPartnersCarousel() {
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
}"""

replacement_js = """function initPartnersCarousel() {
    const tracks = document.querySelectorAll('.partnersCarouselTrack');
    if (!tracks || tracks.length === 0) return;
    
    tracks.forEach(track => {
        setInterval(() => {
            const maxScroll = track.scrollWidth - track.clientWidth;
            
            if (track.scrollLeft >= maxScroll - 10) {
                track.style.scrollBehavior = 'auto';
                track.scrollLeft = 0;
                void track.offsetHeight;
                track.style.scrollBehavior = 'smooth';
            }
            
            const cards = track.querySelectorAll('.partner-box');
            let nextScroll = 0;
            
            for (let card of cards) {
                let cardLeft = card.offsetLeft;
                if (cardLeft > track.scrollLeft + 5) {
                    nextScroll = cardLeft;
                    break;
                }
            }
            
            if (nextScroll > 0) {
                track.scrollTo({ left: nextScroll, behavior: 'smooth' });
            }
        }, 3000);
    });
}"""

js = js.replace(target_js, replacement_js)

with open('app.js', 'w') as f:
    f.write(js)
