import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update the Next button in the fare popup
content = content.replace(
    '''<button class="primary-btn" style="padding: 12px 24px; border-radius: 8px; font-size: 14px;" onclick="closeFarePopup()">Next</button>''',
    '''<button class="primary-btn" style="padding: 12px 24px; border-radius: 8px; font-size: 14px;" onclick="goToPassengerDetails()">Next</button>'''
)

# 2. Inject screenPassenger before screenDestinationAI
screen_html = """
                <!-- SCREEN 5: PASSENGER DETAILS -->
                <div class="screen" id="screenPassenger">
                    <div class="passenger-header">
                        <div class="passenger-nav-bar" style="display: flex; justify-content: space-between; align-items: center; padding: 16px 24px; position: sticky; top: 0; background: #E6EAF0; z-index: 10;">
                            <div class="back-btn-chevron" onclick="navigateTo('results')">
                                <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="15 18 9 12 15 6"></polyline>
                                </svg>
                            </div>
                            <div style="font-size: 18px; font-weight: 800; color: #1e293b;">Passenger Details</div>
                            <div style="width: 24px;"></div> <!-- Spacer -->
                        </div>
                    </div>
                    
                    <div class="passenger-body" style="padding: 16px 24px 120px 24px;">
                        
                        <!-- Flight Info Snippet -->
                        <div class="neo-card" style="margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; padding: 16px;">
                            <div>
                                <div style="font-size: 12px; color: #64748b; font-weight: 600; margin-bottom: 4px;">Flight Summary</div>
                                <div style="font-size: 16px; font-weight: 800; color: #0f172a;">DEL → BOM</div>
                                <div style="font-size: 12px; color: #64748b;">3 Adults, 1 Child • <span id="passenger-fare-type" style="color: var(--indigo-blue); font-weight: 700;">Saver</span></div>
                            </div>
                            <div style="font-size: 12px; color: var(--indigo-blue); font-weight: 700;">View details ></div>
                        </div>

                        <!-- Progress Bar -->
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <div style="font-size: 16px; font-weight: 800; color: #0f172a;">Passengers</div>
                            <div style="font-size: 12px; font-weight: 700; color: var(--indigo-blue);"><span id="passenger-added-count">1</span>/4 Added</div>
                        </div>

                        <!-- Passenger Cards Container -->
                        <div id="passenger-cards-container" style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 32px;">
                            <!-- Passenger 1 (Pre-filled) -->
                            <div class="passenger-card completed" id="passenger-card-1" onclick="openPassengerForm(1, 'Ragini Shah', 'Adult', 'Female')">
                                <div style="display: flex; align-items: center; gap: 16px;">
                                    <div class="passenger-avatar"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg></div>
                                    <div style="flex: 1;">
                                        <div class="passenger-name">Ragini Shah</div>
                                        <div class="passenger-type">Adult • Saved</div>
                                    </div>
                                    <div class="passenger-status"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#22c55e" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
                                </div>
                            </div>

                            <!-- Passenger 2 (Empty) -->
                            <div class="passenger-card empty" id="passenger-card-2" onclick="openPassengerForm(2, '', 'Adult', '')">
                                <div style="display: flex; align-items: center; gap: 16px;">
                                    <div class="passenger-avatar empty"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg></div>
                                    <div style="flex: 1;">
                                        <div class="passenger-name">Passenger 2</div>
                                        <div class="passenger-type">Adult</div>
                                    </div>
                                    <div class="passenger-add-btn">Add details ></div>
                                </div>
                            </div>

                            <!-- Passenger 3 (Empty) -->
                            <div class="passenger-card empty" id="passenger-card-3" onclick="openPassengerForm(3, '', 'Adult', '')">
                                <div style="display: flex; align-items: center; gap: 16px;">
                                    <div class="passenger-avatar empty"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg></div>
                                    <div style="flex: 1;">
                                        <div class="passenger-name">Passenger 3</div>
                                        <div class="passenger-type">Adult</div>
                                    </div>
                                    <div class="passenger-add-btn">Add details ></div>
                                </div>
                            </div>

                            <!-- Passenger 4 (Child) -->
                            <div class="passenger-card empty" id="passenger-card-4" onclick="openPassengerForm(4, '', 'Child', '')">
                                <div style="display: flex; align-items: center; gap: 16px;">
                                    <div class="passenger-avatar empty"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg></div>
                                    <div style="flex: 1;">
                                        <div class="passenger-name">Passenger 4</div>
                                        <div class="passenger-type">Child (2-12 yrs)</div>
                                    </div>
                                    <div class="passenger-add-btn">Add details ></div>
                                </div>
                            </div>
                        </div>

                        <!-- Contact Details -->
                        <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-bottom: 16px;">Contact Details</div>
                        <div class="neo-card" style="padding: 20px; display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px;">
                            <div class="neo-input-group" style="display: flex; align-items: center; gap: 12px; background: #E6EAF0; padding: 12px 16px; border-radius: 12px; box-shadow: inset 2px 2px 5px rgba(163,177,198,0.5), inset -2px -2px 5px rgba(255,255,255,0.8);">
                                <div style="font-size: 16px;">📞</div>
                                <input type="tel" value="+91 9948593940" readonly style="flex: 1; border: none; background: transparent; outline: none; font-size: 14px; font-weight: 600; color: #333;">
                            </div>
                            <div class="neo-input-group" style="display: flex; align-items: center; gap: 12px; background: #E6EAF0; padding: 12px 16px; border-radius: 12px; box-shadow: inset 2px 2px 5px rgba(163,177,198,0.5), inset -2px -2px 5px rgba(255,255,255,0.8);">
                                <div style="font-size: 16px;">✉️</div>
                                <input type="email" value="raginishah@gmail.com" readonly style="flex: 1; border: none; background: transparent; outline: none; font-size: 14px; font-weight: 600; color: #333;">
                            </div>
                        </div>

                        <!-- Secure Your Trip -->
                        <div class="neo-card" style="padding: 20px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="width: 40px; height: 40px; border-radius: 12px; background: #E6EAF0; display: flex; align-items: center; justify-content: center; box-shadow: inset 2px 2px 5px rgba(163,177,198,0.5), inset -2px -2px 5px rgba(255,255,255,0.8);">🛡️</div>
                                <div>
                                    <div style="font-size: 14px; font-weight: 800; color: #0f172a;">Secure your trip</div>
                                    <div style="font-size: 11px; color: #64748b;">Zero cancellation from ₹425</div>
                                </div>
                            </div>
                            <div style="font-size: 14px; color: var(--indigo-blue); font-weight: 800;">Add +</div>
                        </div>

                        <!-- Terms & Conditions Checkboxes -->
                        <div style="display: flex; flex-direction: column; gap: 16px; margin-top: 32px;">
                            <label style="font-size: 11px; color: #64748b; line-height: 1.4; display: flex; align-items: flex-start; gap: 12px;">
                                <input type="checkbox" checked style="margin-top: 2px;">
                                <span>I have read and agree to IndiGo's <span style="color: var(--indigo-blue); font-weight: 700;">Conditions of Carriage</span>. I further agree to the Privacy Policy.</span>
                            </label>
                            <label style="font-size: 11px; color: #64748b; line-height: 1.4; display: flex; align-items: flex-start; gap: 12px;">
                                <input type="checkbox" checked style="margin-top: 2px;">
                                <span>Get updates on WhatsApp. By subscribing to this, you agree to the terms.</span>
                            </label>
                        </div>
                    </div>

                    <!-- Sticky Action Footer -->
                    <div class="passenger-sticky-footer" style="position: fixed; bottom: 0; left: 0; right: 0; padding: 16px 24px; background: #E6EAF0; box-shadow: 0 -4px 20px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; z-index: 10; border-top: 1px solid rgba(255,255,255,0.5);">
                        <div style="flex: 1; text-align: left;">
                            <div style="font-size: 10px; font-weight: 700; color: #64748b; text-transform: uppercase;">Total Fare</div>
                            <div style="font-size: 20px; font-weight: 800; color: #0f172a;" id="passenger-total-fare">₹ 6,182</div>
                        </div>
                        <button class="primary-btn" id="passenger-next-btn" style="padding: 12px 32px; border-radius: 8px; font-size: 14px; opacity: 0.5;" disabled onclick="alert('Proceeding to addons!')">Continue</button>
                    </div>
                </div>
"""
content = content.replace('<div class="screen" id="screenDestinationAI">', screen_html + '\n<div class="screen" id="screenDestinationAI">')

# 3. Inject passengerFormSheet before studentBenefitsDrawer
sheet_html = """
                <!-- Passenger Form Bottom Sheet -->
                <div class="bottom-sheet-drawer" id="passengerFormSheet" style="z-index: 5000; padding-bottom: 20px;">
                    <div class="drawer-drag-handle" style="width: 36px; height: 4px; background: #cbd5e1; border-radius: 2px; margin: 12px auto 20px auto;"></div>
                    
                    <div style="padding: 0 24px 32px 24px;">
                        <h2 id="passenger-form-title" style="font-size: 20px; font-weight: 800; color: #0f172a; margin: 0 0 24px 0;">Adult 2 Details</h2>
                        
                        <input type="hidden" id="pf-id" value="">
                        <input type="hidden" id="pf-type" value="Adult">

                        <div style="margin-bottom: 24px;">
                            <div style="font-size: 12px; font-weight: 700; color: #64748b; margin-bottom: 12px;">Gender</div>
                            <div class="gender-segmented-control" style="display: flex; background: #E6EAF0; border-radius: 12px; padding: 4px; box-shadow: inset 3px 3px 6px rgba(163,177,198,0.5), inset -3px -3px 6px rgba(255,255,255,0.8);">
                                <div class="gender-segment active" onclick="selectGender('Male')" id="gender-male" style="flex: 1; text-align: center; padding: 12px 0; border-radius: 8px; font-size: 14px; font-weight: 700; color: #64748b; cursor: pointer; transition: 0.2s;">Male</div>
                                <div class="gender-segment" onclick="selectGender('Female')" id="gender-female" style="flex: 1; text-align: center; padding: 12px 0; border-radius: 8px; font-size: 14px; font-weight: 700; color: #64748b; cursor: pointer; transition: 0.2s;">Female</div>
                            </div>
                        </div>

                        <div style="margin-bottom: 16px;">
                            <div class="neo-input-wrapper">
                                <label style="font-size: 10px; font-weight: 700; color: #64748b; margin-bottom: 4px; display: block; padding-left: 4px;">First & Middle Name</label>
                                <input type="text" id="pf-fname" class="neo-input" placeholder="e.g. Ishika" style="width: 100%; box-sizing: border-box; padding: 16px; border-radius: 12px; border: none; background: #E6EAF0; box-shadow: inset 3px 3px 6px rgba(163,177,198,0.5), inset -3px -3px 6px rgba(255,255,255,0.8); outline: none; font-size: 14px; color: #333; font-weight: 600;">
                            </div>
                        </div>

                        <div style="margin-bottom: 24px;">
                            <div class="neo-input-wrapper">
                                <label style="font-size: 10px; font-weight: 700; color: #64748b; margin-bottom: 4px; display: block; padding-left: 4px;">Last Name</label>
                                <input type="text" id="pf-lname" class="neo-input" placeholder="e.g. Sharma" style="width: 100%; box-sizing: border-box; padding: 16px; border-radius: 12px; border: none; background: #E6EAF0; box-shadow: inset 3px 3px 6px rgba(163,177,198,0.5), inset -3px -3px 6px rgba(255,255,255,0.8); outline: none; font-size: 14px; color: #333; font-weight: 600;">
                            </div>
                        </div>
                        
                        <div style="margin-bottom: 24px;">
                            <div class="neo-input-wrapper">
                                <label style="font-size: 10px; font-weight: 700; color: #64748b; margin-bottom: 4px; display: block; padding-left: 4px;">Date of Birth</label>
                                <input type="date" id="pf-dob" class="neo-input" style="width: 100%; box-sizing: border-box; padding: 16px; border-radius: 12px; border: none; background: #E6EAF0; box-shadow: inset 3px 3px 6px rgba(163,177,198,0.5), inset -3px -3px 6px rgba(255,255,255,0.8); outline: none; text-transform: uppercase; font-size: 14px; color: #333; font-weight: 600;">
                            </div>
                        </div>

                        <button class="primary-btn" style="width: 100%; padding: 16px; border-radius: 12px; font-size: 16px; font-weight: 800;" onclick="savePassengerForm()">Save Details</button>
                    </div>
                </div>
"""
content = content.replace('<!-- Student Benefits Drawer -->', sheet_html + '\n<!-- Student Benefits Drawer -->')

with open('index.html', 'w') as f:
    f.write(content)

