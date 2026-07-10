import re

with open('app.js', 'r') as f:
    js = f.read()

# Replace the backgroundImage setting with both backgroundImage (as fallback) and video src
new_logic = """    const heroImg = document.getElementById('aiDestHeroImg');
    const heroVideo = document.getElementById('aiDestHeroVideo');
    const genericVideoUrl = "https://assets.mixkit.co/videos/preview/mixkit-aerial-view-of-city-traffic-at-night-11-large.mp4";
    
    // We can pause video if it's currently playing
    if (heroVideo) {
        heroVideo.pause();
    }

    if (code === 'BLR' || city === 'Bangalore' || city === 'Bengaluru') {
        heroImg.style.backgroundImage = "url('blr_flower_market.png')";
        if(heroVideo) { heroVideo.poster = 'blr_flower_market.png'; }
        document.getElementById('aiDestTitleCountry').innerText = 'India';
        document.getElementById('aiDestDescription').innerText = 'Bengaluru, often referred to as the "Silicon Valley of India," is a bustling metropolis known for its thriving IT industry and cosmopolitan vibe. The city is a blend of modernity and tradition, with verdant parks like Cubbon Park offering tranquil retreats amidst urban sprawl.';
        document.getElementById('aiRouteText').innerText = 'SIN ⇄ BLR • 1 ADULT';
    } else if (code === 'DXB') {
        heroImg.style.backgroundImage = "url('https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=600&h=400&fit=crop')";
        if(heroVideo) { heroVideo.poster = 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=600&h=400&fit=crop'; }
        document.getElementById('aiDestTitleCountry').innerText = 'UAE';
        document.getElementById('aiDestDescription').innerText = 'Dubai is a city of superlatives, home to the world’s tallest building, the Burj Khalifa, and sprawling futuristic architecture. Experience luxury shopping, ultra-modern attractions, and a vibrant nightlife in this desert oasis.';
        document.getElementById('aiRouteText').innerText = 'DEL ⇄ DXB • 1 ADULT';
    } else if (code === 'BKK') {
        heroImg.style.backgroundImage = "url('https://images.unsplash.com/photo-1508009603885-247a505979c3?w=600&h=400&fit=crop')";
        if(heroVideo) { heroVideo.poster = 'https://images.unsplash.com/photo-1508009603885-247a505979c3?w=600&h=400&fit=crop'; }
        document.getElementById('aiDestTitleCountry').innerText = 'Thailand';
        document.getElementById('aiDestDescription').innerText = 'Bangkok is a sensory overload of vibrant street life, ornate shrines, and bustling floating markets. A paradise for food lovers and culture seekers, blending ancient traditions with a rapid modern pulse.';
        document.getElementById('aiRouteText').innerText = 'DEL ⇄ BKK • 1 ADULT';
    } else if (code === 'DPS') {
        heroImg.style.backgroundImage = "url('https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&h=400&fit=crop')";
        if(heroVideo) { heroVideo.poster = 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&h=400&fit=crop'; }
        document.getElementById('aiDestTitleCountry').innerText = 'Indonesia';
        document.getElementById('aiDestDescription').innerText = 'Bali is an Indonesian island known for its forested volcanic mountains, iconic rice paddies, beaches and coral reefs. The island is home to religious sites such as cliffside Uluwatu Temple.';
        document.getElementById('aiRouteText').innerText = 'BOM ⇄ DPS • 1 ADULT';
    } else {
        // Fallback for Singapore or others
        heroImg.style.backgroundImage = "url('https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=600&h=400&fit=crop')";
        if(heroVideo) { heroVideo.poster = 'https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=600&h=400&fit=crop'; }
        document.getElementById('aiDestTitleCountry').innerText = city;
        document.getElementById('aiDestDescription').innerText = 'Discover the beautiful sights, incredible culture, and amazing cuisine that awaits you.';
        document.getElementById('aiRouteText').innerText = `DEL ⇄ ${code} • 1 ADULT`;
    }
    
    // Play the video
    if (heroVideo) {
        heroVideo.src = genericVideoUrl;
        heroVideo.play().catch(e => console.log("Autoplay prevented:", e));
    }
"""

js = re.sub(r'const heroImg = document\.getElementById\(\'aiDestHeroImg\'\);.*?document\.getElementById\(\'aiRouteText\'\)\.innerText = \'BOM ⇄ DPS • 1 ADULT\';\n    \}', new_logic, js, flags=re.DOTALL)

with open('app.js', 'w') as f:
    f.write(js)
print("Updated JS logic for video play")
