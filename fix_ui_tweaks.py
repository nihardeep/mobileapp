import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Add more chips to the saved list to demonstrate scrolling
old_chips_end = """                                <div class="chip-checkbox"></div>
                            </div>
                        </div>"""

new_chips = """                                <div class="chip-checkbox"></div>
                            </div>
                            <!-- Saved Item 3 -->
                            <div class="saved-passenger-chip" onclick="toggleSavedPassengerChip(this, 'Alka Pande')">
                                <div>
                                    <div style="font-size: 12px; font-weight: 800; color: #0f172a;">Alka Pande</div>
                                    <div style="font-size: 10px; color: #64748b;">Adult - Single seat</div>
                                </div>
                                <div class="chip-checkbox"></div>
                            </div>
                            <!-- Saved Item 4 -->
                            <div class="saved-passenger-chip" onclick="toggleSavedPassengerChip(this, 'Ravi Kumar')">
                                <div>
                                    <div style="font-size: 12px; font-weight: 800; color: #0f172a;">Ravi Kumar</div>
                                    <div style="font-size: 10px; color: #64748b;">Adult - Single seat</div>
                                </div>
                                <div class="chip-checkbox"></div>
                            </div>
                            <!-- Saved Item 5 -->
                            <div class="saved-passenger-chip" onclick="toggleSavedPassengerChip(this, 'Priya Singh')">
                                <div>
                                    <div style="font-size: 12px; font-weight: 800; color: #0f172a;">Priya Singh</div>
                                    <div style="font-size: 10px; color: #64748b;">Child - Single seat</div>
                                </div>
                                <div class="chip-checkbox"></div>
                            </div>
                        </div>"""

html = html.replace(old_chips_end, new_chips)


# 2. Update Passenger Cards Container to have 8 cards with stagger
def get_card(num, is_completed=False, name="", type_label="Adult", display="flex"):
    delay = num * 0.1
    if is_completed:
        return f"""
                            <div class="passenger-card completed" id="passenger-card-{num}" onclick="openPassengerForm({num}, '{name}', '{type_label}', 'Female')" style="border: 2px solid #22c55e; background: #fff; display: {display}; animation: staggerFadeIn 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) forwards; animation-delay: {delay}s; opacity: 0; transform: translateY(15px);">
                                <div style="display: flex; align-items: center; gap: 16px;">
                                    <div class="passenger-avatar" style="background: rgba(34, 197, 94, 0.1); color: #22c55e;">{name[:2].upper() if name else 'RS'}</div>
                                    <div style="flex: 1;">
                                        <div class="passenger-name" style="color: #22c55e;">{name}</div>
                                        <div class="passenger-type">{type_label}</div>
                                    </div>
                                    <div class="passenger-status" style="font-size: 12px; color: var(--indigo-blue); font-weight: 800;">Edit ✏️</div>
                                </div>
                            </div>"""
    else:
        return f"""
                            <div class="passenger-card empty" id="passenger-card-{num}" onclick="openPassengerForm({num}, '', '{type_label}', '')" style="border: 1px solid #cbd5e1; background: #fff; display: {display}; animation: staggerFadeIn 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) forwards; animation-delay: {delay}s; opacity: 0; transform: translateY(15px);">
                                <div style="display: flex; align-items: center; gap: 16px;">
                                    <div style="flex: 1;">
                                        <div class="passenger-name">Passenger {num}</div>
                                        <div class="passenger-type">{type_label}</div>
                                    </div>
                                    <div class="passenger-add-btn">Add details ></div>
                                </div>
                            </div>"""

cards_html = """                        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 16px;">
                            <div style="font-size: 16px; font-weight: 800; color: #0f172a;">Passengers</div>
                            <div style="font-size: 12px; color: var(--indigo-blue); font-weight: 700;"><span id="passenger-added-count">1</span>/8 Added</div>
                        </div>

                        <!-- Passenger Cards Container -->
                        <div id="passenger-cards-container" style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 32px;">"""
cards_html += get_card(1, True, 'Ragini Shah', 'Adult')
cards_html += get_card(2, False, '', 'Child')
cards_html += get_card(3, False, '', 'Senior Citizen')
cards_html += get_card(4, False, '', 'Adult')
cards_html += get_card(5, False, '', 'Adult')
cards_html += f"""
                            <div id="addRemainingBtn" onclick="showRemainingCards()" style="text-align: center; padding: 12px; margin-top: 8px; font-size: 14px; font-weight: 800; color: var(--indigo-blue); background: rgba(14,165,233,0.1); border-radius: 12px; cursor: pointer; animation: staggerFadeIn 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) forwards; animation-delay: 0.6s; opacity: 0; transform: translateY(15px);">
                                Add Remaining (3) ⬇️
                            </div>"""
cards_html += get_card(6, False, '', 'Adult', 'none')
cards_html += get_card(7, False, '', 'Child', 'none')
cards_html += get_card(8, False, '', 'Infant', 'none')
cards_html += """
                        </div>"""

# Replace the entire old cards container logic
start_cards = html.find('                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">')
if start_cards == -1:
    # try baseline
    start_cards = html.find('                        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 16px;">')

end_cards = html.find('                        <!-- Contact Details -->')

if start_cards != -1 and end_cards != -1:
    html = html[:start_cards] + cards_html + '\n' + html[end_cards:]


# 3. Redesign Contact Details
old_contact = """                        <!-- Contact Details -->
                        <div style="margin-bottom: 32px;">
                            <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-bottom: 4px;">Contact details</div>
                            <div style="font-size: 11px; color: #64748b; margin-bottom: 16px;">The flyer must have access to the mobile number submitted below for mandatory travel updates.</div>
                            
                            <div class="neo-card" style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                                <div style="font-size: 16px;">📱</div>
                                <div style="font-size: 14px; font-weight: 700; color: #0f172a;">+91</div>
                                <div style="width: 1px; height: 20px; background: #cbd5e1;"></div>
                                <input type="tel" value="99485939403" readonly style="flex: 1; border: none; background: transparent; outline: none; font-size: 14px; font-weight: 600; color: #333;">
                            </div>
                            
                            <div class="neo-card" style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                                <div style="font-size: 16px;">✉️</div>
                                <input type="email" value="raginishah@gmail.com" readonly style="flex: 1; border: none; background: transparent; outline: none; font-size: 14px; font-weight: 600; color: #333;">
                            </div>
                        </div>"""

new_contact = """                        <!-- Contact Details -->
                        <div style="margin-bottom: 32px;">
                            <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-bottom: 4px;">Contact details</div>
                            <div style="font-size: 11px; color: #64748b; margin-bottom: 16px;">The flyer must have access to the mobile number submitted below for mandatory travel updates.</div>
                            
                            <div class="neo-input-wrapper" style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px; background: #fff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 4px 16px;">
                                <select style="border: none; background: transparent; font-size: 16px; font-weight: 700; color: #0f172a; outline: none; -webkit-appearance: none; cursor: pointer; padding-right: 8px;">
                                    <option value="+91">🇮🇳 +91</option>
                                    <option value="+1">🇺🇸 +1</option>
                                    <option value="+44">🇬🇧 +44</option>
                                    <option value="+61">🇦🇺 +61</option>
                                    <option value="+971">🇦🇪 +971</option>
                                </select>
                                <div style="width: 1px; height: 24px; background: #e2e8f0;"></div>
                                <input type="tel" value="99485 93940" style="flex: 1; border: none; background: transparent; outline: none; font-size: 15px; font-weight: 700; color: #0f172a; letter-spacing: 0.5px; padding: 12px 0;">
                                <div style="color: #22c55e;">
                                    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                </div>
                            </div>
                            
                            <div class="neo-input-wrapper" style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px; background: #fff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 12px 16px;">
                                <div style="font-size: 16px; opacity: 0.5;">✉️</div>
                                <input type="email" value="raginishah@gmail.com" style="flex: 1; border: none; background: transparent; outline: none; font-size: 14px; font-weight: 600; color: #0f172a;">
                            </div>
                            
                            <div style="font-size: 12px; color: var(--indigo-blue); font-weight: 800; cursor: pointer; display: inline-block;">+ Add another contact number</div>
                        </div>"""

html = html.replace(old_contact, new_contact)

with open('index.html', 'w') as f:
    f.write(html)
