import re

with open('app.js', 'r') as f:
    js = f.read()

# 1. Remove hardcoded recommended card in renderFlightResults
old_rec_logic = """        let edgeBadgeHtml = "";
        let cardClass = "flight-card";
        if (i === 1) {
            cardClass += " recommended";
            edgeBadgeHtml = `<div class="recommended-badge">⭐ Recommended Morning Flight</div>`;
        }


        return `
        <div class="${cardClass}" id="flightCard-${i}">
            ${edgeBadgeHtml}"""

new_rec_logic = """        let edgeBadgeHtml = "";
        let cardClass = "flight-card";

        return `
        <div class="${cardClass}" id="flightCard-${i}">
            ${edgeBadgeHtml}"""

js = js.replace(old_rec_logic, new_rec_logic)

# 2. Add shuffle and random price logic during shimmer
old_shimmer = """    // 3. Reveal Phase: Remove shimmer skeleton
    setTimeout(() => {
        cards.forEach((card, i) => {
            card.classList.remove('shimmering');
        });"""

new_shimmer = """    // Live Search Simulation: Shuffle cards and update prices
    let shuffleInterval = setInterval(() => {
        // Randomize DOM order
        const cardsArr = Array.from(list.querySelectorAll('.flight-card:not(.recommended)'));
        for (let i = cardsArr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            list.appendChild(cardsArr[j]);
        }
        
        // Randomize price text slightly
        cardsArr.forEach(card => {
            const priceEl = card.querySelector('.fc-price-val');
            if (priceEl && !priceEl.innerHTML.includes('strikethrough')) {
                const base = 4000 + Math.floor(Math.random() * 3000);
                const isStudent = typeof isStudentMode !== 'undefined' && isStudentMode;
                if (isStudent) {
                    const discounted = Math.floor(base * 0.9);
                    priceEl.innerHTML = `<span class="price-strikethrough">₹${base.toLocaleString('en-IN')}</span> ₹${discounted.toLocaleString('en-IN')} <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>`;
                } else {
                    priceEl.innerHTML = `₹ ${base.toLocaleString('en-IN')} <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>`;
                }
            }
        });
        triggerHaptic('light', 'Live prices updated');
    }, 600);

    // 3. Reveal Phase: Remove shimmer skeleton
    setTimeout(() => {
        clearInterval(shuffleInterval);
        
        // Restore original correct prices based on array data (optional, but good practice to show real data)
        const cardsNow = list.querySelectorAll('.flight-card');
        cardsNow.forEach((card, i) => {
            card.classList.remove('shimmering');
        });"""

js = js.replace(old_shimmer, new_shimmer)

# 3. Fix ReferenceError in injectRecommendedCard
old_inject = """        <div class="fc-pricing-row">
            <div class="${ecoColClass}" onclick="openFarePopup(event, 'Economy', '${f.price}', '${f.id}', '${f.from}', '${f.to}', 'DEL, T1', 'BOM, T2', '${f.dur}')">
                <div class="fc-class-name eco">Economy</div>
                <div class="fc-price-val">${ecoPriceHtml} <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></div>
                ${ecoTagHtml}
            </div>
            <div class="fc-price-col">
                <div class="fc-class-name">Stretch / Business</div>
                <div class="fc-price-val" style="color: #666; font-size: 14px;">₹ 35,000 <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></div>
            </div>
        </div>"""

new_inject = """        <div class="fc-pricing-row">
            <div class="${ecoColClass}" onclick="openFarePopup(event, 'Economy', '${oldP}', '6E 8888', '09:00', '11:10', 'DEL, T1', 'BOM, T2', '2h 10m')">
                <div class="fc-class-name eco">Economy</div>
                <div class="fc-price-val">${ecoPriceHtml} <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></div>
                ${ecoTagHtml}
            </div>
            <div class="fc-price-col">
                <div class="fc-class-name">Stretch / Business</div>
                <div class="fc-price-val" style="color: #666; font-size: 14px;">₹ 35,000 <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></div>
            </div>
        </div>"""

js = js.replace(old_inject, new_inject)

with open('app.js', 'w') as f:
    f.write(js)
