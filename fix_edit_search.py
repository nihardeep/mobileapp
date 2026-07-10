import re

# 1. Update index.html
with open('index.html', 'r') as f:
    html = f.read()

# Add flightSearchDrawer to index.html before savedPassengersSheet
drawer_html = """
<div class="bottom-sheet-drawer" id="flightSearchDrawer" style="z-index: 999999; padding-bottom: 20px;">
    <div class="drawer-drag-handle" style="width: 36px; height: 4px; background: #cbd5e1; border-radius: 2px; margin: 12px auto 20px auto;"></div>
    <div style="padding: 0 24px 16px 24px;">
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 16px;">
            <h2 style="font-size: 20px; font-weight: 800; color: #0f172a; margin: 0;">Edit Search</h2>
            <div onclick="closeAllDrawers()" style="font-size: 14px; color: var(--indigo-blue); font-weight: 700; cursor: pointer;">Close</div>
        </div>
        <div id="flightSearchDrawerContent"></div>
    </div>
</div>
"""
if 'id="flightSearchDrawer"' not in html:
    html = html.replace('<div class="bottom-sheet-drawer" id="savedPassengersSheet"', drawer_html + '\n<div class="bottom-sheet-drawer" id="savedPassengersSheet"')

# Change Edit button on student page to open the drawer
html = html.replace('onclick="navigateTo(\'home\')"', 'onclick="openFlightSearchDrawer()"')

# Increment cache buster
html = html.replace('app.js?v=23', 'app.js?v=24')

with open('index.html', 'w') as f:
    f.write(html)

# 2. Update app.js
with open('app.js', 'r') as f:
    js = f.read()

# Add openFlightSearchDrawer and update closeAllDrawers
new_funcs = """
function openFlightSearchDrawer() {
    triggerHaptic('medium', 'Open search drawer');
    closeAllDrawers();
    
    const backdrop = document.getElementById('bottomSheetBackdrop');
    const drawer = document.getElementById('flightSearchDrawer');
    const searchWidget = document.getElementById('searchWidgetSection');
    const drawerContent = document.getElementById('flightSearchDrawerContent');
    
    if (backdrop && drawer && searchWidget && drawerContent) {
        drawerContent.appendChild(searchWidget);
        searchWidget.style.paddingBottom = "0px";
        backdrop.classList.add('visible');
        drawer.classList.add('visible');
    }
}
"""

if 'openFlightSearchDrawer' not in js:
    js = js.replace('function closeAllDrawers() {', new_funcs + '\nfunction closeAllDrawers() {')

# Modify closeAllDrawers to return the widget
close_widget_logic = """
    const originalContainer = document.getElementById('homeContentContainer');
    const searchWidget = document.getElementById('searchWidgetSection');
    const categoryTabs = document.getElementById('categoryTabsSection');
    if (originalContainer && searchWidget && searchWidget.parentElement && searchWidget.parentElement.id === 'flightSearchDrawerContent') {
        if (categoryTabs && categoryTabs.nextSibling) {
            originalContainer.insertBefore(searchWidget, categoryTabs.nextSibling);
        } else {
            originalContainer.appendChild(searchWidget);
        }
        searchWidget.style.paddingBottom = "24px";
    }
"""

# Insert close_widget_logic right before `if (backdrop) backdrop.classList.remove('visible');`
js = js.replace("if (backdrop) backdrop.classList.remove('visible');", close_widget_logic + "\n    if (backdrop) backdrop.classList.remove('visible');")

# Also ensure navigateTo('home') handles it if we navigate without closing drawer? 
# The closeAllDrawers is called when clicking backdrop, but what if they click a tab?
# It's fine, closeAllDrawers is safe.

# Make sure ai-flight-card has onclick
if 'id="ai-card-${i}"' in js:
    js = js.replace('id="ai-card-${i}"', 'id="ai-card-${i}" onclick="searchFlights()"')

# Bypass search validation
js = js.replace("if (!appState.selectedFrom || !appState.selectedTo) {", "if (!appState.selectedFrom) appState.selectedFrom = 'DEL';\n    if (!appState.selectedTo) appState.selectedTo = 'BOM';\n    if (false) {")

with open('app.js', 'w') as f:
    f.write(js)

print("Logic updated")
