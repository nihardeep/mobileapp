import re

with open('app.js', 'r') as f:
    js = f.read()

# Add drag to scroll and click-prevent logic to renderBoardingPassCalendar
old_render_end = """        chip.onclick = (e) => {
            e.stopPropagation(); // prevent card collapse click
            const scrollLeftTarget = chip.offsetLeft - container.offsetWidth / 2 + chip.offsetWidth / 2;
            container.scrollTo({ left: scrollLeftTarget, behavior: 'smooth' });
            selectBoardingPassDate(code, i);
        };
        
        container.appendChild(chip);
    });

    // Add scroll event listener to automatically select the center chip"""

new_render_end = """        // Handle click manually to avoid triggering after drag
        chip.addEventListener('click', (e) => {
            e.stopPropagation(); // prevent card collapse click
            if (container.dataset.isDragging === 'true') return; // Prevent click if dragged
            
            const scrollLeftTarget = chip.offsetLeft - container.offsetWidth / 2 + chip.offsetWidth / 2;
            container.scrollTo({ left: scrollLeftTarget, behavior: 'smooth' });
            selectBoardingPassDate(code, i);
        });
        
        container.appendChild(chip);
    });

    // --- Drag to Scroll Logic for Desktop ---
    let isDown = false;
    let startX;
    let scrollLeft;
    let dragThreshold = false;

    container.addEventListener('mousedown', (e) => {
        isDown = true;
        dragThreshold = false;
        container.dataset.isDragging = 'false';
        container.classList.add('active-drag');
        startX = e.pageX - container.offsetLeft;
        scrollLeft = container.scrollLeft;
        
        // temporarily disable snap for smooth drag
        container.style.scrollSnapType = 'none';
        container.style.scrollBehavior = 'auto';
    });
    
    const stopDrag = () => {
        if (!isDown) return;
        isDown = false;
        container.classList.remove('active-drag');
        // re-enable snap
        container.style.scrollSnapType = 'x mandatory';
        container.style.scrollBehavior = 'smooth';
        
        setTimeout(() => {
            container.dataset.isDragging = 'false';
        }, 50);
    };

    container.addEventListener('mouseleave', stopDrag);
    container.addEventListener('mouseup', stopDrag);

    container.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        const x = e.pageX - container.offsetLeft;
        const walk = (x - startX) * 1.5; // drag speed
        
        if (Math.abs(walk) > 10) {
            dragThreshold = true;
            container.dataset.isDragging = 'true';
            e.preventDefault(); // prevent text selection
        }
        
        container.scrollLeft = scrollLeft - walk;
    });

    // Add scroll event listener to automatically select the center chip"""

js = js.replace(old_render_end, new_render_end)

with open('app.js', 'w') as f:
    f.write(js)
