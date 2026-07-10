with open('index.html', 'r') as f:
    html = f.read()

# We need to insert SCREEN 5 inside .app-content
# The easiest way is to find the closing div of app-content.
# But app-content has many nested divs. Let's find where app-content ends.
# Actually, we can just insert it right before the last closing div before <div class="bottom-nav">

bottom_nav_idx = html.find('<!-- Bottom Navigation Bar -->')

screen_html = """
                <!-- ==========================================================
                     SCREEN 5: AI DESTINATION RECOMMENDATIONS
                     ========================================================== -->
                <div class="screen" id="screenDestinationAI">
                    <div class="ai-dest-header">
                        <div class="ai-dest-title">Inspiring you to travel</div>
                        <div class="ai-dest-close" onclick="closeDestinationAI()">
                            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                        </div>
                    </div>
                    
                    <div class="ai-dest-search-context">
                        <span>Cheapest fare to <strong id="aiDestCityName">Bengaluru</strong></span>
                        <div class="ai-dest-edit-icon">
                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                        </div>
                    </div>
                    
                    <div class="ai-dest-content-scroll">
                        <div class="ai-recommendation-badge">
                            <svg viewBox="0 0 24 24" width="12" height="12" fill="#ffd15c"><path d="M12 2l2.4 7.6L22 12l-7.6 2.4L12 22l-2.4-7.6L2 12l7.6-2.4L12 2z"/></svg>
                            RECOMMENDATIONS FROM AI
                        </div>
                        
                        <div class="ai-dest-main-card">
                            <div class="ai-dest-card-content">
                                <h2 class="ai-dest-card-title"><span id="aiDestTitleCity">Bengaluru</span>, <span id="aiDestTitleCountry">India</span></h2>
                                <p class="ai-dest-card-desc" id="aiDestDescription">
                                    Bengaluru, often referred to as the "Silicon Valley of India," is a bustling metropolis known for its thriving IT industry and cosmopolitan vibe. The city is a blend of modernity and tradition, with verdant parks like Cubbon Park offering tranquil retreats amidst urban sprawl.
                                </p>
                            </div>
                            <div class="ai-dest-hero-img" id="aiDestHeroImg"></div>
                            
                            <div class="ai-flight-cards-container">
                                <div class="ai-flight-route-header">
                                    <span id="aiRouteText">SIN ⇄ BLR • 1 ADULT</span>
                                </div>
                                
                                <div class="ai-flight-list" id="aiFlightList">
                                    <!-- Cards will be injected via JS -->
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
"""

# Find the closing tag for appContent. 
# appContent ends right before bottom-nav in index.html.
# Let's verify by finding `<div class="bottom-nav">`
html = html[:bottom_nav_idx] + screen_html + '\n                ' + html[bottom_nav_idx:]

with open('index.html', 'w') as f:
    f.write(html)
