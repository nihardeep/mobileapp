import re

with open('index.html', 'r') as f:
    html = f.read()

old_card3 = """                            <div class="passenger-card empty" id="passenger-card-3" onclick="openPassengerForm(3, '', 'Senior Citizen', '')" style="border: 1px solid #cbd5e1; background: #fff; display: flex; animation: staggerFadeIn 0.6s cubic-bezier(0.25, 0.8, 0.25, 1) forwards; animation-delay: 0.44999999999999996s; opacity: 0; transform: translateY(15px);">
                                <div style="display: flex; align-items: center; gap: 12px;">
                                    <div style="flex: 1;">
                                        <div class="passenger-name">Passenger 3</div>
                                        <div class="passenger-type">Senior Citizen</div>
                                    </div>
                                    <div class="passenger-add-btn">Add details ></div>
                                </div>
                            </div>"""

new_card3 = """                            <div class="passenger-card incomplete" id="passenger-card-3" onclick="openPassengerForm(3, 'John', 'Senior Citizen', '')" style="border: 1px dashed #f59e0b; background: rgba(245, 158, 11, 0.05); display: flex; animation: staggerFadeIn 0.6s cubic-bezier(0.25, 0.8, 0.25, 1) forwards; animation-delay: 0.45s; opacity: 0; transform: translateY(15px);">
                                <div style="display: flex; align-items: center; gap: 12px;">
                                    <div class="passenger-avatar" style="background: rgba(245, 158, 11, 0.15); color: #f59e0b; font-weight: 800;">JO</div>
                                    <div style="flex: 1;">
                                        <div class="passenger-name" style="color: #0f172a;">John</div>
                                        <div class="passenger-type">Senior Citizen</div>
                                    </div>
                                    <div style="font-size: 10px; font-weight: 800; color: #f59e0b; background: rgba(245, 158, 11, 0.1); padding: 4px 8px; border-radius: 6px;">Incomplete ⚠️</div>
                                </div>
                            </div>"""

html = html.replace(old_card3, new_card3)

with open('index.html', 'w') as f:
    f.write(html)

