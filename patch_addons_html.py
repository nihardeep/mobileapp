import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update the Continue button
html = html.replace("onclick=\"alert('Proceeding to addons!')\"", "onclick=\"navigateTo('addons')\"")

# 2. Add the screenAddons HTML
addons_html = """
                <div class="screen" id="screenAddons">
                    <div class="passenger-header">
                        <div class="passenger-nav-bar" style="display: flex; justify-content: space-between; align-items: center; padding: 16px 24px; position: sticky; top: 0; background: #ffffff; z-index: 10;">
                            <div class="back-btn-chevron" onclick="navigateTo('passenger')">
                                <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="15 18 9 12 15 6"></polyline>
                                </svg>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 16px; font-weight: 800; color: #1e293b;">Add-ons</div>
                                <div style="font-size: 10px; font-weight: 600; color: #64748b; margin-top: 2px;">Step 2/4</div>
                            </div>
                            <div class="skip-btn" style="font-size: 14px; font-weight: 700; color: var(--indigo-blue); cursor: pointer;" onclick="alert('Proceeding to Payment!')">Skip</div>
                        </div>
                    </div>

                    <div class="addons-content-scroll" style="flex: 1; overflow-y: auto; background: #f8fafc; padding-bottom: 120px;">
                        
                        <!-- Route Sector Indicator -->
                        <div class="addon-sector-container">
                            <div class="addon-sector-pill active">DEL — BOM</div>
                            <div class="addon-sector-pill inactive">BOM — DEL <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
                        </div>

                        <!-- Passenger Selector -->
                        <div class="addon-pax-section">
                            <div class="addon-pax-title">Select Add-ons for</div>
                            <div class="addon-pax-chips" id="addonPaxChipsContainer">
                                <!-- Populated dynamically via JS -->
                            </div>
                        </div>

                        <!-- Addon Category Tabs -->
                        <div class="addon-category-tabs">
                            <div class="addon-tab active">Recommended</div>
                            <div class="addon-tab">Premium</div>
                            <div class="addon-tab">Meals</div>
                            <div class="addon-tab">Excess Baggage</div>
                        </div>

                        <!-- Recommended Bundles Section -->
                        <div class="addon-bundles-section">
                            <div class="addon-section-title">Personalised Bundles for Your Journey</div>
                            <div class="addon-bundles-scroll" id="addonBundlesContainer">
                                
                                <!-- GoFlex Bundle -->
                                <div class="addon-bundle-card">
                                    <div class="bundle-discount-badge">Up to 30% off</div>
                                    <div class="bundle-header">
                                        <div class="bundle-title">GoFlex</div>
                                    </div>
                                    <div class="bundle-features">
                                        <ul>
                                            <li>Fast Forward</li>
                                            <li>Fruit Cake Slice + Beverage of choice</li>
                                            <li>Standard Seats</li>
                                        </ul>
                                    </div>
                                    <div class="bundle-images">
                                        <img src="https://images.unsplash.com/photo-1579546929518-9e396f3cc809?ixlib=rb-1.2.1&auto=format&fit=crop&w=150&q=80" alt="Fast Forward">
                                        <img src="https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?ixlib=rb-1.2.1&auto=format&fit=crop&w=150&q=80" alt="Food">
                                        <img src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?ixlib=rb-1.2.1&auto=format&fit=crop&w=150&q=80" alt="Seat">
                                    </div>
                                    <div class="bundle-footer">
                                        <div class="bundle-price">
                                            <span class="old-price">₹ 1,499</span>
                                            <span class="new-price">₹ 999</span>
                                        </div>
                                        <button class="bundle-add-btn" onclick="addAddon(this, 'GoFlex', 999)">Add</button>
                                    </div>
                                </div>
                                
                                <!-- GoSmart Bundle -->
                                <div class="addon-bundle-card">
                                    <div class="bundle-header">
                                        <div class="bundle-title">GoSmart</div>
                                    </div>
                                    <div class="bundle-features">
                                        <ul>
                                            <li>Paneer Tikka Sandwich + Beverage of choice</li>
                                            <li>Premium Seats</li>
                                        </ul>
                                    </div>
                                    <div class="bundle-images">
                                        <img src="https://images.unsplash.com/photo-1528735602780-2552fd46c7af?ixlib=rb-1.2.1&auto=format&fit=crop&w=150&q=80" alt="Sandwich">
                                        <img src="https://images.unsplash.com/photo-1569154941061-e231b4725ef1?ixlib=rb-1.2.1&auto=format&fit=crop&w=150&q=80" alt="Premium Seat">
                                    </div>
                                    <div class="bundle-footer">
                                        <div class="bundle-price">
                                            <span class="old-price">₹ 1,299</span>
                                            <span class="new-price">₹ 799</span>
                                        </div>
                                        <button class="bundle-add-btn" onclick="addAddon(this, 'GoSmart', 799)">Add</button>
                                    </div>
                                </div>

                            </div>
                        </div>

                        <!-- Popular Add-ons (Meals/Seats) -->
                        <div class="addon-bundles-section" style="margin-top: 16px;">
                            <div class="addon-section-title">Most popular add-ons</div>
                            
                            <div id="smart-inclusion-banner" style="display: none; background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 8px; padding: 12px; margin: 0 20px 16px; align-items: center; gap: 12px;">
                                <div style="background: #22c55e; color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                                    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                </div>
                                <div>
                                    <div style="font-size: 12px; font-weight: 800; color: #15803d;" id="smart-inclusion-title">Student Benefits Applied</div>
                                    <div style="font-size: 10px; font-weight: 600; color: #166534;" id="smart-inclusion-desc">10kg extra baggage and standard seat is free!</div>
                                </div>
                            </div>

                            <div class="addon-bundles-scroll" id="addonPopularContainer">
                                <!-- Pre-rendered Popular Meal -->
                                <div class="addon-meal-card">
                                    <div class="meal-discount-badge" id="meal-discount-badge">Up to 10% off</div>
                                    <div class="meal-tag veg"><div class="veg-dot"></div> Veg</div>
                                    <div class="meal-image">
                                        <img src="https://images.unsplash.com/photo-1528735602780-2552fd46c7af?ixlib=rb-1.2.1&auto=format&fit=crop&w=200&q=80" alt="Sandwich">
                                    </div>
                                    <div class="meal-details">
                                        <div class="meal-title">Paneer Tikka Sandwich + Beverage of choice</div>
                                        <div class="meal-footer">
                                            <div class="meal-price">
                                                <span class="old-price">₹ 400</span>
                                                <span class="new-price" id="meal-price-val">₹ 370</span>
                                            </div>
                                            <button class="bundle-add-btn" id="meal-add-btn" onclick="addAddon(this, 'Veg Meal', 370)">Add</button>
                                        </div>
                                        <div class="meal-nutrition">Nutritional info ↗</div>
                                    </div>
                                </div>

                                <!-- Pre-rendered Seat/Eat Combo -->
                                <div class="addon-meal-card">
                                    <div class="meal-image" style="height: 100px;">
                                        <img src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?ixlib=rb-1.2.1&auto=format&fit=crop&w=200&q=80" alt="Seat">
                                    </div>
                                    <div class="meal-details" style="padding-top: 12px;">
                                        <div class="meal-title" style="font-size: 14px;">6E Seat and Eat</div>
                                        <div style="font-size: 10px; color: #64748b; margin-top: 4px; line-height: 1.3;">Standard seat of your choice & A snack combo</div>
                                        <div class="meal-footer" style="margin-top: 12px;">
                                            <div class="meal-price">
                                                <span class="old-price">₹ 1,200</span>
                                                <span class="new-price" id="seat-eat-price">₹ 999</span>
                                            </div>
                                            <button class="bundle-add-btn" id="seat-eat-add-btn" onclick="addAddon(this, '6E Seat & Eat', 999)">Add</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <!-- Upgrade Banner -->
                    <div class="addon-upgrade-banner" style="position: absolute; bottom: 85px; left: 0; right: 0; background: #f0fdf4; border-top: 1px solid #bbf7d0; padding: 12px 24px; display: flex; justify-content: space-between; align-items: center; z-index: 10;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#22c55e" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-4"></path><path d="M12 8h.01"></path></svg>
                            <span style="font-size: 12px; font-weight: 700; color: #166534;">Upgrade to <strong style="color: #15803d;">UpFront @2,499</strong></span>
                        </div>
                        <div style="font-size: 10px; font-weight: 700; color: var(--indigo-blue);">See Benefits ↗</div>
                    </div>

                    <!-- Sticky Action Footer -->
                    <div class="passenger-sticky-footer" style="position: sticky; bottom: 0; left: 0; right: 0; padding: 16px 24px; background: #ffffff; box-shadow: 0 -4px 20px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; z-index: 11; border-top: 1px solid rgba(0,0,0,0.05);">
                        <div style="flex: 1; text-align: left; display: flex; flex-direction: column; justify-content: center;">
                            <div style="font-size: 10px; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 2px;">Total Fare</div>
                            <div style="display: flex; align-items: baseline; gap: 8px;">
                                <div style="font-size: 20px; font-weight: 800; color: #0f172a;" id="addon-total-fare">₹ 6,182</div>
                            </div>
                            <div style="font-size: 10px; font-weight: 700; color: var(--indigo-blue); margin-top: 2px;">Trip & Fare Details ^</div>
                        </div>
                        <button class="primary-btn" style="padding: 12px 32px; border-radius: 8px; font-size: 14px;" onclick="alert('Proceeding to Payment!')">Next</button>
                    </div>

                    <!-- Green Toast Notification -->
                    <div id="addon-toast" style="position: absolute; bottom: 140px; left: 20px; right: 20px; background: #f0fdf4; border: 1.5px solid #22c55e; border-radius: 12px; padding: 16px; display: flex; gap: 12px; z-index: 20; transform: translateY(150%); opacity: 0; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);">
                        <div style="background: #22c55e; color: white; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                            <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        </div>
                        <div style="flex: 1;">
                            <div style="font-size: 14px; font-weight: 800; color: #15803d; margin-bottom: 4px;">Add-on successfully added</div>
                            <div style="font-size: 11px; font-weight: 500; color: #166534;">You can review or modify it anytime before checkout.</div>
                        </div>
                        <div style="color: #15803d; cursor: pointer;" onclick="document.getElementById('addon-toast').style.transform = 'translateY(150%)'; document.getElementById('addon-toast').style.opacity='0';">
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                        </div>
                    </div>

                </div>
<div class="screen" id="screenDestinationAI">
"""

html = html.replace('<div class="screen" id="screenDestinationAI">', addons_html)

with open('index.html', 'w') as f:
    f.write(html)
