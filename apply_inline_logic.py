import re

with open('app.js', 'r') as f:
    js = f.read()

# 1. Remove old Drawer logic
# Find window.openFareSelectionDrawer up to the end of window.updateFareFooter
start_idx = js.find('window.openFareSelectionDrawer = function')
if start_idx != -1:
    end_idx = js.find('window.updateFareFooter = function')
    end_idx = js.find('};', end_idx) + 2
    js = js[:start_idx] + js[end_idx:]

new_logic = """
window.toggleInlineFare = function(event, cardId, className, basePrice) {
    if (event) event.stopPropagation();
    
    // Close other expanded cards
    document.querySelectorAll('.inline-fare-container.expanded').forEach(el => {
        if (el.id !== `inline-fare-${cardId}`) {
            el.classList.remove('expanded');
        }
    });

    const container = document.getElementById(`inline-fare-${cardId}`);
    if (!container) return;

    // Toggle expansion
    if (container.classList.contains('expanded') && container.dataset.currentClass === className) {
        container.classList.remove('expanded');
        return;
    }

    container.classList.add('expanded');
    container.dataset.currentClass = className;
    
    window.currentBaseFare = parseInt(basePrice.toString().replace(/,/g, ''));
    
    // Generate HTML for the carousel
    const options = window.fareOptions[className] || window.fareOptions['Economy'];
    let carouselHtml = `<div class="inline-carousel">`;
    
    options.forEach(opt => {
        const totalFare = window.currentBaseFare + opt.priceAdd;
        const isPopular = opt.isPopular ? `<div class="inline-popular-badge ${opt.badgeClass || ''}">Popular fare</div>` : '';
        const cardClass = `inline-fare-card ${className === 'Stretch' ? 'stretch-card' : ''}`;
        
        let featuresHtml = '';
        opt.features.forEach(f => {
            if (f.type === 'text-only') {
                featuresHtml += `<div class="inline-feature-item" style="justify-content: ${f.align || 'flex-start'}">${f.text}</div>`;
            } else {
                const iconSvg = svgIcons[f.icon] || '';
                const itemClass = `inline-feature-item ${f.type === 'cross' ? 'cross' : 'highlighted'}`;
                featuresHtml += `<div class="${itemClass}">${iconSvg} <span>${f.text}</span></div>`;
            }
        });
        
        carouselHtml += `
            <div class="${cardClass}">
                <div class="inline-fare-header">${opt.name}</div>
                ${isPopular}
                <div class="inline-fare-features">
                    ${featuresHtml}
                </div>
                <div class="inline-fare-footer">
                    <div style="font-size: 10px; color: #999;">Starting from</div>
                    <div style="font-size: 16px; font-weight: 800; color: ${className==='Stretch' ? '#D4AF37' : 'var(--indigo-blue)'};">₹ ${totalFare.toLocaleString('en-IN')}<span style="font-size:11px; font-weight:400; color:#666;">/ Pax</span></div>
                    <button class="inline-select-btn" onclick="selectFinalFare(event, '${opt.id}', ${totalFare})">Select</button>
                </div>
            </div>
        `;
    });
    
    carouselHtml += `</div>`;
    
    // Add compare button
    carouselHtml += `
        <div class="inline-compare-btn" onclick="openCompareFaresModal(event, '${className}')">
            Compare Fares <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -2px;"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </div>
    `;

    container.innerHTML = carouselHtml;
    if (typeof triggerHaptic === 'function') triggerHaptic('light', 'Inline fare toggled');
};

window.selectFinalFare = function(event, fareId, totalFare) {
    if (event) event.stopPropagation();
    if (typeof triggerHaptic === 'function') triggerHaptic('medium', 'Fare selected');
    
    document.querySelectorAll('.inline-fare-container.expanded').forEach(el => el.classList.remove('expanded'));
    alert(`Selected fare: ${fareId}. Total: ₹ ${totalFare.toLocaleString('en-IN')}. Proceeding to next step...`);
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
js = js.replace(r"openFareSelectionDrawer(event, 'Economy', '${f.price}', '${f.id}', '${f.from}', '${f.to}', 'DEL, T1', 'BOM, T2', '${f.dur}')", 
                r"toggleInlineFare(event, '${i}', 'Economy', '${f.price}')")

js = js.replace(r"openFareSelectionDrawer(event, 'Stretch', '${f.stretch || 28000}', '${f.id}', '${f.from}', '${f.to}', 'DEL, T1', 'BOM, T2', '${f.dur}')", 
                r"toggleInlineFare(event, '${i}', 'Stretch', '${f.stretch || 28000}')")

# Add the inline container to the end of flight-card
card_end = r"</div>\n        </div>\n        `;"
new_card_end = r"</div>\n            <div class=\"inline-fare-container\" id=\"inline-fare-${i}\"></div>\n        </div>\n        `;"
js = js.replace(card_end, new_card_end)

with open('app.js', 'w') as f:
    f.write(js)

print("Updated app.js logic")

# 3. Update index.html
with open('index.html', 'r') as f:
    html = f.read()

# Remove drawer
drawer_regex = re.compile(r'<!-- Fare Selection Drawer -->.*?<!-- Bank Offer Sheet -->', re.DOTALL)
html = re.sub(drawer_regex, '<!-- Bank Offer Sheet -->', html)

# Add compare modal
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
    html = html.replace('<!-- Flight Details Full Drawer -->', compare_modal + '\n                <!-- Flight Details Full Drawer -->')

# Modify hardcoded flight cards
for i in range(1, 11):
    html = html.replace(f"openFareSelectionDrawer(event, 'Economy', '4800', '6E 1234', '05:15', '07:30', 'DEL, T1', 'BOM, T2', '2h 15m')",
                        f"toggleInlineFare(event, 'hc{i}', 'Economy', '4800')")
    html = html.replace(f"openFareSelectionDrawer(event, 'Stretch', '28000', '6E 1234', '05:15', '07:30', 'DEL, T1', 'BOM, T2', '2h 15m')",
                        f"toggleInlineFare(event, 'hc{i}', 'Stretch', '28000')")
    
    # We need to inject the inline container into hardcoded cards. 
    # This is tricky because hardcoded cards don't have IDs like the dynamic ones.
    # It's better to tell the user to use the search to see it dynamically, 
    # but I'll add an ID to the first hardcoded card if I can.
    
with open('index.html', 'w') as f:
    f.write(html)

print("Updated index.html")
