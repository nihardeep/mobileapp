import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove from trips screen
demo_panel_html = """                        <!-- Demo Control Panel -->
                        <div class="bp-demo-panel">
                            <button class="bp-demo-btn active" id="btnBPSingle" onclick="setBPState('single')">Single City</button>
                            <button class="bp-demo-btn" id="btnBPMulti" onclick="setBPState('multi')">Multi-City</button>
                            <button class="bp-demo-btn" id="btnBPDone" onclick="setBPState('completed')">Leg 1 Done</button>
                        </div>"""
content = content.replace(demo_panel_html, "")

# 2. Insert into developer console
# Find: <div class="dev-state-label">Atmosphere & Sound overrides</div>
# and insert BEFORE the parent .dev-state-group
dev_insert_html = """            <div class="dev-state-group">
                <div class="dev-state-label">Digital Boarding Pass states</div>
                <div class="dev-btn-stack">
                    <button class="dev-trigger-btn active" id="btnBPSingle" onclick="setBPState('single')">
                        🎫 Single City Pass
                        <div class="dev-btn-indicator"></div>
                    </button>
                    <button class="dev-trigger-btn" id="btnBPMulti" onclick="setBPState('multi')">
                        🎟️ Multi-City (Connecting)
                        <div class="dev-btn-indicator"></div>
                    </button>
                    <button class="dev-trigger-btn" id="btnBPDone" onclick="setBPState('completed')">
                        ✅ Leg 1 Completed
                        <div class="dev-btn-indicator"></div>
                    </button>
                </div>
            </div>

            <div class="dev-state-group">
                <div class="dev-state-label">Atmosphere & Sound overrides</div>"""

content = content.replace("""            <div class="dev-state-group">
                <div class="dev-state-label">Atmosphere & Sound overrides</div>""", dev_insert_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Fix script.js logic which modifies .bp-demo-btn classes.
with open('script.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

js_content = js_content.replace(".bp-demo-btn", ".dev-trigger-btn")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Toggles moved to dev console.")
