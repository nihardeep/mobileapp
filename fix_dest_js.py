import re

with open('app.js', 'r') as f:
    js = f.read()

# Replace selectDestination(code, city) with the new logic
new_func = """function selectDestination(code, city) {
    triggerHaptic('medium', 'Destination Selected');
    
    // Set text fields in the new AI Destination screen
    document.getElementById('aiDestCityName').innerText = city;
    document.getElementById('aiDestTitleCity').innerText = city;
    
    // Optionally map the image
    const heroImg = document.getElementById('aiDestHeroImg');
    if (code === 'BLR' || city === 'Bangalore' || city === 'Bengaluru') {
        heroImg.style.backgroundImage = "url('blr_flower_market.png')";
        document.getElementById('aiDestTitleCountry').innerText = 'India';
        document.getElementById('aiDestDescription').innerText = 'Bengaluru, often referred to as the "Silicon Valley of India," is a bustling metropolis known for its thriving IT industry and cosmopolitan vibe. The city is a blend of modernity and tradition, with verdant parks like Cubbon Park offering tranquil retreats amidst urban sprawl.';
        document.getElementById('aiRouteText').innerText = 'SIN ⇄ BLR • 1 ADULT';
    } else if (code === 'DXB') {
        heroImg.style.backgroundImage = "url('https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=600&h=400&fit=crop')";
        document.getElementById('aiDestTitleCountry').innerText = 'UAE';
        document.getElementById('aiDestDescription').innerText = 'Dubai is a city of superlatives, home to the world’s tallest building, the Burj Khalifa, and sprawling futuristic architecture. Experience luxury shopping, ultra-modern attractions, and a vibrant nightlife in this desert oasis.';
        document.getElementById('aiRouteText').innerText = 'DEL ⇄ DXB • 1 ADULT';
    } else if (code === 'BKK') {
        heroImg.style.backgroundImage = "url('https://images.unsplash.com/photo-1508009603885-247a505979c3?w=600&h=400&fit=crop')";
        document.getElementById('aiDestTitleCountry').innerText = 'Thailand';
        document.getElementById('aiDestDescription').innerText = 'Bangkok is a sensory overload of vibrant street life, ornate shrines, and bustling floating markets. A paradise for food lovers and culture seekers, blending ancient traditions with a rapid modern pulse.';
        document.getElementById('aiRouteText').innerText = 'DEL ⇄ BKK • 1 ADULT';
    } else if (code === 'DPS') {
        heroImg.style.backgroundImage = "url('https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&h=400&fit=crop')";
        document.getElementById('aiDestTitleCountry').innerText = 'Indonesia';
        document.getElementById('aiDestDescription').innerText = 'Bali is an Indonesian island known for its forested volcanic mountains, iconic rice paddies, beaches and coral reefs. The island is home to religious sites such as cliffside Uluwatu Temple.';
        document.getElementById('aiRouteText').innerText = 'BOM ⇄ DPS • 1 ADULT';
    }
    
    // Clear old cards and generate 10 new flight cards
    const flightList = document.getElementById('aiFlightList');
    flightList.innerHTML = '';
    
    // Generate dates based on today + some offset
    const today = new Date();
    
    for (let i = 0; i < 10; i++) {
        // Date math
        const startDate = new Date(today);
        startDate.setDate(today.getDate() + 10 + (i * 7)); // start 10 days out, increment by 1 week
        const endDate = new Date(startDate);
        endDate.setDate(startDate.getDate() + 4); // 4 day trip
        
        const formatOptions = { weekday: 'short', day: 'numeric', month: 'short' };
        const startStr = startDate.toLocaleDateString('en-GB', formatOptions);
        const endStr = endDate.toLocaleDateString('en-GB', formatOptions);
        
        // Price math
        const basePrice = 300 + (Math.random() * 200);
        const priceStr = basePrice.toFixed(1);
        
        const cardHtml = `
            <div class="ai-flight-card" id="ai-card-${i}">
                <div class="ai-flight-left">
                    <span class="ai-flight-dates">${startStr} - ${endStr}</span>
                    <span class="ai-flight-class">ECONOMY</span>
                </div>
                <div class="ai-flight-right">
                    <div class="ai-flight-price-box">
                        <div class="ai-flight-price-lbl">From SGD</div>
                        <div class="ai-flight-price-val">${priceStr}</div>
                    </div>
                    <div class="ai-flight-arrow">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    </div>
                </div>
            </div>
        `;
        flightList.insertAdjacentHTML('beforeend', cardHtml);
    }
    
    // Navigate to the AI Destination Screen
    navigateTo('DestinationAI');
    
    // Trigger staggered animation after a short delay so screen transition occurs first
    setTimeout(() => {
        animateFlightCardsUp();
    }, 200);
}

function animateFlightCardsUp() {
    const cards = document.querySelectorAll('.ai-flight-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('animate-in');
            if (index % 3 === 0) triggerHaptic('light', 'Card Load');
        }, index * 80); // 80ms stagger
    });
}

function closeDestinationAI() {
    triggerHaptic('light', 'Close AI Destination');
    // Remove animate class so they can be re-animated next time
    const cards = document.querySelectorAll('.ai-flight-card');
    cards.forEach(card => card.classList.remove('animate-in'));
    navigateTo('home');
}
"""

js = re.sub(r'function selectDestination\(code, city\) \{.*?(?=\nfunction |\Z)', new_func + '\n', js, flags=re.DOTALL)

with open('app.js', 'w') as f:
    f.write(js)
