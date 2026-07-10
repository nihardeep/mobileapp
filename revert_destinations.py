import re

with open('index.html', 'r') as f:
    html = f.read()

# First, undo the Bangkok custom play button
# The current Bangkok looks like:
# <div class="insta-story-card carousel-slide" onclick="selectDestination('BKK', 'Bangkok')">
#                                         <video id="bkk-video" src="..." style="..."></video>
#                                         <div class="insta-play-ring" id="bkk-play-btn" onclick="toggleBkkVideo(event)"><svg ...></div>

# Let's just find all <div class="insta-story-card carousel-slide" onclick="selectDestination('...', 'City')">
# and replace whatever is between it and <div class="insta-story-overlay"> with the correct video code.

posters = {
    "Dubai": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=600&h=400&fit=crop",
    "Bangkok": "https://images.unsplash.com/photo-1508009603885-247a505979c3?w=600&h=400&fit=crop",
    "Bali": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&h=400&fit=crop",
    "Bengaluru": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?w=600&h=400&fit=crop",
    "Singapore": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=600&h=400&fit=crop"
}

def replace_card(match):
    city = match.group(1)
    poster = posters.get(city, "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=600&h=400&fit=crop")
    
    video_html = f'<video src="https://assets.mixkit.co/videos/preview/mixkit-aerial-view-of-city-traffic-at-night-11-large.mp4" class="insta-card-video" loop muted playsinline poster="{poster}"></video>'
    play_ring = '<div class="insta-play-ring"><svg viewBox="0 0 24 24" width="10" height="10" fill="white"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg></div>'
    
    return f'<div class="insta-story-card carousel-slide" onclick="selectDestination(this, \'{city}\')">\n                                        {video_html}\n                                        {play_ring}\n                                        <div class="insta-story-overlay">'

# Wait, the onclick is `onclick="selectDestination('BKK', 'Bangkok')"`
# Let's match the exact onclick string and the overlay.
pattern = r'<div class="insta-story-card carousel-slide" onclick="selectDestination\(\'[^\']*\', \'([^\']*)\'\)">.*?<div class="insta-story-overlay">'

def replace_regex(match):
    city = match.group(1)
    poster = posters.get(city, "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=600&h=400&fit=crop")
    full_match = match.group(0)
    # The prefix is everything up to the closing > of the first div
    prefix_end = full_match.find('>') + 1
    prefix = full_match[:prefix_end]
    
    video_html = f'<video src="https://assets.mixkit.co/videos/preview/mixkit-aerial-view-of-city-traffic-at-night-11-large.mp4" class="insta-card-video" loop muted playsinline poster="{poster}"></video>'
    play_ring = '<div class="insta-play-ring"><svg viewBox="0 0 24 24" width="10" height="10" fill="white"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg></div>'
    
    return f'{prefix}\n                                        {video_html}\n                                        {play_ring}\n                                        <div class="insta-story-overlay">'

new_html = re.sub(pattern, replace_regex, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(new_html)

# Revert app.js
with open('app.js', 'r') as f:
    js = f.read()

# Replace toggleBkkVideo back with IntersectionObserver
toggle_target = """// ==========================================================================
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
};"""

obs_logic = """// ==========================================================================
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

js = js.replace(toggle_target, obs_logic)

with open('app.js', 'w') as f:
    f.write(js)

