import re

# 1. Update index.html
with open('index.html', 'r') as f:
    html = f.read()

drawer_html = """
                <!-- Fare Selection Drawer -->
                <div class="bottom-sheet-drawer" id="fareSelectionDrawer" style="padding-bottom: 0; display: flex; flex-direction: column; max-height: 90vh;">
                    <div class="drawer-drag-handle" style="width: 36px; height: 4px; background: #E0E0E0; border-radius: 2px; margin: 12px auto 16px auto; flex-shrink: 0;"></div>
                    
                    <!-- Drawer Header (Flight Info) -->
                    <div style="padding: 0 20px 16px 20px; text-align: center; border-bottom: 1px solid rgba(0,0,0,0.05); flex-shrink: 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <div style="font-size: 11px; color: #666; display: flex; align-items: center; gap: 4px;"><svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg> <span id="fsd-flight-number">6E 12347</span></div>
                            <div style="font-size: 11px; color: #666;" id="fsd-duration">3h 10m</div>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <div style="text-align: left;">
                                <div style="font-size: 20px; font-weight: 800; color: #000;" id="fsd-dep-time">05:00</div>
                                <div style="font-size: 12px; color: #666;" id="fsd-dep-airport">DEL, T3</div>
                            </div>
                            <div style="flex: 1; padding: 0 16px; position: relative;">
                                <div style="border-top: 1px dashed #ccc; width: 100%; position: absolute; top: 50%; left: 0; transform: translateY(-50%);"></div>
                                <div style="background: white; position: relative; display: inline-block; padding: 0 8px; font-size: 10px; color: var(--indigo-blue); font-weight: 700;">Non-stop</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 20px; font-weight: 800; color: #000;" id="fsd-arr-time">08:10</div>
                                <div style="font-size: 12px; color: #666;" id="fsd-arr-airport">BOM, T2</div>
                            </div>
                        </div>
                        <div style="color: var(--indigo-blue); font-size: 12px; font-weight: 700;">Flight details <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -2px;"><polyline points="9 18 15 12 9 6"></polyline></svg></div>
                    </div>

                    <!-- Segmented Control -->
                    <div style="padding: 16px 20px; flex-shrink: 0;">
                        <div class="fsd-segment-control">
                            <div class="fsd-segment" id="fsd-seg-stretch" onclick="switchFareClass('Stretch')">Stretch</div>
                            <div class="fsd-segment active" id="fsd-seg-economy" onclick="switchFareClass('Economy')">Economy</div>
                        </div>
                    </div>

                    <!-- Fare Cards Scroll Area -->
                    <div class="fsd-cards-scroll-area" id="fsd-cards-container">
                        <!-- Cards will be injected by JS -->
                    </div>

                    <!-- Sticky Footer -->
                    <div class="fsd-sticky-footer">
                        <div style="flex: 1;">
                            <div style="font-size: 10px; font-weight: 700; color: #666; text-transform: uppercase;">Total Fare</div>
                            <div style="font-size: 22px; font-weight: 800; color: #000;" id="fsd-total-fare">₹ 6,182</div>
                            <div style="font-size: 10px; color: #666; margin-top: 2px;">*Convenience fee may apply</div>
                            <div style="font-size: 12px; color: var(--indigo-blue); font-weight: 700; margin-top: 4px;">View Fare Details <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -2px;"><polyline points="9 18 15 12 9 6"></polyline></svg></div>
                        </div>
                        <button class="primary-btn" style="padding: 14px 32px; border-radius: 8px; font-size: 16px; min-width: 120px;" onclick="closeAllDrawers()">Next</button>
                    </div>
                </div>
"""

if 'id="fareSelectionDrawer"' not in html:
    html = html.replace('<!-- Bank Offer Sheet -->', drawer_html + '\n                <!-- Bank Offer Sheet -->')

# Add onclick to price columns in index.html (hardcoded cards)
html = html.replace('<div class="fc-price-col student-fare-active">', '<div class="fc-price-col student-fare-active" onclick="openFareSelectionDrawer(event, \'Economy\', \'4800\', \'6E 1234\', \'05:15\', \'07:30\', \'DEL, T1\', \'BOM, T2\', \'2h 15m\')">')
html = html.replace('<div class="fc-price-col">', '<div class="fc-price-col" onclick="openFareSelectionDrawer(event, \'Stretch\', \'28000\', \'6E 1234\', \'05:15\', \'07:30\', \'DEL, T1\', \'BOM, T2\', \'2h 15m\')">')


with open('index.html', 'w') as f:
    f.write(html)

print("Updated index.html")

# 2. Update app.js
with open('app.js', 'r') as f:
    js = f.read()

js_payload = """
window.fareOptions = {
    'Economy': [
        {
            id: 'saver',
            name: 'Saver',
            isPopular: false,
            priceAdd: 0,
            features: [
                { icon: 'bag', text: '<strong>7 kg</strong> Cabin bag', type: 'tick' },
                { icon: 'luggage', text: '<strong>15 kg</strong> Checkin bag', type: 'tick' },
                { icon: 'seat', text: 'Free Standard Seat', type: 'cross' },
                { icon: 'cancel', text: 'Standard Cancellation', type: 'cross' }
            ]
        },
        {
            id: 'flexi',
            name: 'Flexi',
            isPopular: true,
            badgeClass: '',
            priceAdd: 860,
            features: [
                { icon: 'bag', text: '<strong>7 kg</strong> Cabin bag', type: 'tick' },
                { icon: 'luggage', text: '<strong>15 kg</strong> Checkin bag', type: 'tick' },
                { icon: 'meal', text: '<strong>Free</strong> Meal', type: 'tick' },
                { icon: 'seat', text: '<strong>Free</strong> Standard Seat', type: 'tick' },
                { icon: 'date', text: '<strong>Free</strong> Date Change', type: 'tick' },
                { icon: 'cancel', text: '<strong>Free</strong> Cancellation', type: 'tick' }
            ]
        },
        {
            id: 'upfront',
            name: 'Upfront',
            isPopular: false,
            priceAdd: 1200,
            features: [
                { icon: 'bag', text: '<strong>7 kg</strong> Cabin bag', type: 'tick' },
                { icon: 'luggage', text: '<strong>15 kg</strong> Checkin bag', type: 'tick' },
                { icon: 'meal', text: '<strong>Free</strong> Meal', type: 'cross' },
                { icon: 'seat', text: '<strong>Free</strong> Standard Seat', type: 'cross' },
                { icon: 'cancel', text: 'Standard Cancellation', type: 'cross' }
            ]
        }
    ],
    'Stretch': [
        {
            id: 'stretch-base',
            name: 'Stretch',
            isPopular: false,
            priceAdd: 0,
            features: [
                { text: '<span style="color:#D4AF37; font-weight:700;">Extra Leg Room</span>', type: 'text-only', align: 'center' },
                { icon: 'bag', text: '<strong>12 kg</strong> Cabin bag', type: 'tick' },
                { icon: 'luggage', text: '<strong>40 kg</strong> Checkin bag', type: 'tick' },
                { icon: 'fast', text: 'Fast Forward', type: 'tick' },
                { icon: 'cancel', text: 'Standard Cancellation', type: 'cross' },
                { icon: 'meal', text: 'Free Veg Meal', type: 'cross' },
                { icon: 'seat', text: 'Free Premium Seat', type: 'cross' }
            ]
        },
        {
            id: 'stretch-plus',
            name: 'Stretch+',
            isPopular: true,
            badgeClass: 'stretch-badge',
            priceAdd: 2500,
            features: [
                { text: '<span style="color:#D4AF37; font-weight:700;">Extra Leg Room</span>', type: 'text-only', align: 'center' },
                { icon: 'bag', text: '<strong>12 kg</strong> Cabin bag', type: 'tick' },
                { icon: 'luggage', text: '<strong>40 kg</strong> Checkin bag', type: 'tick' },
                { icon: 'fast', text: 'Fast Forward', type: 'tick' },
                { icon: 'meal', text: '<strong>Free</strong> Veg Meal', type: 'tick' },
                { icon: 'seat', text: '<strong>Free</strong> Premium Seat', type: 'tick' },
                { icon: 'date', text: '<strong>Free</strong> Plan Change', type: 'tick' }
            ]
        }
    ]
};

window.currentBaseFare = 0;
window.currentSelectedFareId = '';

const svgIcons = {
    bag: '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>',
    luggage: '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="8" width="14" height="14" rx="2" ry="2"/><path d="M8 8V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v4"/><line x1="12" y1="12" x2="12" y2="18"/></svg>',
    meal: '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/></svg>',
    seat: '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 18v-4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v4"/><path d="M4 14V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8"/><path d="M2 22h20"/></svg>',
    date: '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    cancel: '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
    fast: '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>'
};

window.openFareSelectionDrawer = function(event, className, basePrice, flNum, depTime, arrTime, depAir, arrAir, dur) {
    if (event) event.stopPropagation();
    
    // Parse the base price
    window.currentBaseFare = parseInt(basePrice.toString().replace(/,/g, ''));
    
    // Set Header Info
    document.getElementById('fsd-flight-number').innerText = flNum || '6E 1234';
    document.getElementById('fsd-duration').innerText = dur || '2h 15m';
    document.getElementById('fsd-dep-time').innerText = depTime || '05:15';
    document.getElementById('fsd-arr-time').innerText = arrTime || '07:30';
    document.getElementById('fsd-dep-airport').innerText = depAir || 'DEL, T1';
    document.getElementById('fsd-arr-airport').innerText = arrAir || 'BOM, T2';

    // Switch the tab
    switchFareClass(className);
    
    const drawer = document.getElementById('fareSelectionDrawer');
    const backdrop = document.getElementById('bottomSheetBackdrop');
    if (drawer && backdrop) {
        drawer.classList.add('visible');
        backdrop.classList.add('visible');
        if (typeof triggerHaptic === 'function') triggerHaptic('medium', 'Fare selection opened');
    }
};

window.switchFareClass = function(className) {
    document.getElementById('fsd-seg-stretch').classList.remove('active');
    document.getElementById('fsd-seg-economy').classList.remove('active');
    
    if (className === 'Stretch') {
        document.getElementById('fsd-seg-stretch').classList.add('active');
    } else {
        document.getElementById('fsd-seg-economy').classList.add('active');
    }
    
    const options = window.fareOptions[className] || window.fareOptions['Economy'];
    
    // Default select Flexi for Economy, Stretch+ for Stretch if they exist
    window.currentSelectedFareId = (className === 'Economy') ? 'flexi' : 'stretch-plus';
    
    renderFareCards(options, className);
};

window.renderFareCards = function(options, className) {
    const container = document.getElementById('fsd-cards-container');
    let html = '';
    
    options.forEach(opt => {
        const isSelected = opt.id === window.currentSelectedFareId;
        const cardClass = `fsd-fare-card ${isSelected ? 'selected' : ''} ${className === 'Stretch' ? 'stretch-card' : ''}`;
        
        let popularHtml = '';
        if (opt.isPopular) {
            popularHtml = `<div class="fsd-popular-badge ${opt.badgeClass || ''}">Popular fare</div>`;
        }
        
        let featuresHtml = '';
        opt.features.forEach(f => {
            if (f.type === 'text-only') {
                featuresHtml += `<div class="fsd-feature-item" style="justify-content: ${f.align || 'flex-start'}; margin-bottom: 16px;">${f.text}</div>`;
            } else {
                const iconSvg = svgIcons[f.icon] || '';
                const itemClass = `fsd-feature-item ${f.type === 'cross' ? 'cross' : 'highlighted'}`;
                featuresHtml += `<div class="${itemClass}">${iconSvg} <span>${f.text}</span></div>`;
            }
        });
        
        const totalFare = window.currentBaseFare + opt.priceAdd;
        
        html += `
            <div class="${cardClass}" onclick="selectFareCard('${opt.id}', ${totalFare}, '${className}')">
                <div class="fsd-fare-header">${opt.name}</div>
                ${popularHtml}
                <div class="fsd-fare-features">
                    ${featuresHtml}
                    
                    <div class="fsd-pricing-block">
                        <div style="font-size: 10px; color: #999;">Starting from</div>
                        <div style="font-size: 18px; font-weight: 800; color: ${className==='Stretch' && isSelected ? '#D4AF37' : 'var(--indigo-blue)'};">₹ ${totalFare.toLocaleString('en-IN')}<span style="font-size:12px; font-weight:400; color:#666;">/ Pax</span></div>
                        <div style="font-size: 10px; color: #4CAF50; margin-top: 4px;">+ Earn 6,200 IndiGo BluChips</div>
                        <div style="font-size: 12px; color: var(--indigo-blue); font-weight: 700; margin-top: 12px; display: inline-flex; align-items: center; gap: 4px;">Know More <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg></div>
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
    
    // Update footer total
    const selectedOpt = options.find(o => o.id === window.currentSelectedFareId) || options[0];
    updateFareFooter(window.currentBaseFare + selectedOpt.priceAdd);
};

window.selectFareCard = function(id, totalFare, className) {
    window.currentSelectedFareId = id;
    if (typeof triggerHaptic === 'function') triggerHaptic('light', 'Fare card selected');
    
    const options = window.fareOptions[className] || window.fareOptions['Economy'];
    renderFareCards(options, className);
};

window.updateFareFooter = function(totalFare) {
    document.getElementById('fsd-total-fare').innerText = '₹ ' + totalFare.toLocaleString('en-IN');
};
"""

if 'window.openFareSelectionDrawer' not in js:
    js += '\n' + js_payload
    
    # Also update dynamic generation inside app.js
    js = js.replace('<div class="${ecoColClass}">', '<div class="${ecoColClass}" onclick="openFareSelectionDrawer(event, \\\'Economy\\\', \\\'${f.price}\\\', \\\'${f.airline} ${f.code}\\\', \\\'${f.depTime}\\\', \\\'${f.arrTime}\\\', \\\'${f.depCode}\\\', \\\'${f.arrCode}\\\', \\\'${f.duration}\\\')">')
    
    js = js.replace('<div class="fc-price-col">\n                <div class="fc-class-name">Stretch', '<div class="fc-price-col" onclick="openFareSelectionDrawer(event, \\\'Stretch\\\', \\\'${f.stretch || 28000}\\\', \\\'${f.airline} ${f.code}\\\', \\\'${f.depTime}\\\', \\\'${f.arrTime}\\\', \\\'${f.depCode}\\\', \\\'${f.arrCode}\\\', \\\'${f.duration}\\\')">\n                <div class="fc-class-name">Stretch')

    with open('app.js', 'w') as f:
        f.write(js)
    print("Updated app.js")

