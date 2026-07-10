import re

with open('index.html', 'r') as f:
    html = f.read()

# Pattern to find all insta-story-card elements
pattern = r'(<div class="insta-story-card carousel-slide"[^>]*>)\s*<video[^>]*></video>\s*<div class="insta-play-ring">.*?</div>'

# We want to keep the video ONLY for Bangkok.
# Bangkok card has: onclick="selectDestination('BKK', 'Bangkok')"
def replace_card(match):
    prefix = match.group(1)
    if "'BKK', 'Bangkok'" in prefix:
        # It's Bangkok, modify the play ring to have onclick
        video_html = '<video id="bkk-video" src="https://assets.mixkit.co/videos/preview/mixkit-aerial-view-of-city-traffic-at-night-11-large.mp4" class="insta-card-video" loop muted playsinline poster="https://images.unsplash.com/photo-1508009603885-247a505979c3?w=600&h=400&fit=crop" style="width: 100%; height: 100%; object-fit: cover; border-radius: 16px;"></video>'
        play_ring = '<div class="insta-play-ring" id="bkk-play-btn" onclick="toggleBkkVideo(event)"><svg viewBox="0 0 24 24" width="10" height="10" fill="white"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg></div>'
        return f'{prefix}\n                                        {video_html}\n                                        {play_ring}'
    else:
        # Not Bangkok, just remove video and play ring
        return prefix

new_html = re.sub(pattern, replace_card, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(new_html)

# Now remove IntersectionObserver from app.js and add toggleBkkVideo
with open('app.js', 'r') as f:
    js = f.read()

# Remove observer
obs_target = """// ==========================================================================
// VIDEO SCROLL OBSERVER
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
    const videos = document.querySelectorAll('.insta-card-video');
    
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const video = entry.target;
                if (entry.isIntersecting) {
                    video.play().catch(e => console.log('Autoplay prevented', e));
                } else {
                    video.pause();
                }
            });
        }, { threshold: 0.5 }); // Play when at least 50% visible
        
        videos.forEach(video => {
            observer.observe(video);
        });
    }
});"""

js = js.replace(obs_target, """// ==========================================================================
// VIDEO PLAYBACK LOGIC
// ==========================================================================
window.toggleBkkVideo = function(e) {
    e.stopPropagation();
    const video = document.getElementById('bkk-video');
    const btn = document.getElementById('bkk-play-btn');
    if (!video) return;
    
    if (video.paused) {
        video.play();
        btn.innerHTML = '<svg viewBox="0 0 24 24" width="10" height="10" fill="white"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>'; // Pause icon
    } else {
        video.pause();
        btn.innerHTML = '<svg viewBox="0 0 24 24" width="10" height="10" fill="white"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>'; // Play icon
    }
};""")

with open('app.js', 'w') as f:
    f.write(js)

