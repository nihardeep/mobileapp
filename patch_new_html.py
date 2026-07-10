with open('index.html', 'r') as f:
    html = f.read()

new_html = """
<div class="screen" id="screenAddons" style="background: #f8fafc;">
    
    <!-- Ultra-Premium Header & Sticky Cart -->
    <div style="position: sticky; top: 0; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(20px); z-index: 50; padding-top: 16px; border-bottom: 1px solid rgba(0,0,0,0.05);">
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0 24px;">
            <div class="back-btn-chevron" onclick="navigateTo('passenger')">
                <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#0f172a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="15 18 9 12 15 6"></polyline>
                </svg>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 18px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px;">Add-ons</div>
                <div style="font-size: 10px; font-weight: 700; color: var(--indigo-blue); text-transform: uppercase; letter-spacing: 1px; margin-top: 2px;">DEL — BOM</div>
            </div>
            <div style="font-size: 14px; font-weight: 700; color: #64748b; cursor: pointer;" onclick="alert('Skip to Pay')">Skip</div>
        </div>

        <!-- Dynamic Island Passenger Selector -->
        <div style="padding: 16px 24px; display: flex; gap: 12px; overflow-x: auto; scrollbar-width: none;" id="addonPaxCartContainer">
            <!-- Populated via JS -->
        </div>

        <!-- Scroll-Spy Category Tabs -->
        <div class="addon-spy-tabs">
            <div class="spy-tab active" onclick="scrollToAddonSection('recommended')">Recommended</div>
            <div class="spy-tab" onclick="scrollToAddonSection('meals')">Meals</div>
            <div class="spy-tab" onclick="scrollToAddonSection('baggage')">Baggage</div>
        </div>
    </div>

    <!-- Main Scrollable Feed -->
    <div class="addons-main-feed" id="addonsMainFeed" style="padding: 16px 24px 140px; height: calc(100vh - 180px); overflow-y: auto;">
        
        <!-- SECTION: Recommended -->
        <div class="addon-scroll-section" id="section-recommended">
            <h3 style="font-size: 18px; font-weight: 800; color: #0f172a; margin-bottom: 16px; letter-spacing: -0.5px;">Premium Bundles</h3>
            
            <!-- Dark Mode Premium Card -->
            <div class="premium-bundle-card">
                <div class="bundle-glow"></div>
                <div style="position: relative; z-index: 2;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
                        <div>
                            <div style="font-size: 24px; font-weight: 900; color: #ffffff; letter-spacing: -1px;">GoFlex</div>
                            <div style="font-size: 12px; color: #94a3b8; font-weight: 600; margin-top: 4px;">The Ultimate Freedom</div>
                        </div>
                        <div style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; font-size: 10px; font-weight: 800; padding: 6px 12px; border-radius: 20px; text-transform: uppercase; letter-spacing: 1px;">Best Value</div>
                    </div>
                    
                    <div style="display: flex; gap: 12px; margin-bottom: 20px;">
                        <div class="bundle-icon-pill"><span style="font-size: 16px;">⏩</span> Fast Forward</div>
                        <div class="bundle-icon-pill"><span style="font-size: 16px;">💺</span> Any Seat</div>
                        <div class="bundle-icon-pill"><span style="font-size: 16px;">🍱</span> Hot Meal</div>
                    </div>

                    <div style="display: flex; justify-content: space-between; align-items: flex-end; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 16px;">
                        <div>
                            <div style="font-size: 12px; color: #64748b; text-decoration: line-through; font-weight: 600;">₹ 1,499</div>
                            <div style="font-size: 24px; font-weight: 800; color: #ffffff;">₹ 999</div>
                        </div>
                        <button class="neon-add-btn" onclick="toggleAddonCart(this, 'GoFlex', 999)">Add to Cart</button>
                    </div>
                </div>
            </div>

            <!-- GoSmart Light Mode Card -->
            <div class="smart-bundle-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                    <div>
                        <div style="font-size: 20px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px;">GoSmart</div>
                        <div style="font-size: 12px; color: #64748b; font-weight: 600; margin-top: 2px;">Essential Comfort</div>
                    </div>
                </div>
                
                <ul style="margin: 0; padding-left: 16px; font-size: 13px; color: #475569; line-height: 1.6; font-weight: 500; margin-bottom: 16px;">
                    <li>Standard Seat included</li>
                    <li>Choice of cold snack + beverage</li>
                </ul>

                <div style="display: flex; justify-content: space-between; align-items: flex-end; border-top: 1px dashed #cbd5e1; padding-top: 16px;">
                    <div>
                        <div style="font-size: 12px; color: #94a3b8; text-decoration: line-through; font-weight: 600;">₹ 1,000</div>
                        <div style="font-size: 20px; font-weight: 800; color: #0f172a;">₹ 699</div>
                    </div>
                    <button class="standard-add-btn" onclick="toggleAddonCart(this, 'GoSmart', 699)">Add</button>
                </div>
            </div>
        </div>

        <!-- SECTION: Meals -->
        <div class="addon-scroll-section" id="section-meals" style="padding-top: 32px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <h3 style="font-size: 18px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; margin: 0;">In-Flight Meals</h3>
                <div style="display: flex; background: #e2e8f0; border-radius: 8px; padding: 2px;">
                    <div class="meal-filter active" onclick="filterMeals('all', this)">All</div>
                    <div class="meal-filter" onclick="filterMeals('veg', this)"><div class="veg-dot"></div></div>
                    <div class="meal-filter" onclick="filterMeals('nonveg', this)"><div class="nonveg-dot"></div></div>
                </div>
            </div>

            <!-- Smart Inclusion Freebie Banner (Hidden by default) -->
            <div id="meal-freebie-banner" class="celebration-banner">
                <div class="celebration-icon">🎉</div>
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: #15803d;">Popular Fare Perks!</div>
                    <div style="font-size: 11px; font-weight: 600; color: #166534; opacity: 0.8;">Enjoy a complimentary Veg Meal on us.</div>
                </div>
            </div>

            <!-- Immersive Meal Grid -->
            <div class="meal-grid">
                
                <!-- Veg Meal -->
                <div class="immersive-meal-card" data-type="veg">
                    <img src="https://images.unsplash.com/photo-1528735602780-2552fd46c7af?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80" alt="Sandwich" class="meal-bg">
                    <div class="meal-overlay">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div class="meal-diet-tag veg"><div class="veg-dot"></div> Veg</div>
                        </div>
                        <div>
                            <div style="font-size: 14px; font-weight: 800; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">Paneer Tikka Sandwich</div>
                            <div style="font-size: 11px; color: rgba(255,255,255,0.8); margin-top: 2px;">Includes beverage</div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px;">
                                <div class="glass-price" id="veg-meal-price">₹ 370</div>
                                <button class="glass-add-btn" id="veg-meal-btn" onclick="toggleAddonCart(this, 'Paneer Tikka Meal', 370)">Add</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Non-Veg Meal -->
                <div class="immersive-meal-card" data-type="nonveg">
                    <img src="https://images.unsplash.com/photo-1626200419189-39c8c93a0293?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80" alt="Chicken" class="meal-bg">
                    <div class="meal-overlay">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div class="meal-diet-tag nonveg"><div class="nonveg-dot"></div> Non-Veg</div>
                        </div>
                        <div>
                            <div style="font-size: 14px; font-weight: 800; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">Chicken Junglee Sandwich</div>
                            <div style="font-size: 11px; color: rgba(255,255,255,0.8); margin-top: 2px;">Includes beverage</div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px;">
                                <div class="glass-price">₹ 420</div>
                                <button class="glass-add-btn" onclick="toggleAddonCart(this, 'Chicken Meal', 420)">Add</button>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <!-- SECTION: Baggage -->
        <div class="addon-scroll-section" id="section-baggage" style="padding-top: 32px;">
            <h3 style="font-size: 18px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; margin-bottom: 16px;">Excess Baggage</h3>
            
            <!-- Smart Inclusion Freebie Banner -->
            <div id="baggage-freebie-banner" class="celebration-banner">
                <div class="celebration-icon">🎓</div>
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: #15803d;">Student Perks Applied!</div>
                    <div style="font-size: 11px; font-weight: 600; color: #166534; opacity: 0.8;">10kg extra baggage is automatically included.</div>
                </div>
            </div>

            <!-- Baggage Stepper -->
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="font-size: 24px;">🧳</div>
                        <div>
                            <div style="font-size: 14px; font-weight: 800; color: #0f172a;">Prepaid Extra Baggage</div>
                            <div style="font-size: 11px; color: #64748b; margin-top: 2px;">Save up to 20% vs airport rates</div>
                        </div>
                    </div>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; background: #f8fafc; padding: 8px; border-radius: 30px; border: 1px solid #e2e8f0;">
                    <div class="stepper-btn" onclick="updateBaggage(-5)">-</div>
                    <div style="font-size: 18px; font-weight: 900; color: var(--indigo-blue); min-width: 60px; text-align: center;"><span id="baggage-val">0</span> kg</div>
                    <div class="stepper-btn" onclick="updateBaggage(5)">+</div>
                </div>
                <div style="text-align: center; font-size: 12px; font-weight: 700; color: #0f172a; margin-top: 16px;">
                    Additional cost: <span id="baggage-cost" style="color: var(--indigo-blue);">₹ 0</span>
                </div>
            </div>
        </div>

    </div> <!-- End Main Feed -->

    <!-- Premium Metallic UpFront Banner -->
    <div style="position: fixed; bottom: 85px; left: 16px; right: 16px; background: linear-gradient(135deg, #f8fafc, #e2e8f0); border: 1px solid #cbd5e1; border-radius: 12px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; z-index: 100; box-shadow: 0 -4px 20px rgba(0,0,0,0.05);">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: linear-gradient(135deg, #001b94, #2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; font-size: 16px; font-style: italic;">UpFront</div>
            <div style="font-size: 11px; font-weight: 700; color: #475569;">Upgrade @ ₹2,499</div>
        </div>
        <div style="font-size: 10px; font-weight: 800; color: var(--indigo-blue); text-transform: uppercase; letter-spacing: 0.5px;">See Benefits ➔</div>
    </div>

    <!-- Sticky Bottom Checkout Bar -->
    <div style="position: fixed; bottom: 0; left: 0; right: 0; background: #ffffff; padding: 16px 24px 24px; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; z-index: 101; box-shadow: 0 -10px 30px rgba(0,0,0,0.05);">
        <div>
            <div style="font-size: 10px; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">Total Fare</div>
            <div style="font-size: 24px; font-weight: 900; color: #0f172a; letter-spacing: -0.5px;" id="addon-checkout-total">₹ 6,182</div>
        </div>
        <button class="primary-btn" style="padding: 14px 40px; border-radius: 30px; font-size: 16px; font-weight: 800; box-shadow: 0 4px 15px rgba(0,27,148,0.2);" onclick="alert('Proceeding to Checkout!')">Continue</button>
    </div>

</div>
<div class="screen" id="screenDestinationAI">
"""

html = html.replace('<div class="screen" id="screenDestinationAI">', new_html)

with open('index.html', 'w') as f:
    f.write(html)
