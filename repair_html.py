with open('index.html', 'r') as f:
    html = f.read()

missing_chunk = """                            <!-- Offers Carousel (Not business as usual slides) -->
                            <div class="offers-carousel-section" id="featureBannerSection">
                                <div class="offers-header-row" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; margin-top: 4px; padding: 0 4px;">
                                    <span class="section-title">Exclusive Offers</span>
                                </div>
                                <div class="carousel-container" id="offersCarouselContainer">
                                    <div class="carousel-3d-track" id="offersCarousel">
                                        <!-- Slide 1: Weekend Exclusives -->
                                        <div class="carousel-slide offers-slide-1" onclick="triggerHaptic('medium', 'Book Weekend Exclusives'); alert('Redirecting to Weekend Exclusives flight search...')">
                                            <div class="offer-overlay">
                                                <div class="offer-title">Weekend Exclusives</div>
                                                <div class="offer-subtitle">Book your perfect getaway now</div>
                                            </div>
                                        </div>
"""

broken_spot = """                                        </div>
                                    </div>
                                </div>
                            </div>

                            
                                        <!-- Slide 2: Save ₹400 per person -->"""

if broken_spot in html:
    fixed_spot = """                                        </div>
                                    </div>
                                </div>
                            </div>

""" + missing_chunk + """                                        <!-- Slide 2: Save ₹400 per person -->"""
    html = html.replace(broken_spot, fixed_spot)
    with open('index.html', 'w') as f:
        f.write(html)
    print("Repaired Offers Carousel")
else:
    print("Could not find broken spot")
