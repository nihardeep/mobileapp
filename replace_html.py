import re

with open('index.html', 'r') as f:
    html = f.read()

new_html = """                            <!-- Trending Destinations Insta Stories -->
                            <div class="insta-stories-section" id="trendingDestinationsSection">
                                <div class="promo-section-header">
                                    <div class="section-title">Trending Destinations</div>
                                </div>
                                <div class="insta-stories-scroll">
                                    <!-- Card 1 -->
                                    <div class="insta-story-card" onclick="selectDestination('DXB', 'Dubai')" style="background-image: url('https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=600&h=400&fit=crop')">
                                        <div class="insta-play-ring"><svg viewBox="0 0 24 24" width="10" height="10" fill="white"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg></div>
                                        <div class="insta-story-overlay">
                                            <div class="insta-story-city">Dubai</div>
                                            <div class="insta-story-price">From ₹20,199</div>
                                        </div>
                                    </div>
                                    <!-- Card 2 -->
                                    <div class="insta-story-card" onclick="selectDestination('BKK', 'Bangkok')" style="background-image: url('https://images.unsplash.com/photo-1508009603885-247a505979c3?w=600&h=400&fit=crop')">
                                        <div class="insta-play-ring"><svg viewBox="0 0 24 24" width="10" height="10" fill="white"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg></div>
                                        <div class="insta-story-overlay">
                                            <div class="insta-story-city">Bangkok</div>
                                            <div class="insta-story-price">From ₹20,199</div>
                                        </div>
                                    </div>
                                    <!-- Card 3 -->
                                    <div class="insta-story-card" onclick="selectDestination('DPS', 'Bali')" style="background-image: url('https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&h=400&fit=crop')">
                                        <div class="insta-play-ring"><svg viewBox="0 0 24 24" width="10" height="10" fill="white"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg></div>
                                        <div class="insta-story-overlay">
                                            <div class="insta-story-city">Bali</div>
                                            <div class="insta-story-price">From ₹25,400</div>
                                        </div>
                                    </div>
                                    <!-- Card 4 -->
                                    <div class="insta-story-card" onclick="selectDestination('BLR', 'Bengaluru')" style="background-image: url('blr_flower_market.png')">
                                        <div class="insta-play-ring"><svg viewBox="0 0 24 24" width="10" height="10" fill="white"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg></div>
                                        <div class="insta-story-overlay">
                                            <div class="insta-story-city">Bengaluru</div>
                                            <div class="insta-story-price">From ₹5,400</div>
                                        </div>
                                    </div>
                                    <!-- Card 5 -->
                                    <div class="insta-story-card" onclick="selectDestination('SIN', 'Singapore')" style="background-image: url('https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=600&h=400&fit=crop')">
                                        <div class="insta-play-ring"><svg viewBox="0 0 24 24" width="10" height="10" fill="white"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg></div>
                                        <div class="insta-story-overlay">
                                            <div class="insta-story-city">Singapore</div>
                                            <div class="insta-story-price">From ₹18,900</div>
                                        </div>
                                    </div>
                                </div>
                                <div class="explore-all-text" onclick="alert('Exploring all destinations!')">Explore all destinations</div>
                            </div>"""

start_idx = html.find('<!-- Trending Destinations Carousel -->')
end_idx = html.find('<!-- Travel on Tap -->')

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_html + "\n\n                            " + html[end_idx:]
    with open('index.html', 'w') as f:
        f.write(html)
    print("HTML updated")
else:
    print("Tags not found")
