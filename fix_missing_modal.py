import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

modal_html = """
                        <!-- Full Screen QR Modal -->
                        <div id="bpQrFullscreen" class="bp-qr-fullscreen" style="display: none;">
                            <div class="bp-qr-modal-content">
                                <div class="bp-qr-close" onclick="closeQRModal()">✕</div>
                                <div class="bp-qr-modal-title">Ready to Scan</div>
                                <img src="qr_code.png" class="bp-qr-modal-img" />
                                <div class="bp-qr-modal-subtitle" id="bpQrModalSubtitle">SEC. 6E2341:001 (LEG 1)</div>
                            </div>
                        </div>
"""

insert_point = html.find('<!-- Bottom Navigation Bar -->')
if insert_point != -1:
    html = html[:insert_point] + modal_html + '\n                ' + html[insert_point:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Modal successfully injected.")
else:
    print("Could not find insert point!")
