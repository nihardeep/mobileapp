import re

# 1. Update style.css transition for slow opening
with open('style.css', 'r') as f:
    css = f.read()

old_pass_body = """    transition: max-height 0.45s cubic-bezier(0.25, 1, 0.5, 1), 
                opacity 0.35s ease;"""

new_pass_body = """    transition: max-height 0.8s cubic-bezier(0.25, 1, 0.5, 1), 
                opacity 0.6s ease;"""

css = css.replace(old_pass_body, new_pass_body)

with open('style.css', 'w') as f:
    f.write(css)

# 2. Update app.js
with open('app.js', 'r') as f:
    js = f.read()

# Make expandBoardingPass scroll the window smoothly to the card
old_expand = """    const targetCard = document.getElementById(`passCard${code}`);
    if (targetCard) {
        targetCard.classList.add('expanded');
    }
    
    // Render the fare calendar inside this pass
    renderBoardingPassCalendar(code);"""

new_expand = """    const targetCard = document.getElementById(`passCard${code}`);
    if (targetCard) {
        targetCard.classList.add('expanded');
        // keep focus seamlessly
        setTimeout(() => {
            targetCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
    }
    
    // Render the fare calendar inside this pass
    renderBoardingPassCalendar(code);"""

js = js.replace(old_expand, new_expand)

# Replace scrollIntoView inside chip click
old_chip_click = """        chip.onclick = (e) => {
            e.stopPropagation(); // prevent card collapse click
            chip.scrollIntoView({ behavior: 'smooth', inline: 'center' });
            selectBoardingPassDate(code, i);
        };"""

new_chip_click = """        chip.onclick = (e) => {
            e.stopPropagation(); // prevent card collapse click
            const scrollLeftTarget = chip.offsetLeft - container.offsetWidth / 2 + chip.offsetWidth / 2;
            container.scrollTo({ left: scrollLeftTarget, behavior: 'smooth' });
            selectBoardingPassDate(code, i);
        };"""

js = js.replace(old_chip_click, new_chip_click)

# Replace scrollIntoView on initial render
old_init_scroll = """    // On initial render, scroll the 5th item into the center
    setTimeout(() => {
        if (container.children.length > 4) {
            // we use center inline so it's perfectly middle
            container.children[4].scrollIntoView({ behavior: 'auto', inline: 'center' });
        }
    }, 50);"""

new_init_scroll = """    // On initial render, scroll the 5th item into the center horizontally
    setTimeout(() => {
        if (container.children.length > 4) {
            const chip = container.children[4];
            const scrollLeftTarget = chip.offsetLeft - container.offsetWidth / 2 + chip.offsetWidth / 2;
            container.scrollTo({ left: scrollLeftTarget, behavior: 'auto' });
        }
    }, 50);"""

js = js.replace(old_init_scroll, new_init_scroll)

with open('app.js', 'w') as f:
    f.write(js)

