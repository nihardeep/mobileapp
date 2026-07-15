
/* ==========================================================================
   DIGITAL BOARDING PASS LOGIC
   ========================================================================== */

function setBPState(state) {
    // Update Demo Buttons
    document.querySelectorAll('.bp-demo-btn').forEach(btn => btn.classList.remove('active'));
    
    const dividers = document.querySelectorAll('.bp-divider.multi-only');
    const leg2s = document.querySelectorAll('.bp-leg.multi-only');
    const overlays = document.querySelectorAll('.bp-completed-overlay');
    const hints = document.querySelectorAll('.bp-scan-hint');
    const leg1s = document.querySelectorAll('.bp-leg:not(.multi-only)');

    if (state === 'single') {
        document.getElementById('btnBPSingle').classList.add('active');
        dividers.forEach(el => el.style.display = 'none');
        leg2s.forEach(el => el.style.display = 'none');
        overlays.forEach(el => el.classList.remove('show'));
        leg1s.forEach(el => el.classList.remove('dimmed'));
        hints.forEach(el => el.innerText = 'TAP TO SCAN FOR XA 201');
    } else if (state === 'multi') {
        document.getElementById('btnBPMulti').classList.add('active');
        dividers.forEach(el => el.style.display = 'block');
        leg2s.forEach(el => el.style.display = 'block');
        overlays.forEach(el => el.classList.remove('show'));
        leg1s.forEach(el => el.classList.remove('dimmed'));
        hints.forEach(el => el.innerText = 'TAP TO SCAN FOR XA 201 (LEG 1)');
    } else if (state === 'completed') {
        document.getElementById('btnBPDone').classList.add('active');
        dividers.forEach(el => el.style.display = 'block');
        leg2s.forEach(el => el.style.display = 'block');
        overlays.forEach(el => el.classList.add('show'));
        leg1s.forEach(el => el.classList.add('dimmed'));
        hints.forEach(el => el.innerText = 'TAP TO SCAN FOR XA 405 (LEG 2)');
    }
}

// Carousel Scroll Logic
const bpCarousel = document.getElementById('bpCarousel');
const bpDots = document.querySelectorAll('.bp-dot');

if (bpCarousel) {
    bpCarousel.addEventListener('scroll', () => {
        const slideWidth = bpCarousel.offsetWidth;
        const scrollPos = bpCarousel.scrollLeft;
        const activeIndex = Math.round(scrollPos / slideWidth);
        
        bpDots.forEach((dot, index) => {
            if (index === activeIndex) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    });
}

function scrollToSlide(index) {
    if (bpCarousel) {
        const slideWidth = bpCarousel.offsetWidth;
        bpCarousel.scrollTo({
            left: slideWidth * index,
            behavior: 'smooth'
        });
    }
}

// Initialize single state on load
document.addEventListener('DOMContentLoaded', () => {
    if(document.getElementById('btnBPSingle')) {
        setBPState('single');
    }
});

// Trip Companion Flow
function handleCheckIn() {
    const btn = document.getElementById('btnCheckIn');
    btn.innerHTML = '<span style="animation: pulse-glow 1s infinite;">Checking in...</span>';
    setTimeout(() => {
        btn.style.display = 'none';
        document.getElementById('btnViewBP').style.display = 'block';
    }, 1500);
}

function showBoardingPasses() {
    document.getElementById('tripsCompanionCard').style.display = 'none';
    document.getElementById('tripsBoardingPassUI').style.display = 'block';
}

function hideBoardingPasses() {
    document.getElementById('tripsCompanionCard').style.display = 'block';
    document.getElementById('tripsBoardingPassUI').style.display = 'none';
}
