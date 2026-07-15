import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Toggles
content = content.replace(
    '<div class="bp-toggle-btn active" onclick="flipToLeg(1)" id="btnLeg1">DEL ✈ BOM</div>',
    '<div class="bp-toggle-btn active" onclick="flipToLeg(1)" id="btnLeg1">LKO ✈ DEL</div>'
)
content = content.replace(
    '<div class="bp-toggle-btn" onclick="flipToLeg(2)" id="btnLeg2">BOM ✈ GOI</div>',
    '<div class="bp-toggle-btn" onclick="flipToLeg(2)" id="btnLeg2">DEL ✈ AMS</div>'
)

# Replace Timeline routes
# Leg 1:
content = content.replace(
"""                                                        <div class="bp-tl-route">
                                                            <div class="city">DEL</div>
                                                            <div class="icon">✈</div>
                                                            <div class="city">BOM</div>
                                                        </div>""",
"""                                                        <div class="bp-tl-route">
                                                            <div class="city">LKO</div>
                                                            <div class="icon">✈</div>
                                                            <div class="city">DEL</div>
                                                        </div>"""
)

# Leg 2:
content = content.replace(
"""                                                        <div class="bp-tl-route">
                                                            <div class="city">BOM</div>
                                                            <div class="icon">✈</div>
                                                            <div class="city">GOI</div>
                                                        </div>""",
"""                                                        <div class="bp-tl-route">
                                                            <div class="city">DEL</div>
                                                            <div class="icon">✈</div>
                                                            <div class="city">AMS</div>
                                                        </div>"""
)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated cities.")
