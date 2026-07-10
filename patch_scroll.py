import re

# 1. Update style.css
with open('style.css', 'r') as f:
    css = f.read()

old_chips_css = """.pass-calendar-chips {
    display: flex;
    justify-content: space-between;
    gap: 5px;
}

.pass-chip {
    flex: 1;"""

new_chips_css = """.pass-calendar-chips {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    scroll-behavior: smooth;
    -ms-overflow-style: none;  /* IE and Edge */
    scrollbar-width: none;  /* Firefox */
    padding-bottom: 5px;
}

.pass-calendar-chips::-webkit-scrollbar {
    display: none;
}

.pass-chip {
    flex: 0 0 23%;
    scroll-snap-align: center;"""

css = css.replace(old_chips_css, new_chips_css)
with open('style.css', 'w') as f:
    f.write(css)

# 2. Update app.js
with open('app.js', 'r') as f:
    js = f.read()

# Replace travelOnTapData completely
import textwrap
new_data = """const travelOnTapData = {
    HJR: {
        name: 'Khajuraho Airport (HJR)',
        basePrice: '₹3,199',
        fares: [
            { date: '14 Jun', price: 3499, display: '₹3,499' },
            { date: '15 Jun', price: 3299, display: '₹3,299' },
            { date: '16 Jun', price: 3199, display: '₹3,199', lowest: true },
            { date: '17 Jun', price: 3399, display: '₹3,399' },
            { date: '18 Jun', price: 3499, display: '₹3,499' },
            { date: '19 Jun', price: 3199, display: '₹3,199', lowest: true },
            { date: '20 Jun', price: 3899, display: '₹3,899' },
            { date: '21 Jun', price: 3599, display: '₹3,599' },
            { date: '22 Jun', price: 4299, display: '₹4,299' },
            { date: '23 Jun', price: 4099, display: '₹4,099' }
        ]
    },
    KNU: {
        name: 'Kanpur (KNU)',
        basePrice: '₹2,999',
        fares: [
            { date: '14 Jun', price: 2999, display: '₹2,999', lowest: true },
            { date: '15 Jun', price: 3199, display: '₹3,199' },
            { date: '16 Jun', price: 3399, display: '₹3,399' },
            { date: '17 Jun', price: 3099, display: '₹3,099' },
            { date: '18 Jun', price: 2999, display: '₹2,999', lowest: true },
            { date: '19 Jun', price: 3299, display: '₹3,299' },
            { date: '20 Jun', price: 3099, display: '₹3,099' },
            { date: '21 Jun', price: 3499, display: '₹3,499' },
            { date: '22 Jun', price: 3999, display: '₹3,999' },
            { date: '23 Jun', price: 3799, display: '₹3,799' }
        ]
    },
    DHM: {
        name: 'Dharamsala (DHM)',
        basePrice: '₹4,199',
        fares: [
            { date: '14 Jun', price: 4299, display: '₹4,299' },
            { date: '15 Jun', price: 4199, display: '₹4,199', lowest: true },
            { date: '16 Jun', price: 4599, display: '₹4,599' },
            { date: '17 Jun', price: 4799, display: '₹4,799' },
            { date: '18 Jun', price: 4599, display: '₹4,599' },
            { date: '19 Jun', price: 4399, display: '₹4,399' },
            { date: '20 Jun', price: 4199, display: '₹4,199', lowest: true },
            { date: '21 Jun', price: 4899, display: '₹4,899' },
            { date: '22 Jun', price: 4299, display: '₹4,299' },
            { date: '23 Jun', price: 4499, display: '₹4,499' }
        ]
    },
    IXC: {
        name: 'Chandigarh (IXC)',
        basePrice: '₹3,199',
        fares: [
            { date: '14 Jun', price: 3199, display: '₹3,199', lowest: true },
            { date: '15 Jun', price: 3499, display: '₹3,499' },
            { date: '16 Jun', price: 3299, display: '₹3,299' },
            { date: '17 Jun', price: 3599, display: '₹3,599' },
            { date: '18 Jun', price: 3399, display: '₹3,399' },
            { date: '19 Jun', price: 3199, display: '₹3,199', lowest: true },
            { date: '20 Jun', price: 3599, display: '₹3,599' },
            { date: '21 Jun', price: 3299, display: '₹3,299' },
            { date: '22 Jun', price: 3899, display: '₹3,899' },
            { date: '23 Jun', price: 3699, display: '₹3,699' }
        ]
    }
};"""

old_data_regex = re.compile(r"const travelOnTapData = \{.*?\n};", re.DOTALL)
js = old_data_regex.sub(new_data, js)

js = js.replace('let selectedTapFareIndex = -1;', 'let selectedTapFareIndex = 4;')
js = js.replace('selectedTapFareIndex = -1; // reset selected date in the new pass', 'selectedTapFareIndex = 4; // default to middle item')


# Update renderBoardingPassCalendar to add the scroll listener
old_render = """        chip.onclick = (e) => {
            e.stopPropagation(); // prevent card collapse click
            selectBoardingPassDate(code, i);
        };
        
        container.appendChild(chip);
    });
}"""

new_render = """        chip.onclick = (e) => {
            e.stopPropagation(); // prevent card collapse click
            chip.scrollIntoView({ behavior: 'smooth', inline: 'center' });
            selectBoardingPassDate(code, i);
        };
        
        container.appendChild(chip);
    });

    // Add scroll event listener to automatically select the center chip
    container.addEventListener('scroll', () => {
        const containerCenter = container.getBoundingClientRect().left + container.offsetWidth / 2;
        let closestIndex = -1;
        let minDistance = Infinity;
        
        const chips = container.querySelectorAll('.pass-chip');
        chips.forEach((c, idx) => {
            const rect = c.getBoundingClientRect();
            const chipCenter = rect.left + rect.width / 2;
            const dist = Math.abs(chipCenter - containerCenter);
            if (dist < minDistance) {
                minDistance = dist;
                closestIndex = idx;
            }
        });
        
        if (closestIndex !== -1 && selectedTapFareIndex !== closestIndex) {
            chips.forEach(c => c.classList.remove('selected-fare'));
            chips[closestIndex].classList.add('selected-fare');
            selectedTapFareIndex = closestIndex;
            
            // Auto-fill Search Widget parameters for the new center date silently
            const destObj = travelOnTapData[code];
            if (destObj) {
                const originAp = airports.find(ap => ap.code === 'DEL');
                const destAp = airports.find(ap => ap.code === code);
                if (originAp && destAp) {
                    appState.selectedFrom = originAp;
                    appState.selectedTo = destAp;
                    document.getElementById('valFromCode').innerText = originAp.city;
                    document.getElementById('valToCode').innerText = destAp.city;
                }
            }
        }
    });

    // On initial render, scroll the 5th item into the center
    setTimeout(() => {
        if (container.children.length > 4) {
            // we use center inline so it's perfectly middle
            container.children[4].scrollIntoView({ behavior: 'auto', inline: 'center' });
        }
    }, 50);
}"""

js = js.replace(old_render, new_render)

with open('app.js', 'w') as f:
    f.write(js)
