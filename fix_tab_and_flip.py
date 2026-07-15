import re

# 1. Update style.css
with open('style.css', 'a', encoding='utf-8') as f:
    f.write("""
/* Update Toggle for Dark Theme */
.bp-leg-toggle {
    background: rgba(255,255,255,0.1) !important;
    border-radius: 20px !important;
    padding: 6px !important;
}
.bp-toggle-btn {
    color: rgba(255,255,255,0.7) !important;
    border-radius: 16px !important;
}
.bp-toggle-btn.active {
    background: #fff !important; 
    color: #020b1f !important;
}

/* Flip Animation */
@keyframes flip-ticket {
    0% { transform: rotateY(0deg); opacity: 1; }
    50% { transform: rotateY(90deg); opacity: 0; }
    100% { transform: rotateY(0deg); opacity: 1; }
}
.bp-ticket-card.animate-flip {
    animation: flip-ticket 0.6s ease-in-out;
}
""")

# 2. Strip inline styles from index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('style="color: white; border: 1px solid rgba(255,255,255,0.4); padding: 8px 16px; border-radius: 20px; font-size: 12px; font-weight: 600;"', '')
html = html.replace('style="margin-top: 24px; display: flex; justify-content: center; gap: 16px;"', 'style="margin-top: 24px;"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 3. Update app.js
with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# We need to wrap the text update inside setTimeout
import re

old_flip = """window.flipToLeg = function(legNum) {
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
        city1NameEls.forEach(el => el.innerText = 'DELHI');
        city1CodeEls.forEach(el => el.innerText = 'DEL');
        city2NameEls.forEach(el => el.innerText = 'MUMBAI');
        city2CodeEls.forEach(el => el.innerText = 'BOM');
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
    const cards = document.querySelectorAll('.bp-ticket-card');

    // Trigger flip animation
    cards.forEach(card => {
        card.classList.remove('animate-flip');
        void card.offsetWidth; // trigger reflow
        card.classList.add('animate-flip');
    });

    if (legNum === 1) {
        toggles1.forEach(t => t.classList.add('active'));
        toggles2.forEach(t => t.classList.remove('active'));
        triggerHaptic('light', 'Switched to Leg 1');
        
        setTimeout(() => {
            city1NameEls.forEach(el => el.innerText = 'DELHI');
            city1CodeEls.forEach(el => el.innerText = 'DEL');
            city2NameEls.forEach(el => el.innerText = 'MUMBAI');
            city2CodeEls.forEach(el => el.innerText = 'BOM');
            flightEls.forEach(el => el.innerText = '6E 2341');
            boardingTimeEls.forEach(el => el.innerText = '22:00');
            gateEls.forEach(el => el.innerText = '5B / L1');
            zoneEls.forEach(el => el.innerText = '02');
            dateEls.forEach(el => el.innerText = '25 MAR 2026');
            seatEls.forEach(el => {
                if(el.innerText === '8F') el.innerText = '12C';
            });
            if(document.getElementById('bpQrModalSubtitle')) document.getElementById('bpQrModalSubtitle').innerText = 'SEC. 6E2341:001 (LEG 1)';
        }, 300);
    } else {
        toggles1.forEach(t => t.classList.remove('active'));
        toggles2.forEach(t => t.classList.add('active'));
        triggerHaptic('light', 'Switched to Leg 2');
        
        setTimeout(() => {
            city1NameEls.forEach(el => el.innerText = 'MUMBAI');
            city1CodeEls.forEach(el => el.innerText = 'BOM');
            city2NameEls.forEach(el => el.innerText = 'GOA');
            city2CodeEls.forEach(el => el.innerText = 'GOI');
            flightEls.forEach(el => el.innerText = '6E 7892');
            boardingTimeEls.forEach(el => el.innerText = '05:45');
            gateEls.forEach(el => el.innerText = '2A / L2');
            zoneEls.forEach(el => el.innerText = '01');
            dateEls.forEach(el => el.innerText = '26 MAR 2026');
            seatEls.forEach(el => el.innerText = '8F');
            if(document.getElementById('bpQrModalSubtitle')) document.getElementById('bpQrModalSubtitle').innerText = 'SEC. 6E7892:002 (LEG 2)';
        }, 300);
    }
}"""

if old_flip in app_js:
    app_js = app_js.replace(old_flip, new_flip)
else:
    print("WARNING: Could not find old_flip logic in app.js")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("Done patching.")
