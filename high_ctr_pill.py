import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_text = """                                                <div style="text-align: center; color: rgba(255,255,255,0.95); font-size: 11px; line-height: 1.4; padding: 0 20px;">
                                                    <strong style="color: #ffffff; font-weight: 800;">Veg Club, Seat 12A, Fast Track</strong><br/>
                                                    are already included.
                                                </div>"""

new_text = """                                                <!-- High-CTR Dynamic VIP Pill -->
                                                <div style="margin-top: 4px; display: inline-flex; align-items: center; justify-content: center; padding: 6px 14px; background: linear-gradient(90deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%); border: 1px solid rgba(255,255,255,0.3); border-radius: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1), inset 0 1px 1px rgba(255,255,255,0.4); animation: pulse-glow 2s infinite ease-in-out;">
                                                    <span style="font-size: 13px; margin-right: 6px;">✨</span>
                                                    <span style="font-size: 11px; font-weight: 800; color: #ffffff; letter-spacing: 0.2px;">
                                                        Your usuals are <span style="color: #4ade80;">already included!</span>
                                                    </span>
                                                </div>"""

content = content.replace(old_text, new_text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('style.css', 'a', encoding='utf-8') as f:
    f.write('''
/* High CTR Pulse Glow for VIP Pill */
@keyframes pulse-glow {
    0% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.4); }
    70% { box-shadow: 0 0 0 6px rgba(255, 255, 255, 0); }
    100% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); }
}
''')

print("Pill added.")
