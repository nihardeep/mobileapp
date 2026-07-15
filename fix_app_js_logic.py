js_code = """

// ==========================================================================
// TIMELINE BOARDING PASS LOGIC
// ==========================================================================

window.flipToLeg = function(legNum) {
    const flipper = document.getElementById('bpQrFlipper');
    const slider = document.getElementById('bpTimelineSlider');
    const btn1 = document.getElementById('btnLeg1');
    const btn2 = document.getElementById('btnLeg2');
    
    if (legNum === 1) {
        if(flipper) flipper.classList.remove('flipped');
        if(slider) slider.style.transform = 'translateX(0%)';
        if(btn1) btn1.classList.add('active');
        if(btn2) btn2.classList.remove('active');
        if(document.getElementById('bpQrModalSubtitle')) document.getElementById('bpQrModalSubtitle').innerText = 'SEC. 6E2341:001 (LEG 1)';
        triggerHaptic('light', 'Switched to Leg 1');
    } else {
        if(flipper) flipper.classList.add('flipped');
        if(slider) slider.style.transform = 'translateX(-50%)';
        if(btn1) btn1.classList.remove('active');
        if(btn2) btn2.classList.add('active');
        if(document.getElementById('bpQrModalSubtitle')) document.getElementById('bpQrModalSubtitle').innerText = 'SEC. 6E7892:002 (LEG 2)';
        triggerHaptic('light', 'Switched to Leg 2');
    }
}

window.openQRModal = function() {
    if(document.getElementById('bpQrFullscreen')) document.getElementById('bpQrFullscreen').style.display = 'flex';
    triggerHaptic('medium', 'QR Modal Opened');
}

window.closeQRModal = function() {
    if(document.getElementById('bpQrFullscreen')) document.getElementById('bpQrFullscreen').style.display = 'none';
}

// Override the demo state toggles to handle the new timeline structure
window.setBPState = function(state) {
    document.getElementById('btnBPSingle').classList.remove('active');
    document.getElementById('btnBPMulti').classList.remove('active');
    document.getElementById('btnBPDone').classList.remove('active');
    
    const toggles = document.querySelectorAll('.bp-leg-toggle');
    const slider = document.getElementById('bpTimelineSlider');
    
    if (state === 'single') {
        document.getElementById('btnBPSingle').classList.add('active');
        toggles.forEach(t => t.style.display = 'none');
        if(slider) slider.style.width = '100%';
        flipToLeg(1);
    } else if (state === 'multi') {
        document.getElementById('btnBPMulti').classList.add('active');
        toggles.forEach(t => t.style.display = 'flex');
        if(slider) slider.style.width = '200%';
        flipToLeg(1);
    } else if (state === 'completed') {
        document.getElementById('btnBPDone').classList.add('active');
        toggles.forEach(t => t.style.display = 'flex');
        if(slider) slider.style.width = '200%';
        flipToLeg(2);
    }
}
"""

with open('app.js', 'a', encoding='utf-8') as f:
    f.write(js_code)

print("Logic appended to app.js")
