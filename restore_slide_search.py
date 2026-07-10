import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_search_ui = """
    <!-- Slide Out Search UI -->
    <div id="slideOutSearch" style="position: absolute; top: 20px; right: 0; z-index: 50; display: flex; align-items: flex-start; transform: translateX(calc(100% - 28px)); transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);">
        <!-- Vertical Tab -->
        <div style="background: #1f2937; color: #fff; padding: 12px 6px; border-radius: 8px 0 0 8px; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: -2px 0 8px rgba(0,0,0,0.15);" onclick="document.getElementById('slideOutSearch').style.transform = 'translateX(0)'">
            <div style="writing-mode: vertical-rl; transform: rotate(180deg); font-size: 12px; font-weight: 600; letter-spacing: 1px;">Search</div>
        </div>
        
        <!-- Search Box -->
        <div style="background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(8px); padding: 10px; border-radius: 0 0 0 12px; width: 240px; box-shadow: -4px 4px 16px rgba(0,0,0,0.1); border-bottom: 1px solid #e2e8f0; border-left: 1px solid #e2e8f0; display: flex; flex-direction: column;">
            <div style="display: flex; align-items: center; background: #f1f5f9; border-radius: 8px; padding: 4px 8px;">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#64748b" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                <input type="text" id="mapSearchInput" placeholder="Find city..." style="border: none; background: transparent; padding: 8px; font-size: 14px; font-weight: 600; color: #0f172a; width: 100%; outline: none;" onkeyup="handleMapSearch(this.value)">
                <svg onclick="document.getElementById('slideOutSearch').style.transform = 'translateX(calc(100% - 28px))'" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#64748b" stroke-width="2" style="cursor: pointer; margin-left: 4px; padding: 2px;"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </div>
            <!-- Autocomplete Results -->
            <div id="mapSearchResults" style="margin-top: 8px; max-height: 160px; overflow-y: auto; display: none;"></div>
        </div>
    </div>
"""

target = '<div class="globe-map-container">'
if target in content:
    content = content.replace(target, target + new_search_ui)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully restored the Slide Out Search UI!")
else:
    print("Could not find globe-map-container!")

