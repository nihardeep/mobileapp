import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update passenger card inline styles for smaller size & slower animation
# Decrease padding, gaps, and avatar sizes. Increase animation duration/delays.
html = re.sub(r'animation: staggerFadeIn 0\.4s', 'animation: staggerFadeIn 0.6s', html)
# Slow down the delays
for i in range(1, 9):
    # Old delay was i * 0.1, now i * 0.15
    old_delay = f"animation-delay: {i*0.1:.1f}s;"
    new_delay = f"animation-delay: {i*0.15:.2f}s;"
    html = html.replace(old_delay, new_delay)
    
    # Also fix the integer formatting like 0.10s -> 0.15s
    # In my previous python script I did f"{num * 0.1}s", so for 1 it was "0.1s", 2 was "0.2s"
    html = html.replace(f"animation-delay: {i*0.1}s;", f"animation-delay: {i*0.15}s;")

# Also update the Add Remaining Btn delay
html = html.replace('animation-delay: 0.6s;', 'animation-delay: 0.9s;')

# Make the cards smaller via inline styles: avatar 40px -> 32px, gap 16px -> 12px
html = html.replace('width: 40px; height: 40px;', 'width: 32px; height: 32px; font-size: 12px;')
html = html.replace('gap: 16px;', 'gap: 12px;')


# 2. Contact Details section redesign
old_contact = """                        <!-- Contact Details -->
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

if old_contact in html:
    html = html.replace(old_contact, new_contact)
else:
    print("Could not find old contact snippet, skipping replacement.")

with open('index.html', 'w') as f:
    f.write(html)

