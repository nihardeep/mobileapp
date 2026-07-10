import re

with open('index.html', 'r') as f:
    html = f.read()

old_contact = """                        <!-- Contact Details -->
                        <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-bottom: 16px;">Contact Details</div>
                        <div class="neo-card" style="padding: 20px; display: flex; flex-direction: column; gap: 12px; margin-bottom: 24px;">
                            <div class="neo-input-group" style="display: flex; align-items: center; gap: 12px; background: #E6EAF0; padding: 12px 16px; border-radius: 12px; box-shadow: inset 2px 2px 5px rgba(163,177,198,0.5), inset -2px -2px 5px rgba(255,255,255,0.8);">
                                <div style="font-size: 16px;">📞</div>
                                <input type="tel" value="+91 9948593940" readonly style="flex: 1; border: none; background: transparent; outline: none; font-size: 14px; font-weight: 600; color: #333;">
                            </div>
                            <div class="neo-input-group" style="display: flex; align-items: center; gap: 12px; background: #E6EAF0; padding: 12px 16px; border-radius: 12px; box-shadow: inset 2px 2px 5px rgba(163,177,198,0.5), inset -2px -2px 5px rgba(255,255,255,0.8);">
                                <div style="font-size: 16px;">✉️</div>
                                <input type="email" value="raginishah@gmail.com" readonly style="flex: 1; border: none; background: transparent; outline: none; font-size: 14px; font-weight: 600; color: #333;">
                            </div>
                        </div>"""

new_contact = """                        <!-- Contact Details -->
                        <div class="neo-card" style="margin-bottom: 32px; padding: 20px;">
                            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                                <div style="width: 32px; height: 32px; border-radius: 10px; background: #E6EAF0; display: flex; align-items: center; justify-content: center; box-shadow: inset 2px 2px 5px rgba(163,177,198,0.5), inset -2px -2px 5px rgba(255,255,255,0.8); font-size: 14px;">📞</div>
                                <div>
                                    <div style="font-size: 16px; font-weight: 800; color: #0f172a;">Contact Details</div>
                                    <div style="font-size: 10px; color: #64748b;">Required for flight updates</div>
                                </div>
                            </div>
                            
                            <div class="neo-input" style="display: flex; align-items: center; gap: 8px; margin-top: 16px; background: #E6EAF0; border-radius: 12px; padding: 4px 16px; box-shadow: inset 3px 3px 6px rgba(163,177,198,0.5), inset -3px -3px 6px rgba(255,255,255,0.8);">
                                <select style="border: none; background: transparent; font-size: 15px; font-weight: 700; color: #0f172a; outline: none; -webkit-appearance: none; cursor: pointer; padding-right: 4px;">
                                    <option value="+91">🇮🇳 +91</option>
                                    <option value="+1">🇺🇸 +1</option>
                                    <option value="+44">🇬🇧 +44</option>
                                    <option value="+61">🇦🇺 +61</option>
                                    <option value="+971">🇦🇪 +971</option>
                                </select>
                                <div style="width: 1px; height: 20px; background: rgba(0,0,0,0.1);"></div>
                                <input type="tel" value="99485 93940" style="flex: 1; border: none; background: transparent; outline: none; font-size: 14px; font-weight: 700; color: #0f172a; letter-spacing: 0.5px; padding: 12px 0;">
                                <div style="color: #22c55e;">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                </div>
                            </div>
                            
                            <div class="neo-input" style="display: flex; align-items: center; gap: 12px; margin-top: 12px; background: #E6EAF0; border-radius: 12px; padding: 12px 16px; box-shadow: inset 3px 3px 6px rgba(163,177,198,0.5), inset -3px -3px 6px rgba(255,255,255,0.8);">
                                <div style="font-size: 14px; opacity: 0.5;">✉️</div>
                                <input type="email" value="raginishah@gmail.com" style="flex: 1; border: none; background: transparent; outline: none; font-size: 14px; font-weight: 600; color: #0f172a;">
                            </div>
                            
                            <div style="font-size: 12px; color: var(--indigo-blue); font-weight: 800; cursor: pointer; margin-top: 16px; display: inline-block;">+ Add another contact</div>
                        </div>"""

html = html.replace(old_contact, new_contact)

with open('index.html', 'w') as f:
    f.write(html)

