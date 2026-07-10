import re

with open('index.html', 'r') as f:
    html = f.read()

compare_modal = """
                <!-- Compare Fares Modal -->
                <div class="compare-modal-overlay" id="compareFaresModal">
                    <div class="compare-modal-content">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <h2 style="font-size: 20px; font-weight: 800; color: #000; margin: 0;">Compare Fares</h2>
                            <div onclick="closeCompareModal()" style="padding: 8px; cursor: pointer; background: #F5F5F5; border-radius: 50%;"><svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></div>
                        </div>
                        <p style="font-size: 13px; color: #666; margin: 0 0 16px 0; line-height: 1.4;">See what you get extra with popular fares compared to standard options.</p>
                        <div id="compareTableContainer"></div>
                    </div>
                </div>
"""

if 'id="compareFaresModal"' not in html:
    html = html.replace('<div class="bottom-sheet-backdrop" id="bottomSheetBackdrop"', compare_modal + '\n                <div class="bottom-sheet-backdrop" id="bottomSheetBackdrop"')
    with open('index.html', 'w') as f:
        f.write(html)
    print("Injected modal")
else:
    print("Modal already present")
