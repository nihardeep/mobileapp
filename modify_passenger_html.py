import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Inject "Choose from saved list" into index.html inside passenger-body
saved_list_html = """
                        <!-- Choose from saved list -->
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; margin-top: 24px;">
                            <div style="font-size: 16px; font-weight: 800; color: #0f172a;">Choose from saved list</div>
                            <div style="font-size: 12px; font-weight: 700; color: var(--indigo-blue); cursor: pointer;" onclick="openBulkAddSheet()">View all ></div>
                        </div>
                        <div style="display: flex; gap: 12px; overflow-x: auto; padding-bottom: 16px; margin-bottom: 16px; -webkit-overflow-scrolling: touch; padding-right: 24px; margin-right: -24px;" class="hide-scrollbar">
                            <!-- Saved Item 1 -->
                            <div class="saved-passenger-chip active" onclick="toggleSavedPassengerChip(this, 'Ragini Shah')">
                                <div>
                                    <div style="font-size: 12px; font-weight: 800; color: #0f172a;">Ragini Shah</div>
                                    <div style="font-size: 10px; color: #64748b;">Adult - Single seat</div>
                                </div>
                                <div class="chip-checkbox"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
                            </div>
                            <!-- Saved Item 2 -->
                            <div class="saved-passenger-chip" onclick="toggleSavedPassengerChip(this, 'Smriti Shah')">
                                <div>
                                    <div style="font-size: 12px; font-weight: 800; color: #0f172a;">Smriti Shah</div>
                                    <div style="font-size: 10px; color: #64748b;">Child - Single seat</div>
                                </div>
                                <div class="chip-checkbox"></div>
                            </div>
                        </div>
"""

# Replace the progress bar with saved list + progress bar
html = html.replace('<!-- Progress Bar -->', saved_list_html + '\n                        <!-- Progress Bar -->')

# 2. Add Bulk Add Sheet and Redesign Passenger Form Sheet
new_sheets_html = """
                <!-- Bulk Add Passenger Sheet -->
                <div class="bottom-sheet-drawer" id="savedPassengersSheet" style="z-index: 5000; padding-bottom: 20px;">
                    <div class="drawer-drag-handle" style="width: 36px; height: 4px; background: #cbd5e1; border-radius: 2px; margin: 12px auto 20px auto;"></div>
                    <div style="padding: 0 24px 32px 24px;">
                        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 24px;">
                            <h2 style="font-size: 20px; font-weight: 800; color: #0f172a; margin: 0;">Your saved passenger</h2>
                            <div style="font-size: 12px; color: #64748b; font-weight: 600;">6 Nominees</div>
                        </div>
                        
                        <div style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 32px; max-height: 400px; overflow-y: auto;">
                            <!-- List of saved passengers -->
                            <div class="bulk-saved-item" onclick="toggleBulkCheckbox(this)">
                                <div class="bulk-avatar" style="background: #e0f2fe; color: #0ea5e9;">RS</div>
                                <div style="flex: 1;">
                                    <div style="font-size: 14px; font-weight: 800; color: #0f172a;">Ragini Shah</div>
                                    <div style="font-size: 11px; color: #64748b;">Adult, Single seat</div>
                                </div>
                                <input type="checkbox" class="bulk-checkbox" checked style="width: 20px; height: 20px;">
                                <div class="bulk-edit">✏️</div>
                            </div>
                            <div class="bulk-saved-item" onclick="toggleBulkCheckbox(this)">
                                <div class="bulk-avatar" style="background: #f1f5f9; color: #64748b;">AP</div>
                                <div style="flex: 1;">
                                    <div style="font-size: 14px; font-weight: 800; color: #0f172a;">Alka Pande</div>
                                    <div style="font-size: 11px; color: #64748b;">Adult, Single seat</div>
                                </div>
                                <input type="checkbox" class="bulk-checkbox" style="width: 20px; height: 20px;">
                                <div class="bulk-edit">✏️</div>
                            </div>
                            <div class="bulk-saved-item" onclick="toggleBulkCheckbox(this)">
                                <div class="bulk-avatar" style="background: #e0f2fe; color: #0ea5e9;">RS</div>
                                <div style="flex: 1;">
                                    <div style="font-size: 14px; font-weight: 800; color: #0f172a;">Rajvardhan Shah</div>
                                    <div style="font-size: 11px; color: #64748b;">Adult, Single seat</div>
                                </div>
                                <input type="checkbox" class="bulk-checkbox" style="width: 20px; height: 20px;">
                                <div class="bulk-edit">✏️</div>
                            </div>
                        </div>
                        <button class="primary-btn" style="width: 100%; padding: 16px; border-radius: 12px; font-size: 16px; font-weight: 800;" onclick="applyBulkAdd()">Add details</button>
                    </div>
                </div>

                <!-- Passenger Form Bottom Sheet -->
                <div class="bottom-sheet-drawer" id="passengerFormSheet" style="z-index: 5000; padding-bottom: 20px; height: 85vh; overflow-y: auto;">
                    <div class="drawer-drag-handle" style="width: 36px; height: 4px; background: #cbd5e1; border-radius: 2px; margin: 12px auto 20px auto;"></div>
                    
                    <div style="padding: 0 24px 32px 24px;">
                        <h2 id="passenger-form-title" style="font-size: 20px; font-weight: 800; color: #0f172a; margin: 0 0 24px 0;">Adult Details</h2>
                        
                        <input type="hidden" id="pf-id" value="">
                        <input type="hidden" id="pf-type" value="Adult">

                        <div style="margin-bottom: 24px;">
                            <div style="font-size: 12px; font-weight: 700; color: #64748b; margin-bottom: 12px;">What's your gender?</div>
                            <div class="gender-segmented-control" style="display: flex; gap: 12px;">
                                <div class="gender-segment active" onclick="selectGender('Male')" id="gender-male" style="flex: 1; text-align: center; padding: 12px 0; border-radius: 12px; font-size: 14px; font-weight: 700; color: #0f172a; border: 1px solid var(--indigo-blue); background: rgba(14,165,233,0.05); cursor: pointer;">👨 Male</div>
                                <div class="gender-segment" onclick="selectGender('Female')" id="gender-female" style="flex: 1; text-align: center; padding: 12px 0; border-radius: 12px; font-size: 14px; font-weight: 700; color: #64748b; border: 1px solid #cbd5e1; cursor: pointer;">👩 Female</div>
                            </div>
                        </div>

                        <div class="form-field-group" style="margin-bottom: 20px;">
                            <label style="font-size: 10px; font-weight: 700; color: #64748b; margin-bottom: 4px; display: block;">Nationality</label>
                            <select id="pf-nationality" class="neo-input" style="width: 100%; padding: 14px; border-radius: 12px; border: 1px solid #e2e8f0; background: #fff; font-size: 14px; font-weight: 600; outline: none; -webkit-appearance: none;">
                                <option value="Indian">Indian</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>

                        <div class="form-field-group" style="margin-bottom: 20px;">
                            <label style="font-size: 10px; font-weight: 700; color: #64748b; margin-bottom: 4px; display: block;">First Name and Middle Name</label>
                            <input type="text" id="pf-fname" class="neo-input" placeholder="e.g. Ishika" style="width: 100%; box-sizing: border-box; padding: 14px; border-radius: 12px; border: 1px solid #e2e8f0; background: #fff; outline: none; font-size: 14px; font-weight: 600;">
                        </div>

                        <div class="form-field-group" style="margin-bottom: 8px;">
                            <label style="font-size: 10px; font-weight: 700; color: #64748b; margin-bottom: 4px; display: block;">Last Name</label>
                            <input type="text" id="pf-lname" class="neo-input" placeholder="e.g. Sharma" style="width: 100%; box-sizing: border-box; padding: 14px; border-radius: 12px; border: 1px solid #e2e8f0; background: #fff; outline: none; font-size: 14px; font-weight: 600;">
                        </div>
                        
                        <label class="neo-checkbox-container" style="font-size: 11px; color: #64748b; margin-bottom: 24px; display: flex; align-items: flex-start; gap: 8px;">
                            <input type="checkbox" checked style="margin-top: 2px;">
                            <span>Name must match Government ID</span>
                        </label>
                        
                        <div class="form-field-group" style="margin-bottom: 20px;">
                            <label style="font-size: 10px; font-weight: 700; color: #64748b; margin-bottom: 4px; display: block;">Date of birth (Optional)</label>
                            <input type="date" id="pf-dob" class="neo-input" style="width: 100%; box-sizing: border-box; padding: 14px; border-radius: 12px; border: 1px solid #e2e8f0; background: #fff; outline: none; text-transform: uppercase; font-size: 14px; font-weight: 600;">
                        </div>

                        <div class="form-field-group" style="margin-bottom: 20px;">
                            <label style="font-size: 10px; font-weight: 700; color: #64748b; margin-bottom: 4px; display: block;">Special Assistance (Optional)</label>
                            <select id="pf-assistance" class="neo-input" style="width: 100%; padding: 14px; border-radius: 12px; border: 1px solid #e2e8f0; background: #fff; font-size: 14px; font-weight: 600; outline: none; -webkit-appearance: none;">
                                <option value="">None</option>
                                <option value="Wheelchair">Wheelchair required</option>
                            </select>
                        </div>
                        
                        <div class="form-field-group" style="margin-bottom: 20px;">
                            <label style="font-size: 10px; font-weight: 700; color: #64748b; margin-bottom: 4px; display: block;">IndiGo BluChip Membership Number (Optional)</label>
                            <input type="text" id="pf-bluchip" class="neo-input" placeholder="" style="width: 100%; box-sizing: border-box; padding: 14px; border-radius: 12px; border: 1px solid #e2e8f0; background: #fff; outline: none; font-size: 14px; font-weight: 600;">
                        </div>

                        <label class="neo-checkbox-container" style="font-size: 12px; font-weight: 700; color: #0f172a; margin-bottom: 32px; display: flex; align-items: flex-start; gap: 8px;">
                            <input type="checkbox" checked style="margin-top: 2px;">
                            <span>Save passenger details for future trips</span>
                        </label>

                        <button class="primary-btn" style="width: 100%; padding: 16px; border-radius: 12px; font-size: 16px; font-weight: 800;" onclick="savePassengerForm()">Next</button>
                    </div>
                </div>
"""

start_idx = html.find('<!-- Passenger Form Bottom Sheet -->')
end_idx = html.find('<!-- Student Benefits Drawer -->')
if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_sheets_html + '\n' + html[end_idx:]

# Update Passenger Cards to have Edit icons and green outlines when completed
def update_card(card_html, num, name, type_label, is_completed):
    if is_completed:
        return f"""
                            <div class="passenger-card completed" id="passenger-card-{num}" onclick="openPassengerForm({num}, '{name}', '{type_label}', 'Female')" style="border: 2px solid #22c55e; background: #fff;">
                                <div style="display: flex; align-items: center; gap: 16px;">
                                    <div class="passenger-avatar" style="background: rgba(34, 197, 94, 0.1); color: #22c55e;">RS</div>
                                    <div style="flex: 1;">
                                        <div class="passenger-name" style="color: #22c55e;">{name}</div>
                                        <div class="passenger-type">{type_label}</div>
                                    </div>
                                    <div class="passenger-status" style="font-size: 12px; color: var(--indigo-blue); font-weight: 800;">Edit ✏️</div>
                                </div>
                            </div>
"""
    else:
        return f"""
                            <div class="passenger-card empty" id="passenger-card-{num}" onclick="openPassengerForm({num}, '', '{type_label}', '')" style="border: 1px solid #cbd5e1; background: #fff;">
                                <div style="display: flex; align-items: center; gap: 16px;">
                                    <div style="flex: 1;">
                                        <div class="passenger-name">Passenger {num}</div>
                                        <div class="passenger-type">{type_label}</div>
                                    </div>
                                    <div class="passenger-add-btn">Add details ></div>
                                </div>
                            </div>
"""

# We'll just replace the entire passenger-cards-container
cards_container_start = html.find('<!-- Passenger Cards Container -->')
cards_container_end = html.find('<!-- Contact Details -->')

new_cards_html = """<!-- Passenger Cards Container -->
                        <div id="passenger-cards-container" style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 32px;">
""" + update_card(html, 1, 'Ragini Shah', 'Adult', True) + \
update_card(html, 2, '', 'Child', False) + \
update_card(html, 3, '', 'Senior Citizen', False) + \
update_card(html, 4, '', 'Adult', False) + """
                        </div>
"""
if cards_container_start != -1 and cards_container_end != -1:
    html = html[:cards_container_start] + new_cards_html + '\n                        ' + html[cards_container_end:]

with open('index.html', 'w') as f:
    f.write(html)
