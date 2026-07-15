import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Replace flipToLeg
old_flip = """window.flipToLeg = function(legNum) {
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
        if(slider) slider.style.transform = 'translateX(-100%)';
        if(btn1) btn1.classList.remove('active');
        if(btn2) btn2.classList.add('active');
        if(document.getElementById('bpQrModalSubtitle')) document.getElementById('bpQrModalSubtitle').innerText = 'SEC. 6E7892:002 (LEG 2)';
        triggerHaptic('light', 'Switched to Leg 2');
    }
}"""

new_flip = """window.flipToLeg = function(legNum) {
    // Find all toggles and sync them
    const toggles1 = document.querySelectorAll('.bp-toggle-btn:first-child');
    const toggles2 = document.querySelectorAll('.bp-toggle-btn:last-child');
    
    const flightEls = document.querySelectorAll('#tkFlight');
    const city1NameEls = document.querySelectorAll('#tkCity1Name');
    const city1CodeEls = document.querySelectorAll('#tkCity1Code');
    const city2NameEls = document.querySelectorAll('#tkCity2Name');
    const city2CodeEls = document.querySelectorAll('#tkCity2Code');
    const boardingTimeEls = document.querySelectorAll('#tkBoardingTime');
    const gateEls = document.querySelectorAll('#tkGate');
    const zoneEls = document.querySelectorAll('#tkZone');
    const dateEls = document.querySelectorAll('#tkDate');
    const seqEls = document.querySelectorAll('#tkSeq');
    const seatEls = document.querySelectorAll('#tkSeat');
    
    if (legNum === 1) {
        toggles1.forEach(t => t.classList.add('active'));
        toggles2.forEach(t => t.classList.remove('active'));
        
        // Leg 1 Data: LKO -> DEL
        city1NameEls.forEach(el => el.innerText = 'LUCKNOW');
        city1CodeEls.forEach(el => el.innerText = 'LKO');
        city2NameEls.forEach(el => el.innerText = 'NEW DELHI');
        city2CodeEls.forEach(el => el.innerText = 'DEL');
        flightEls.forEach(el => el.innerText = '6E 2341');
        boardingTimeEls.forEach(el => el.innerText = '22:00');
        gateEls.forEach(el => el.innerText = '5B / L1');
        zoneEls.forEach(el => el.innerText = '02');
        dateEls.forEach(el => el.innerText = '25 MAR 2026');
        // Seat logic: keep as is for 12C, 12D etc. 
        seatEls.forEach(el => {
            if(el.innerText === '8F') el.innerText = '12C';
        });
        
        if(document.getElementById('bpQrModalSubtitle')) document.getElementById('bpQrModalSubtitle').innerText = 'SEC. 6E2341:001 (LEG 1)';
        triggerHaptic('light', 'Switched to Leg 1');
    } else {
        toggles1.forEach(t => t.classList.remove('active'));
        toggles2.forEach(t => t.classList.add('active'));
        
        // Leg 2 Data: DEL -> AMS (or GOA based on Indigo pass)
        // Let's use MUMBAI -> GOA as per the Indigo pass since it's the second leg
        city1NameEls.forEach(el => el.innerText = 'MUMBAI');
        city1CodeEls.forEach(el => el.innerText = 'BOM');
        city2NameEls.forEach(el => el.innerText = 'GOA');
        city2CodeEls.forEach(el => el.innerText = 'GOI');
        flightEls.forEach(el => el.innerText = '6E 7892');
        boardingTimeEls.forEach(el => el.innerText = '05:45');
        gateEls.forEach(el => el.innerText = '2A / L2');
        zoneEls.forEach(el => el.innerText = '01');
        dateEls.forEach(el => el.innerText = '26 MAR 2026');
        
        // Seat logic: change to 8F
        seatEls.forEach(el => el.innerText = '8F');
        
        if(document.getElementById('bpQrModalSubtitle')) document.getElementById('bpQrModalSubtitle').innerText = 'SEC. 6E7892:002 (LEG 2)';
        triggerHaptic('light', 'Switched to Leg 2');
    }
}"""

if old_flip in app_js:
    app_js = app_js.replace(old_flip, new_flip)
else:
    print("Could not find old_flip")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("App JS Updated")
