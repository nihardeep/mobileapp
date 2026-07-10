import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

benefits_html = """                                            <!-- Striking Benefits Panel -->
                                            <div style="margin: 0px 16px 10px; background: rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 12px; border: 1px solid rgba(255, 255, 255, 0.2); box-shadow: 0 4px 12px rgba(0,0,0,0.1); display: flex; flex-direction: column; gap: 8px;">
                                                <div style="display: flex; align-items: center; gap: 10px;">
                                                    <div style="background: rgba(16, 185, 129, 0.2); border-radius: 50%; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center;">
                                                        <span style="font-size: 13px;">💰</span>
                                                    </div>
                                                    <span style="font-size: 12px; font-weight: 700; color: #34d399;">Saves you ₹500 on add-ons</span>
                                                </div>
                                                <div style="display: flex; align-items: center; gap: 10px;">
                                                    <div style="background: rgba(56, 189, 248, 0.2); border-radius: 50%; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center;">
                                                        <span style="font-size: 13px;">⚡</span>
                                                    </div>
                                                    <span style="font-size: 12px; font-weight: 700; color: #ffffff;">Seamless journey with pre-selected usuals</span>
                                                </div>
                                                <div style="display: flex; align-items: center; gap: 10px;">
                                                    <div style="background: rgba(245, 158, 11, 0.2); border-radius: 50%; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 0 4px rgba(245,158,11,0.5);">
                                                        <span style="font-size: 12px; color: #fbbf24; font-weight: 900; text-shadow: 0 1px 2px rgba(0,0,0,0.5);">B</span>
                                                    </div>
                                                    <span style="font-size: 12px; font-weight: 700; color: #fcd34d;">Earns 500 BluChip Points</span>
                                                </div>
                                            </div>"""

content = content.replace(benefits_html, "")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Benefits panel removed.")
