with open('app.js', 'r') as f:
    js = f.read()

observer_code = """
// ==========================================================================
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
});
"""

if "VIDEO SCROLL OBSERVER" not in js:
    with open('app.js', 'a') as f:
        f.write("\n" + observer_code)
    print("Observer added")
else:
    print("Observer already exists")
