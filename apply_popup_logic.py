import re

with open('app.js', 'r') as f:
    js = f.read()

# Remove toggleInlineFare logic
start_idx = js.find('window.toggleInlineFare = function')
if start_idx != -1:
    end_idx = js.find('window.closeCompareModal = function')
    end_idx = js.find('};', end_idx) + 2
    js = js[:start_idx] + js[end_idx:]

new_logic = """
window.openFarePopup = function(event, className, basePrice, flNum, depTime, arrTime, depAir, arrAir, dur) {
    if (event) event.stopPropagation();
    
    window.currentBaseFare = parseInt(basePrice.toString().replace(/,/g, ''));
    window.currentPopupClass = className;
    
    // Set Header Info
    document.getElementById('cp-flight-num').innerText = flNum || '6E 1234';
    document.getElementById('cp-dur').innerText = dur || '2h 15m';
    document.getElementById('cp-dep-time').innerText = depTime || '05:15';
    document.getElementById('cp-arr-time').innerText = arrTime || '07:30';
    document.getElementById('cp-dep-air').innerText = depAir || 'DEL, T1';
    document.getElementById('cp-arr-air').innerText = arrAir || 'BOM, T2';

    // Switch Tab & Render Cards
    switchPopupTab(className);
    
    const popup = document.getElementById('fareCenteredPopup');
    if (popup) {
        popup.classList.add('active');
        if (typeof triggerHaptic === 'function') triggerHaptic('medium', 'Fare popup opened');
        
        // Reset scroll position
        setTimeout(() => {
            const container = document.getElementById('cp-carousel');
            if (container) {
                // Scroll to center card initially
                const cards = container.querySelectorAll('.cp-3d-card');
                if (cards.length > 1) {
                    const centerCard = className === 'Economy' ? cards[1] : cards[0]; // Flexi is index 1, Stretch is 0
                    container.scrollLeft = centerCard.offsetLeft - (container.offsetWidth / 2) + (centerCard.offsetWidth / 2);
                }
                handleCarouselScroll();
            }
        }, 50);
    }
};

window.switchPopupTab = function(className) {
    document.getElementById('cp-seg-stretch').classList.remove('active');
    document.getElementById('cp-seg-economy').classList.remove('active');
    
    if (className === 'Stretch') {
        document.getElementById('cp-seg-stretch').classList.add('active');
    } else {
        document.getElementById('cp-seg-economy').classList.add('active');
    }
    
    window.currentPopupClass = className;
    const options = window.fareOptions[className] || window.fareOptions['Economy'];
    renderPopupCards(options, className);
};

window.renderPopupCards = function(options, className) {
    const track = document.getElementById('cp-track');
    let html = '';
    
    options.forEach((opt, idx) => {
        let popularHtml = '';
        if (opt.isPopular) {
            popularHtml = `<div class="cp-popular-badge ${opt.badgeClass || ''}">Popular fare</div>`;
        }
        
        let featuresHtml = '';
        opt.features.forEach(f => {
            if (f.type === 'text-only') {
                featuresHtml += `<div class="cp-feature-item" style="justify-content: ${f.align || 'flex-start'}; margin-bottom: 12px; font-weight:700;">${f.text}</div>`;
            } else {
                const iconSvg = svgIcons[f.icon] || '';
                const itemClass = `cp-feature-item ${f.type === 'cross' ? 'cross' : 'highlighted'}`;
                featuresHtml += `<div class="${itemClass}">${iconSvg} <span>${f.text}</span></div>`;
            }
        });
        
        const totalFare = window.currentBaseFare + opt.priceAdd;
        
        html += `
            <div class="cp-3d-card ${className === 'Stretch' ? 'stretch-mode' : ''}" data-fare="${totalFare}" data-id="${opt.id}">
                <div class="cp-card-header">${opt.name}</div>
                ${popularHtml}
                <div class="cp-card-features">
                    ${featuresHtml}
                </div>
                <div class="cp-pricing-block">
                    <div style="font-size: 10px; color: #999;">Starting from</div>
                    <div style="font-size: 16px; font-weight: 800; color: #000;">₹ ${totalFare.toLocaleString('en-IN')}<span style="font-size:11px; font-weight:400; color:#666;">/ Pax</span></div>
                    <div style="font-size: 9px; color: var(--indigo-blue); font-weight: 700; margin-top: 8px;">Know More <svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-1px;"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg></div>
                </div>
            </div>
        `;
    });
    
    track.innerHTML = html;
};

window.handleCarouselScroll = function() {
    const container = document.getElementById('cp-carousel');
    if (!container) return;
    
    const cards = container.querySelectorAll('.cp-3d-card');
    const containerCenter = container.scrollLeft + (container.offsetWidth / 2);
    
    let closestCard = null;
    let minDistance = Infinity;
    
    cards.forEach(card => {
        const cardCenter = card.offsetLeft + (card.offsetWidth / 2);
        const distance = Math.abs(containerCenter - cardCenter);
        
        // Remove active class
        card.classList.remove('active-center');
        
        if (distance < minDistance) {
            minDistance = distance;
            closestCard = card;
        }
    });
    
    if (closestCard) {
        closestCard.classList.add('active-center');
        
        // Update total fare based on the centered card
        const fare = closestCard.getAttribute('data-fare');
        if (fare) {
            document.getElementById('cp-total-fare').innerText = '₹ ' + parseInt(fare).toLocaleString('en-IN');
        }
    }
};

window.closeFarePopup = function() {
    const popup = document.getElementById('fareCenteredPopup');
    if (popup) popup.classList.remove('active');
};

window.openCompareFaresModal = function(event, className) {
    if (event) event.stopPropagation();
    
    const modal = document.getElementById('compareFaresModal');
    const tableContainer = document.getElementById('compareTableContainer');
    if (!modal || !tableContainer) return;
    
    let tableHtml = '';
    
    if (className === 'Economy') {
        tableHtml = `
            <table class="compare-table">
                <thead>
                    <tr>
                        <th>Feature</th>
                        <th>Saver</th>
                        <th class="compare-highlight">Flexi (Popular)</th>
                        <th>Upfront</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="feature-name">Cabin Baggage</td>
                        <td>7 kg</td>
                        <td class="compare-highlight">7 kg</td>
                        <td>7 kg</td>
                    </tr>
                    <tr>
                        <td class="feature-name">Check-in Baggage</td>
                        <td>15 kg</td>
                        <td class="compare-highlight">15 kg</td>
                        <td>15 kg</td>
                    </tr>
                    <tr>
                        <td class="feature-name">Meals</td>
                        <td>❌</td>
                        <td class="compare-highlight">✔️ Free Meal (Extra)</td>
                        <td>❌</td>
                    </tr>
                    <tr>
                        <td class="feature-name">Seat Selection</td>
                        <td>Paid</td>
                        <td class="compare-highlight">✔️ Free Standard Seat (Extra)</td>
                        <td>Paid</td>
                    </tr>
                    <tr>
                        <td class="feature-name">Date Change</td>
                        <td>Paid</td>
                        <td class="compare-highlight">✔️ Free Date Change (Extra)</td>
                        <td>Paid</td>
                    </tr>
                    <tr>
                        <td class="feature-name">Cancellation</td>
                        <td>Standard Fee</td>
                        <td class="compare-highlight">✔️ Free Cancellation (Extra)</td>
                        <td>Standard Fee</td>
                    </tr>
                </tbody>
            </table>
        `;
    } else {
        tableHtml = `
            <table class="compare-table">
                <thead>
                    <tr>
                        <th>Feature</th>
                        <th>Stretch</th>
                        <th class="compare-highlight" style="color: #D4AF37;">Stretch+ (Popular)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="feature-name">Leg Room</td>
                        <td>Extra</td>
                        <td class="compare-highlight">Extra</td>
                    </tr>
                    <tr>
                        <td class="feature-name">Meals</td>
                        <td>❌</td>
                        <td class="compare-highlight">✔️ Free Veg Meal (Extra)</td>
                    </tr>
                    <tr>
                        <td class="feature-name">Seat Selection</td>
                        <td>❌</td>
                        <td class="compare-highlight">✔️ Free Premium Seat (Extra)</td>
                    </tr>
                    <tr>
                        <td class="feature-name">Plan Change</td>
                        <td>Paid</td>
                        <td class="compare-highlight">✔️ Free Plan Change (Extra)</td>
                    </tr>
                </tbody>
            </table>
        `;
    }
    
    tableContainer.innerHTML = tableHtml;
    modal.classList.add('active');
};

window.closeCompareModal = function() {
    const modal = document.getElementById('compareFaresModal');
    if (modal) modal.classList.remove('active');
};
"""

js += '\n' + new_logic

# Change the onclicks in app.js
js = js.replace(r"toggleInlineFare(event, '${i}', 'Economy', '${f.price}')", 
                r"openFarePopup(event, 'Economy', '${f.price}', '${f.id}', '${f.from}', '${f.to}', 'DEL, T1', 'BOM, T2', '${f.dur}')")

js = js.replace(r"toggleInlineFare(event, '${i}', 'Stretch', '${f.stretch || 28000}')", 
                r"openFarePopup(event, 'Stretch', '${f.stretch || 28000}', '${f.id}', '${f.from}', '${f.to}', 'DEL, T1', 'BOM, T2', '${f.dur}')")

js = js.replace(r"toggleInlineFare(event, 'rec', 'Economy', '${oldP}')", 
                r"openFarePopup(event, 'Economy', '${oldP}', '6E 5678', '06:30', '10:45', 'DEL, T1', 'BOM, T2', '4h 15m')")


# Remove inline containers from app.js
js = js.replace(r'<div class="inline-fare-container" id="inline-fare-${i}"></div>', '')
js = js.replace(r'<div class="inline-fare-container" id="inline-fare-rec"></div>', '')


with open('app.js', 'w') as f:
    f.write(js)

print("Updated app.js logic")

# 3. Update index.html
with open('index.html', 'r') as f:
    html = f.read()

# Add Centered Popup Modal
popup_modal = """
                <!-- Centered Popup Overlay -->
                <div class="centered-popup-overlay" id="fareCenteredPopup">
                    <div class="centered-popup-content">
                        <!-- Header -->
                        <div style="padding: 16px 20px 12px; text-align: center; border-bottom: 1px solid rgba(0,0,0,0.05); position: relative;">
                            <div onclick="closeFarePopup()" style="position: absolute; right: 16px; top: 16px; cursor: pointer; color: #999;"><svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div>
                            <div style="font-size: 11px; color: #666; margin-bottom: 8px;"><svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor" style="vertical-align: -2px;"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg> <span id="cp-flight-num">6E 1234</span></div>
                            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0 10%;">
                                <div style="text-align: center;">
                                    <div style="font-size: 16px; font-weight: 800; color: #000;" id="cp-dep-time">05:00</div>
                                    <div style="font-size: 10px; color: #666;" id="cp-dep-air">DEL, T3</div>
                                </div>
                                <div style="flex: 1; padding: 0 12px; position: relative; text-align: center;">
                                    <div style="border-top: 1px dashed #ccc; width: 100%; position: absolute; top: 50%; left: 0; transform: translateY(-50%); z-index: 1;"></div>
                                    <div style="background: white; position: relative; display: inline-block; padding: 0 8px; font-size: 10px; color: var(--indigo-blue); font-weight: 700; z-index: 2;" id="cp-dur">3h 10m</div>
                                </div>
                                <div style="text-align: center;">
                                    <div style="font-size: 16px; font-weight: 800; color: #000;" id="cp-arr-time">08:10</div>
                                    <div style="font-size: 10px; color: #666;" id="cp-arr-air">BOM, T2</div>
                                </div>
                            </div>
                        </div>

                        <!-- Segmented Control -->
                        <div style="padding: 16px;">
                            <div class="cp-segment-control">
                                <div class="cp-segment" id="cp-seg-stretch" onclick="switchPopupTab('Stretch')">Stretch</div>
                                <div class="cp-segment active" id="cp-seg-economy" onclick="switchPopupTab('Economy')">Economy</div>
                            </div>
                        </div>

                        <!-- 3D Carousel Container -->
                        <div class="cp-carousel-container" id="cp-carousel" onscroll="handleCarouselScroll()">
                            <div class="cp-carousel-padder"></div>
                            <div class="cp-carousel-track" id="cp-track">
                                <!-- Cards injected here -->
                            </div>
                            <div class="cp-carousel-padder"></div>
                        </div>

                        <!-- Compare Fares Link -->
                        <div style="text-align: center; margin-bottom: 16px;">
                            <span class="cp-compare-link" onclick="openCompareFaresModal(event, window.currentPopupClass)">Compare Fares <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -1px;"><line x1="18" y1="6" x2="6" y2="18"/><polyline points="6 6 18 6 18 18"/></svg></span>
                        </div>

                        <!-- Sticky Action Footer -->
                        <div class="cp-sticky-footer">
                            <div style="flex: 1; text-align: left;">
                                <div style="font-size: 10px; font-weight: 700; color: #666; text-transform: uppercase;">Total Fare</div>
                                <div style="font-size: 20px; font-weight: 800; color: #000;" id="cp-total-fare">₹ 6,182</div>
                            </div>
                            <button class="primary-btn" style="padding: 12px 24px; border-radius: 8px; font-size: 14px;" onclick="closeFarePopup()">Next</button>
                        </div>
                    </div>
                </div>
"""

if 'id="fareCenteredPopup"' not in html:
    html = html.replace('<!-- Compare Fares Modal -->', popup_modal + '\n                <!-- Compare Fares Modal -->')

# Modify hardcoded flight cards to use openFarePopup
for i in range(1, 11):
    html = html.replace(f"toggleInlineFare(event, 'hc{i}', 'Economy', '4800')",
                        f"openFarePopup(event, 'Economy', '4800', '6E 1234', '05:15', '07:30', 'DEL, T1', 'BOM, T2', '2h 15m')")
    html = html.replace(f"toggleInlineFare(event, 'hc{i}', 'Stretch', '28000')",
                        f"openFarePopup(event, 'Stretch', '28000', '6E 1234', '05:15', '07:30', 'DEL, T1', 'BOM, T2', '2h 15m')")

# Remove hardcoded inline containers
html = re.sub(r'<div class="inline-fare-container" id="inline-fare-hc\d+"></div>', '', html)

with open('index.html', 'w') as f:
    f.write(html)

print("Updated index.html")
