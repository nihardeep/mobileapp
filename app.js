/* PLAY & WIN GAME LOGIC */
/* ========================================== */
const GAME_TARGET_WORDS = ['FLY', 'PLANE', '6ESKY', 'X AIRLINE'];
const GAME_FOUND_WORDS = new Set();
let gameCurrentPath = []; // array of indices
let gameIsDragging = false;
let gameLastTarget = null;
let gameConfettiInterval;

const GAME_GRID = [
    'X', 'F', 'L', 'X', 'I',
    'X', 'P', 'Y', 'X', 'N',
    'X', 'L', 'S', 'E', 'D',
    'N', 'A', 'K', '6', 'I',
    'E', 'X', 'Y', 'O', 'G'
];

function openGame() {
    triggerHaptic('medium', 'Open Game');
    if (typeof closeAllDrawers === 'function') closeAllDrawers();
    document.getElementById('screenGame').style.display = 'block';
    // Add active class for smooth entry if needed
    document.getElementById('screenGame').classList.add('active');
    document.getElementById('screenGame').style.zIndex = '9999999'; // Ensure it appears above any lingering elements
    
    // Only init if not already init
    if (document.getElementById('gameBoard').children.length <= 1) {
        initGame();
    }
}

function closeGame() {
    triggerHaptic('light', 'Close Game');
    document.getElementById('screenGame').style.display = 'none';
    document.getElementById('screenGame').classList.remove('active');
    document.getElementById('gameWinOverlay').style.display = 'none';
    document.getElementById('gameWinOverlay').style.opacity = '0';
    if (gameConfettiInterval) clearInterval(gameConfettiInterval);
}

function initGame() {
    const board = document.getElementById('gameBoard');
    const placeholders = document.getElementById('gamePlaceholders');
    
    // Render Board
    for (let i = 0; i < 25; i++) {
        const char = GAME_GRID[i];
        const cell = document.createElement('div');
        cell.className = 'game-cell' + (char === 'X' ? ' blocked' : '');
        cell.innerText = char;
        cell.dataset.index = i;
        
        // Touch / Mouse events
        if (char !== 'X') {
            cell.addEventListener('mousedown', gameStartDrag);
            cell.addEventListener('mouseenter', gameEnterCell);
            
            // For touch devices
            cell.addEventListener('touchstart', (e) => {
                e.preventDefault();
                gameStartDrag(e);
            }, {passive: false});
            cell.addEventListener('touchmove', (e) => {
                e.preventDefault();
                const touch = e.touches[0];
                const target = document.elementFromPoint(touch.clientX, touch.clientY);
                if (target && target.classList.contains('game-cell') && target !== gameLastTarget) {
                    gameLastTarget = target;
                    // Trigger fake enter event
                    gameEnterCell({ target: target });
                }
            }, {passive: false});
        }
        
        board.appendChild(cell);
    }
    
    // Global mouseup/touchend
    document.addEventListener('mouseup', gameEndDrag);
    document.addEventListener('touchend', gameEndDrag);
    
    // Render Placeholders
    GAME_TARGET_WORDS.forEach(word => {
        const group = document.createElement('div');
        group.className = 'word-group';
        group.id = 'word-group-' + word;
        
        for (let i = 0; i < word.length; i++) {
            const box = document.createElement('div');
            box.className = 'word-box';
            group.appendChild(box);
        }
        
        const check = document.createElement('div');
        check.className = 'word-check';
        check.innerText = '✓';
        group.appendChild(check);
        
        placeholders.appendChild(group);
    });
}

function gameStartDrag(e) {
    let target = e.target;
    // Handle touch event
    if (e.touches && e.touches.length > 0) {
        target = document.elementFromPoint(e.touches[0].clientX, e.touches[0].clientY);
    }
    if (!target || target.classList.contains('blocked') || target.classList.contains('solved')) return;
    
    gameIsDragging = true;
    gameLastTarget = target;
    gameCurrentPath = [parseInt(target.dataset.index)];
    target.classList.add('selected');
    triggerHaptic('light', 'Start Trace');
    drawGamePath();
}

function gameEnterCell(e) {
    if (!gameIsDragging) return;
    
    const cell = e.target;
    if (cell.classList.contains('blocked') || cell.classList.contains('solved')) return;
    
    const index = parseInt(cell.dataset.index);
    const lastIndex = gameCurrentPath[gameCurrentPath.length - 1];
    
    // Backtracking
    if (gameCurrentPath.length >= 2 && index === gameCurrentPath[gameCurrentPath.length - 2]) {
        const popped = gameCurrentPath.pop();
        document.querySelector(`.game-cell[data-index="${popped}"]`).classList.remove('selected');
        triggerHaptic('light', 'Backtrack Trace');
        drawGamePath();
        return;
    }
    
    // Must be adjacent and not already in path
    if (!gameCurrentPath.includes(index) && isAdjacent(lastIndex, index)) {
        gameCurrentPath.push(index);
        cell.classList.add('selected');
        triggerHaptic('light', 'Add Trace');
        drawGamePath();
    }
}

function gameEndDrag() {
    if (!gameIsDragging) return;
    gameIsDragging = false;
    gameLastTarget = null;
    
    // Check if current path matches any word
    let wordSpelled = gameCurrentPath.map(i => GAME_GRID[i]).join('');
    
    // Allow reverse spelling? Yes.
    let wordSpelledRev = gameCurrentPath.slice().reverse().map(i => GAME_GRID[i]).join('');
    
    let foundWord = null;
    if (GAME_TARGET_WORDS.includes(wordSpelled)) foundWord = wordSpelled;
    else if (GAME_TARGET_WORDS.includes(wordSpelledRev)) foundWord = wordSpelledRev;
    
    if (foundWord && !GAME_FOUND_WORDS.has(foundWord)) {
        // Success
        GAME_FOUND_WORDS.add(foundWord);
        GAME_SOLVED_PATHS.push({ word: foundWord, path: [...gameCurrentPath] });
        triggerHaptic('success', 'Word Found');
        
        // Draw permanent SVG path
        const svgContainer = document.getElementById('gamePathSvg');
        const permPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const d = document.getElementById('currentPath').getAttribute('d');
        permPath.setAttribute('d', d);
        permPath.setAttribute('fill', 'none');
        permPath.setAttribute('stroke', '#22d3ee');
        permPath.setAttribute('stroke-width', '18');
        permPath.setAttribute('stroke-linecap', 'round');
        permPath.setAttribute('stroke-linejoin', 'round');
        permPath.setAttribute('opacity', '0.6');
        permPath.setAttribute('class', 'perm-path');
        permPath.id = 'perm-path-' + foundWord;
        svgContainer.insertBefore(permPath, document.getElementById('currentPath'));
        
        // Mark cells as solved (for logic, but don't change background to solid)
        gameCurrentPath.forEach((idx, i) => {
            const el = document.querySelector(`.game-cell[data-index="${idx}"]`);
            el.classList.remove('selected');
            el.classList.add('solved');
            // Add checkmark only to the first letter
            if (i === 0) {
                el.classList.add('solved-start');
            }
        });
        
        // Fill placeholder
        const group = document.getElementById('word-group-' + foundWord);
        const boxes = group.querySelectorAll('.word-box');
        for (let i = 0; i < foundWord.length; i++) {
            boxes[i].innerText = foundWord[i];
            boxes[i].classList.add('filled');
        }
        
        // Check win
        if (GAME_FOUND_WORDS.size === GAME_TARGET_WORDS.length) {
            setTimeout(showGameWin, 800);
        }
    } else {
        // Fail - reset path
        gameCurrentPath.forEach(i => {
            document.querySelector(`.game-cell[data-index="${i}"]`).classList.remove('selected');
        });
        triggerHaptic('light', 'Fail');
    }
    
    gameCurrentPath = [];
    drawGamePath();
}

function drawGamePath() {
    const svgPath = document.getElementById('currentPath');
    if (gameCurrentPath.length < 2) {
        svgPath.setAttribute('d', '');
        return;
    }
    
    let d = '';
    gameCurrentPath.forEach((idx, i) => {
        // Calculate center of cell. 
        // 5 columns, each cell is 50x50, gap is 4.
        // Cell col = idx % 5. Cell row = Math.floor(idx / 5).
        // Center X = col * (50 + 4) + 25 = col * 54 + 25
        // Center Y = row * (50 + 4) + 25 = row * 54 + 25
        const col = idx % 5;
        const row = Math.floor(idx / 5);
        
        const x = col * 54 + 25;
        const y = row * 54 + 25;
        
        if (i === 0) d += `M ${x} ${y} `;
        else d += `L ${x} ${y} `;
    });
    
    svgPath.setAttribute('d', d);
}

function isAdjacent(idx1, idx2) {
    const r1 = Math.floor(idx1 / 5), c1 = idx1 % 5;
    const r2 = Math.floor(idx2 / 5), c2 = idx2 % 5;
    return Math.abs(r1 - r2) + Math.abs(c1 - c2) === 1;
}

const GAME_SOLVED_PATHS = [];

function undoGamePath() {
    if (GAME_SOLVED_PATHS.length > 0) {
        const lastSolve = GAME_SOLVED_PATHS.pop();
        GAME_FOUND_WORDS.delete(lastSolve.word);
        
        // Un-solve cells
        lastSolve.path.forEach(idx => {
            const el = document.querySelector(`.game-cell[data-index="${idx}"]`);
            el.classList.remove('solved');
            el.classList.remove('solved-start');
        });
        
        // Remove permanent path
        const permPath = document.getElementById('perm-path-' + lastSolve.word);
        if (permPath) permPath.remove();
        
        // Un-fill placeholders
        const group = document.getElementById('word-group-' + lastSolve.word);
        const boxes = group.querySelectorAll('.word-box');
        boxes.forEach(box => {
            box.innerText = '';
            box.classList.remove('filled');
        });
        
        triggerHaptic('light', 'Undo');
    }
}

function showGameHint() {
    triggerHaptic('medium', 'Hint');
    const unsolved = GAME_TARGET_WORDS.find(w => !GAME_FOUND_WORDS.has(w));
    if (unsolved) {
        // Find the first letter index of the unsolved word in the grid
        const firstLetter = unsolved[0];
        const possibleIndices = [];
        for (let i = 0; i < 25; i++) {
            if (GAME_GRID[i] === firstLetter && !document.querySelector(`.game-cell[data-index="${i}"]`).classList.contains('solved')) {
                possibleIndices.push(i);
            }
        }
        
        if (possibleIndices.length > 0) {
            const el = document.querySelector(`.game-cell[data-index="${possibleIndices[0]}"]`);
            // Flash it
            el.style.transform = 'scale(1.2)';
            el.style.backgroundColor = '#fbbf24';
            setTimeout(() => {
                el.style.transform = '';
                el.style.backgroundColor = '';
            }, 600);
        }
    }
}

function showGameWin() {
    triggerHaptic('success', 'Game Won');
    const overlay = document.getElementById('gameWinOverlay');
    overlay.style.display = 'flex';
    overlay.style.zIndex = '99999999';
    // Trigger reflow
    void overlay.offsetWidth;
    overlay.style.opacity = '1';
    
    // Simple Confetti
    gameConfettiInterval = setInterval(() => {
        const confetti = document.createElement('div');
        confetti.style.position = 'absolute';
        confetti.style.width = '8px';
        confetti.style.height = '8px';
        confetti.style.backgroundColor = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'][Math.floor(Math.random() * 5)];
        confetti.style.top = '-10px';
        confetti.style.left = Math.random() * 100 + 'vw';
        confetti.style.borderRadius = '50%';
        confetti.style.zIndex = '305';
        confetti.style.pointerEvents = 'none';
        
        document.getElementById('gameWinOverlay').appendChild(confetti);
        
        let drop = 0;
        const anim = setInterval(() => {
            drop += 4;
            confetti.style.transform = `translateY(${drop}px)`;
            if (drop > window.innerHeight) {
                clearInterval(anim);
                confetti.remove();
            }
        }, 16);
    }, 100);
}

let isStudentMode = false;
let isStudentPersonaActive = false;


function toggleStudentPersona() {
    isStudentPersonaActive = !isStudentPersonaActive;
    
    const btn = document.getElementById('btnStateStudentPersona');
    if (btn) {
        if (isStudentPersonaActive) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    }
    
    const wrapper = document.getElementById('studentBannerWrapper');
    if (wrapper) {
        if (isStudentPersonaActive) {
            wrapper.classList.add('active');
            const header = document.getElementById("homeHeaderSection");
            if (header) header.style.paddingTop = "8px";
            triggerHaptic('medium', 'Student Persona On');
        } else {
            wrapper.classList.remove('active');
            const header = document.getElementById("homeHeaderSection");
            if (header) header.style.paddingTop = "52px";
            triggerHaptic('light', 'Student Persona Off');
        }
    }
    
    const carouselSlide = document.getElementById('studentCarouselSlide');
    if (carouselSlide) {
        carouselSlide.style.display = isStudentPersonaActive ? 'block' : 'none';
    }
}


function openStudentHub() {
    triggerHaptic('medium', 'Student Offer Clicked');
    navigateTo('studentHub');
}

function activateStudentModeAndSearch() {
    triggerHaptic('heavy', 'Search Student Fares');
    isStudentMode = true;
    searchFlights();
}

// ==========================================================================
// APP STATE & DATABASE
// ==========================================================================

let appState = {
    currentScreen: 'home',
    flightState: 'checkin_open', // checkin_open, checked_in, gate_open, airport_checkin, go_to_counter, gate_update, delayed, cancelled
    selectedFrom: null,
    selectedTo: null,
    airportSelectorTarget: 'from', // from, to
    activeCategoryIndex: 0,
    tripType: 'oneway',
    hasComplimentaryPerks: false
};

window.toggleComplimentaryPerks = function() {
    appState.hasComplimentaryPerks = !appState.hasComplimentaryPerks;
    const btn = document.getElementById('btnToggleComplimentary');
    if (btn) {
        if (appState.hasComplimentaryPerks) {
            btn.classList.add('active');
            triggerHaptic('success', 'Complimentary perks ON');
        } else {
            btn.classList.remove('active');
            triggerHaptic('medium', 'Complimentary perks OFF');
        }
    }
};

let pickerState = {
    selectedDate: null,
    calendarMonth: null,
    calendarYear: null,
    travelers: {
        adults: 1,
        children: 0,
        infants: 0
    }
};

const airports = [
    { code: 'DEL', city: 'Delhi', name: 'Indira Gandhi Int\'l' },
    { code: 'BOM', city: 'Mumbai', name: 'Chhatrapati Shivaji Maharaj' },
    { code: 'BLR', city: 'Bengaluru', name: 'Kempegowda Int\'l' },
    { code: 'DXB', city: 'Dubai', name: 'Dubai International' },
    { code: 'BKK', city: 'Bangkok', name: 'Suvarnabhumi Airport' },
    { code: 'DPS', city: 'Bali', name: 'Ngurah Rai Int\'l' },
    { code: 'MAA', city: 'Chennai', name: 'Chennai International' },
    { code: 'CCU', city: 'Kolkata', name: 'Netaji Subhash Chandra Bose' },
    { code: 'HJR', city: 'Khajuraho', name: 'Khajuraho Airport' },
    { code: 'KNU', city: 'Kanpur', name: 'Kanpur Airport' },
    { code: 'DHM', city: 'Dharamsala', name: 'Gaggal Airport' },
    { code: 'IXC', city: 'Chandigarh', name: 'Chandigarh Airport' }
];

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    updateTime();
    setInterval(updateTime, 1000 * 60); // Update time every minute
    switchCategory(0); // Set initial category tab
    setFlightState('checkin_open'); // Set initial flight state
    
    // Set default date to tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    pickerState.selectedDate = tomorrow;
    pickerState.calendarMonth = tomorrow.getMonth();
    pickerState.calendarYear = tomorrow.getFullYear();
    updateDateDisplay();
    
    // Initialize 3D carousels
    init3DCurvedCoverflow('offersCarousel', 'offersDots', 280, 220);
    init3DCurvedCoverflow('trendingInstaCarousel', 'trendingInstaDots', 140, 200);
    
    // Initialize Loyalty Loyalty animations
    triggerLoyaltyPlaneAnimation();
    initPartnerWallet();
    
    // Update initial search button state (disabled)
    updateSearchButtonState();
    
    // Initialize Travel on Tap Map & Calendar
    initTravelOnTap();
    
    // Initialize interactive flight simulator
    initFlightSimulator();
    
    // Setup haptic waveform visualizer
    initHapticWaveform();
    
    // Setup parallax scrolling
    setupParallaxScroll();

    // ── CRITICAL FIX ──────────────────────────────────────────────────────────
    // screenAddons and screenPassenger must live at the iphone-screen level
    // so position:absolute overlays work correctly as full-screen panels.
    const iphoneScreen = document.querySelector('.iphone-screen');
    if (iphoneScreen) {
        ['screenAddons', 'screenPassenger', 'screenSeatMap', 'screenSeatLoading'].forEach(id => {
            const el = document.getElementById(id);
            if (el && el.parentElement !== iphoneScreen) {
                iphoneScreen.appendChild(el);
            }
        });
    }
});

// Update Status Bar Time
function updateTime() {
    const now = new Date();
    let hours = now.getHours();
    let minutes = now.getMinutes();
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    document.getElementById('statusTime').innerText = `${hours}:${minutes}`;
}

// ==========================================================================
// SIMULATED HAPTIC & AUDIO SYSTEM
// ==========================================================================

function triggerHaptic(type, details) {
    const feedbackDot = document.getElementById('hapticDot');
    const feedbackMessage = document.getElementById('hapticMessage');
    
    // Trigger canvas visualizer wave burst
    triggerWaveformEffect(type);

    // 1. Play Audio Simulators
    const sndTap = document.getElementById('sndTap');
    const sndConfirm = document.getElementById('sndConfirm');
    const sndAlert = document.getElementById('sndAlert');
    
    if (sndTap && sndConfirm && sndAlert) {
        // Reset audio states
        sndTap.pause(); sndTap.currentTime = 0;
        sndConfirm.pause(); sndConfirm.currentTime = 0;
        sndAlert.pause(); sndAlert.currentTime = 0;
        
        // 2. Audio Triggers & Console Logs
        let color = '#475569';
        if (type === 'light') {
            sndTap.volume = sndTap.volume || 0.4;
            sndTap.play().catch(e => console.log('Audio disabled by browser policy'));
            color = '#8b5cf6'; // Neon Violet
        } else if (type === 'medium') {
            sndTap.volume = sndTap.volume || 0.6;
            sndTap.play().catch(e => console.log('Audio disabled by browser policy'));
            color = '#8b5cf6'; 
        } else if (type === 'heavy') {
            sndAlert.volume = sndAlert.volume || 0.5;
            sndAlert.play().catch(e => console.log('Audio disabled by browser policy'));
            color = '#8b5cf6';
        } else if (type === 'success') {
            sndConfirm.volume = sndConfirm.volume || 0.6;
            sndConfirm.play().catch(e => console.log('Audio disabled by browser policy'));
            color = '#10b981'; // Green
        } else if (type === 'error') {
            sndAlert.volume = sndAlert.volume || 0.7;
            sndAlert.play().catch(e => console.log('Audio disabled by browser policy'));
            color = '#ef4444'; // Red
        }
        
        // Update Cockpit Console Display
        if (feedbackDot && feedbackMessage) {
            feedbackDot.style.background = color;
            feedbackDot.style.boxShadow = `0 0 10px ${color}`;
            feedbackMessage.innerHTML = `<strong>VIBRATE:</strong> ${type.toUpperCase()}<br><span>${details}</span>`;
            
            // Flash dot back to normal
            setTimeout(() => {
                feedbackDot.style.background = '#475569';
                feedbackDot.style.boxShadow = 'none';
            }, 400);
        }
    }

    // 3. Physical Haptic Vibration (Web Vibrate API)
    if (navigator.vibrate) {
        if (type === 'light') {
            navigator.vibrate(12);
        } else if (type === 'medium') {
            navigator.vibrate(28);
        } else if (type === 'heavy') {
            navigator.vibrate(55);
        } else if (type === 'success') {
            navigator.vibrate([20, 40, 20]);
        } else if (type === 'error') {
            navigator.vibrate([60, 40, 60]);
        }
    }
}

// ==========================================================================
// NAVIGATION SYSTEM
// ==========================================================================

function navigateTo(screenName) {
    const screens = document.querySelectorAll('.screen');
    screens.forEach(s => s.classList.remove('active'));
    
    // Hide footer explicitly for some screens
    const bottomNav = document.querySelector('.bottom-nav');
    if (bottomNav) {
        bottomNav.style.display = (screenName === 'addons' || screenName === 'passenger' || screenName === 'seatmap' || screenName === 'seatmap_loading' || screenName === 'payments') ? 'none' : '';
    }

    if (screenName === 'seatmap_loading') {
        const loadingScreen = document.getElementById('screenSeatLoading');
        if (loadingScreen) loadingScreen.classList.add('active');
        
        // Reset state
        const plane = document.getElementById('seatLoadingPlane');
        if (plane) {
            plane.style.transition = 'none';
            plane.style.transform = 'translateY(100vh) scale(0.6)';
            plane.style.opacity = '0';
        }
        
        // Trigger plane animation
        setTimeout(() => {
            if (plane) {
                plane.style.transition = 'all 2.8s cubic-bezier(0.25, 0.8, 0.25, 1)';
                plane.style.opacity = '1';
                plane.style.transform = 'translateY(-100vh) scale(1.4)';
            }
        }, 50);
        
        // Navigate to real seatmap after 3.5s so user can read the message
        setTimeout(() => {
            navigateTo('seatmap');
        }, 3500);
        return;
    }

    try {
        // If navigating to home, ALWAYS reset the companion state even if already on home
        if (screenName === 'home') {
            const searchWidget = document.getElementById('searchWidgetSection');
            if (searchWidget) searchWidget.style.display = 'block';
        
            const recent = document.getElementById('recentSearchesSection');
            if (recent) recent.style.display = 'block';
            const cab = document.getElementById('companionCabDeals');
            if (cab) cab.style.display = 'none';
            
            const loyalty = document.getElementById('loyaltySection');
            if (loyalty) loyalty.style.display = 'block';
            const hotel = document.getElementById('companionHotelDeals');
            if (hotel) hotel.style.display = 'none';
        
            const wrapper = document.getElementById('homeFlightStateWrapper');
            if (wrapper) wrapper.style.display = 'none';
        
        // Remove active state from dev trip button
        const devTrips = document.getElementById('devNavTrips');
        if (devTrips) devTrips.classList.remove('active');
        
        // Activate dev home button
        const devHome = document.getElementById('btnDevNavHome');
        if (devHome) devHome.classList.add('active');
    }

    if (appState.currentScreen === screenName) return;
    
    // Trigger Nav Haptic
    triggerHaptic('light', `Navigate to ${screenName}`);

    // Update state
    appState.currentScreen = screenName;
    
    // Toggle active screen class
    document.querySelectorAll('.screen').forEach(scr => scr.classList.remove('active'));
    
    // Toggle active nav tab
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));

    // Show/hide bottom nav — hide it for full-screen overlay pages
    const bottomNav = document.querySelector('.bottom-nav');
    if (bottomNav) {
        bottomNav.style.display = (screenName === 'addons' || screenName === 'passenger' || screenName === 'seatmap') ? 'none' : '';
    }
    
    if (screenName === 'home') {
        document.getElementById('screenHome').classList.add('active');
        document.getElementById('navHome').classList.add('active');
        switchCategory(0); // Reset sliding tab visual indicator
        triggerLoyaltyPlaneAnimation();
    } else if (screenName === 'deals') {
        document.getElementById('screenDeals').classList.add('active');
        document.getElementById('navFlights').classList.remove('active'); // Deals is active
        document.getElementById('categoryTabsSection').querySelectorAll('.category-tab').forEach((t, idx) => {
            if (idx === 3) t.classList.add('active');
            else t.classList.remove('active');
        });
    } else if (screenName === 'trips') {
        document.getElementById('screenTrips').classList.add('active');
        document.getElementById('navTrips').classList.add('active');
    } else if (screenName === 'DestinationAI') {
        const aiScreen = document.getElementById('screenDestinationAI');
        if (aiScreen) aiScreen.classList.add('active');
    } else if (screenName === 'results') {
        const resultsScreen = document.getElementById('screenResults');
        if (resultsScreen) resultsScreen.classList.add('active');
        // Keep flights tab semi-active or no tab active to focus on results
        renderFlightResults();
    } else if (screenName === 'studentHub') {
        const studentScreen = document.getElementById('screenStudentHub');
        if (studentScreen) studentScreen.classList.add('active');
    } else if (screenName === 'passenger') {
        const passengerScreen = document.getElementById('screenPassenger');
        if (passengerScreen) passengerScreen.classList.add('active');
    }
    
    // Globally hide passenger form when navigating away from passenger screen
    const pForm = document.getElementById('paxDetailsDrawerModal');
    if (pForm) {
        if (screenName === 'passenger') {
            pForm.style.display = 'block';
        } else {
            pForm.style.display = 'none';
        }
    }
    
    const savedPaxSheet = document.getElementById('savedPassengersSheet');
    if (savedPaxSheet) {
        if (screenName === 'passenger') {
            savedPaxSheet.style.display = 'block';
        } else {
            savedPaxSheet.style.display = 'none';
        }
    }
    
    const travelersSheet = document.getElementById('travelersSheetDrawer');
    if (travelersSheet) {
        if (screenName === 'home') {
            travelersSheet.style.display = 'block';
        } else {
            travelersSheet.style.display = 'none';
        }
    }
    
        if (screenName === 'addons') {
            const addonsScreen = document.getElementById('screenAddons');
            if (addonsScreen) {
                const iphoneScreen = document.querySelector('.iphone-screen');
                if (iphoneScreen && addonsScreen.parentElement !== iphoneScreen) iphoneScreen.appendChild(addonsScreen);
                addonsScreen.classList.add('active');
                document.querySelectorAll('.bottom-sheet-drawer').forEach(dr => dr.classList.remove('visible'));
                const bd = document.getElementById('bottomSheetBackdrop');
                if (bd) bd.classList.remove('visible');
                initAddonsScreen();
            }
        }
        
        if (screenName === 'seatmap') {
            const seatmapScreen = document.getElementById('screenSeatMap');
            if (seatmapScreen) {
                const iphoneScreen = document.querySelector('.iphone-screen');
                if (iphoneScreen && seatmapScreen.parentElement !== iphoneScreen) iphoneScreen.appendChild(seatmapScreen);
                seatmapScreen.classList.add('active');
                initSeatMapScreen();
            }
        }
        
        if (screenName === 'payments') {
            const payScreen = document.getElementById('screenPayments');
            if (payScreen) {
                const iphoneScreen = document.querySelector('.iphone-screen');
                if (iphoneScreen && payScreen.parentElement !== iphoneScreen) iphoneScreen.appendChild(payScreen);
                payScreen.classList.add('active');
                if (typeof initPaymentsScreen === 'function') initPaymentsScreen();
            }
        }

    // Sync screen switcher button highlights in Sidebar
    document.querySelectorAll('.dev-simulator-console .dev-btn-stack button').forEach(btn => {
        if (!btn.id.startsWith('btnState')) {
            btn.classList.remove('active');
        }
    });
    
    if (screenName === 'home') {
        const homeBtn = document.getElementById('btnDevNavHome');
        if (homeBtn) homeBtn.classList.add('active');
    } else if (screenName === 'deals') {
        const dealsBtn = document.getElementById('devNavDeals');
        if (dealsBtn) dealsBtn.classList.add('active');
        } else if (screenName === 'trips') {
            const tripsBtn = document.getElementById('devNavTrips');
            if (tripsBtn) tripsBtn.classList.add('active');
        }
    } catch(e) {
        alert("Navigation Error: " + e.message + "\nStack: " + e.stack);
        console.error("Navigation Error:", e);
    }
}

// ==========================================================================
// CATEGORY TABS INTERACTION
// ==========================================================================

function switchCategory(index) {
    appState.activeCategoryIndex = index;
    
    const tabs = document.getElementById('categoryTabsSection').querySelectorAll('.category-tab');
    
    tabs.forEach((tab, idx) => {
        if (idx === index) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });
    
    // Ripple haptic effect
    triggerHaptic('light', `Category Tab changed: ${tabs[index].innerText}`);

    // If changing category to "Deals" via home tabs
    if (index === 3) {
        setTimeout(() => navigateTo('deals'), 250);
    }
}

// ==========================================================================
// ROUTE SELECTION & DRAWER SYSTEM
// ==========================================================================

function openAirportSelector(target) {
    appState.airportSelectorTarget = target;
    
    triggerHaptic('medium', `Open selector drawer for: ${target.toUpperCase()}`);
    
    const backdrop = document.getElementById('bottomSheetBackdrop');
    const drawer = document.getElementById('bottomSheetDrawer');
    const searchInput = document.getElementById('airportSearchInput');
    const title = document.getElementById('drawerTitle');
    
    title.innerText = target === 'from' ? 'Departing From' : 'Flying To';
    searchInput.value = '';
    
    backdrop.classList.add('visible');
    drawer.classList.add('visible');
    
    filterAirports(''); // Load all airports
    
    setTimeout(() => searchInput.focus(), 250);
}

function closeAirportSelector() {
    triggerHaptic('light', 'Close selector drawer');
    
    const backdrop = document.getElementById('bottomSheetBackdrop');
    const drawer = document.getElementById('bottomSheetDrawer');
    
    backdrop.classList.remove('visible');
    drawer.classList.remove('visible');
}

function filterAirports() {
    const query = document.getElementById('airportSearchInput').value.toLowerCase().trim();
    const listContainer = document.getElementById('airportList');
    listContainer.innerHTML = '';
    
    const filtered = airports.filter(ap => 
        ap.city.toLowerCase().includes(query) || 
        ap.code.toLowerCase().includes(query) || 
        ap.name.toLowerCase().includes(query)
    );
    
    if (filtered.length === 0) {
        listContainer.innerHTML = '<div style="padding:20px; text-align:center; font-size:12px; color:#888;">No airports found</div>';
        return;
    }
    
    filtered.forEach(ap => {
        // Prevent selecting same city for from and to
        const isSelectedFrom = appState.selectedFrom && appState.selectedFrom.code === ap.code;
        const isDisabled = (appState.airportSelectorTarget === 'to' && isSelectedFrom);
        
        const option = document.createElement('div');
        option.className = 'airport-option';
        if (isDisabled) {
            option.style.opacity = '0.3';
            option.style.pointerEvents = 'none';
        }
        
        option.innerHTML = `
            <div class="airport-option-details">
                <span class="airport-city">${ap.city}</span>
                <span class="airport-name">${ap.name}</span>
            </div>
            <span class="airport-code-badge">${ap.code}</span>
        `;
        
        option.onclick = () => selectAirport(ap);
        listContainer.appendChild(option);
    });
}

function selectAirport(airport) {
    const homeContent = document.getElementById('homeContentContainer');
    
    if (appState.airportSelectorTarget === 'from') {
        appState.selectedFrom = airport;
        document.getElementById('valFromCode').innerText = airport.city;
        triggerHaptic('success', `Origin Set: ${airport.code}`);
        
        // If Origin is set to Delhi, trigger layout change (Trending destinations slides up!)
        if (airport.code === 'DEL') {
            homeContent.classList.add('route-selected');
            document.getElementById('userGreeting').innerText = 'Delhi';
        } else {
            homeContent.classList.remove('route-selected');
            document.getElementById('userGreeting').innerText = 'Hi Nihar!';
        }
    } else {
        appState.selectedTo = airport;
        document.getElementById('valToCode').innerText = airport.city;
        triggerHaptic('success', `Destination Set: ${airport.code}`);
    }
    
    updateSearchButtonState();
    closeAirportSelector();
}

function updateSearchButtonState() {
    const searchBtn = document.getElementById('searchFlightsBtn');
    if (!searchBtn) return;
    searchBtn.disabled = false;
}

function swapRoutes() {
    if (!appState.selectedTo && !appState.selectedFrom) {
        triggerHaptic('error', 'Select route parameters to swap');
        return;
    }
    
    triggerHaptic('heavy', 'Swap Routes');
    
    const temp = appState.selectedFrom;
    appState.selectedFrom = appState.selectedTo;
    appState.selectedTo = temp;
    
    // Update displays
    document.getElementById('valFromCode').innerText = appState.selectedFrom ? appState.selectedFrom.city : 'Select City';
    document.getElementById('valToCode').innerText = appState.selectedTo ? appState.selectedTo.city : 'Select City';
    
    // Trigger layout shift if Delhi is now the source
    const homeContent = document.getElementById('homeContentContainer');
    if (appState.selectedFrom && appState.selectedFrom.code === 'DEL') {
        homeContent.classList.add('route-selected');
        document.getElementById('userGreeting').innerText = 'Delhi';
    } else {
        homeContent.classList.remove('route-selected');
        document.getElementById('userGreeting').innerText = appState.selectedFrom ? 'Hi Nihar!' : 'Hi Nihar!';
    }

    updateSearchButtonState();
    
    // Animate swap button rotation
    const btn = document.querySelector('.swap-route-btn');
    btn.style.transform = 'translate(-50%, -50%) rotate(180deg)';
    setTimeout(() => {
        btn.style.transform = 'translate(-50%, -50%) rotate(0deg)';
    }, 400);
}

function searchFlights() {
    if (!appState.selectedFrom) appState.selectedFrom = { code: 'DEL', city: 'Delhi' };
    if (!appState.selectedTo) appState.selectedTo = { code: 'BOM', city: 'Mumbai' };
    if (false) {
        triggerHaptic('error', 'Incomplete route parameters');
        alert('Please select both From and Where to? cities to search flights!');
        return;
    }
    
    // Sync student mode with persona state if triggered from home page
    if (typeof isStudentPersonaActive !== 'undefined') {
        isStudentMode = isStudentPersonaActive;
    }
    
    triggerHaptic('success', 'Searching Flights...');
    
    const dateLabel = document.getElementById('valDateText').innerText;
    const travelersLabel = document.getElementById('valTravelersText').innerText;
    
    // Dynamic Island notification showing real flight details
    triggerDynamicIsland(
        `Searching: ${appState.selectedFrom.code} to ${appState.selectedTo.code}`,
        `${dateLabel} • ${travelersLabel}`,
        'Search'
    );
    
    // Show Cockpit Interstitial Takeover
    const cockpit = document.getElementById('cockpitInterstitial');
    const tagline = document.getElementById('cockpitTagline');
    
    if (cockpit) {
        cockpit.classList.add('visible');
        if (tagline) {
            // Reset and trigger typewriter animation
            tagline.classList.remove('typewriter');
            void tagline.offsetWidth; // trigger reflow
            tagline.classList.add('typewriter');
        }
        
        triggerHaptic('heavy', 'Taking off');
        
        // Hide cockpit and show results after 2.6s
        setTimeout(() => {
            cockpit.classList.remove('visible');
            navigateTo('results');
        }, 2600);
    } else {
        // Fallback if HTML is missing
        setTimeout(() => {
            navigateTo('results');
        }, 1500);
    }
}

function selectDestination(code, city) {
    triggerHaptic('medium', 'Destination Selected');
    
    // Set text fields in the new AI Destination screen
    document.getElementById('aiDestCityName').innerText = city;
    document.getElementById('aiDestTitleCity').innerText = city;
    
    // Optionally map the image
        const heroImg = document.getElementById('aiDestHeroImg');
    const heroVideo = document.getElementById('aiDestHeroVideo');
    const genericVideoUrl = "https://assets.mixkit.co/videos/preview/mixkit-aerial-view-of-city-traffic-at-night-11-large.mp4";
    
    // We can pause video if it's currently playing
    if (heroVideo) {
        heroVideo.pause();
    }

    if (code === 'BLR' || city === 'Bangalore' || city === 'Bengaluru') {
        heroImg.style.backgroundImage = "url('blr_flower_market.png')";
        if(heroVideo) { heroVideo.poster = 'blr_flower_market.png'; }
        document.getElementById('aiDestTitleCountry').innerText = 'India';
        document.getElementById('aiDestDescription').innerText = 'Bengaluru, often referred to as the "Silicon Valley of India," is a bustling metropolis known for its thriving IT industry and cosmopolitan vibe. The city is a blend of modernity and tradition, with verdant parks like Cubbon Park offering tranquil retreats amidst urban sprawl.';
        document.getElementById('aiRouteText').innerText = 'SIN ⇄ BLR • 1 ADULT';
    } else if (code === 'DXB') {
        heroImg.style.backgroundImage = "url('https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=600&h=400&fit=crop')";
        if(heroVideo) { heroVideo.poster = 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=600&h=400&fit=crop'; }
        document.getElementById('aiDestTitleCountry').innerText = 'UAE';
        document.getElementById('aiDestDescription').innerText = 'Dubai is a city of superlatives, home to the world’s tallest building, the Burj Khalifa, and sprawling futuristic architecture. Experience luxury shopping, ultra-modern attractions, and a vibrant nightlife in this desert oasis.';
        document.getElementById('aiRouteText').innerText = 'DEL ⇄ DXB • 1 ADULT';
    } else if (code === 'BKK') {
        heroImg.style.backgroundImage = "url('https://images.unsplash.com/photo-1508009603885-247a505979c3?w=600&h=400&fit=crop')";
        if(heroVideo) { heroVideo.poster = 'https://images.unsplash.com/photo-1508009603885-247a505979c3?w=600&h=400&fit=crop'; }
        document.getElementById('aiDestTitleCountry').innerText = 'Thailand';
        document.getElementById('aiDestDescription').innerText = 'Bangkok is a sensory overload of vibrant street life, ornate shrines, and bustling floating markets. A paradise for food lovers and culture seekers, blending ancient traditions with a rapid modern pulse.';
        document.getElementById('aiRouteText').innerText = 'DEL ⇄ BKK • 1 ADULT';
    } else if (code === 'DPS') {
        heroImg.style.backgroundImage = "url('https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&h=400&fit=crop')";
        if(heroVideo) { heroVideo.poster = 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&h=400&fit=crop'; }
        document.getElementById('aiDestTitleCountry').innerText = 'Indonesia';
        document.getElementById('aiDestDescription').innerText = 'Bali is an Indonesian island known for its forested volcanic mountains, iconic rice paddies, beaches and coral reefs. The island is home to religious sites such as cliffside Uluwatu Temple.';
        document.getElementById('aiRouteText').innerText = 'BOM ⇄ DPS • 1 ADULT';
    } else {
        // Fallback for Singapore or others
        heroImg.style.backgroundImage = "url('https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=600&h=400&fit=crop')";
        if(heroVideo) { heroVideo.poster = 'https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=600&h=400&fit=crop'; }
        document.getElementById('aiDestTitleCountry').innerText = city;
        document.getElementById('aiDestDescription').innerText = 'Discover the beautiful sights, incredible culture, and amazing cuisine that awaits you.';
        document.getElementById('aiRouteText').innerText = `DEL ⇄ ${code} • 1 ADULT`;
    }
    
    // Play the video
    if (heroVideo) {
        heroVideo.src = genericVideoUrl;
        heroVideo.play().catch(e => console.log("Autoplay prevented:", e));
    }

    
    // Clear old cards and generate 10 new flight cards
    const flightList = document.getElementById('aiFlightList');
    flightList.innerHTML = '';
    
    
    // Generate dates based on today + some offset
    const today = new Date();
    
    for (let i = 0; i < 10; i++) {
        // Date math
        const startDate = new Date(today);
        startDate.setDate(today.getDate() + 10 + (i * 7)); // start 10 days out, increment by 1 week
        const endDate = new Date(startDate);
        endDate.setDate(startDate.getDate() + 4); // 4 day trip
        
        const formatOptions = { weekday: 'short', day: 'numeric', month: 'short' };
        const startStr = startDate.toLocaleDateString('en-GB', formatOptions);
        const endStr = endDate.toLocaleDateString('en-GB', formatOptions);
        
        // Price math
        const basePrice = 300 + (Math.random() * 200);
        const priceStr = basePrice.toFixed(1);
        
        const cardHtml = `
            <div class="ai-flight-card" id="ai-card-${i}" onclick="searchFlights()">
                <div class="ai-flight-left">
                    <span class="ai-flight-dates">${startStr} - ${endStr}</span>
                    <span class="ai-flight-class">ECONOMY</span>
                </div>
                <div class="ai-flight-right">
                    <div class="ai-flight-price-box">
                        <div class="ai-flight-price-lbl">From SGD</div>
                        <div class="ai-flight-price-val">${priceStr}</div>
                    </div>
                    <div class="ai-flight-arrow">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    </div>
                </div>
            </div>
        `;
        flightList.insertAdjacentHTML('beforeend', cardHtml);
    }
    
    // Navigate to the AI Destination Screen
    navigateTo('DestinationAI');
    
    // Trigger staggered animation after a short delay so screen transition occurs first
    setTimeout(() => {
        animateFlightCardsUp();
    }, 200);
}

function animateFlightCardsUp() {
    const cards = document.querySelectorAll('.ai-flight-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('animate-in');
            if (index % 3 === 0) triggerHaptic('light', 'Card Load');
        }, index * 80); // 80ms stagger
    });
}

function closeDestinationAI() {
    triggerHaptic('light', 'Close AI Destination');
    // Pause video
    const heroVideo = document.getElementById('aiDestHeroVideo');
    if (heroVideo) {
        heroVideo.pause();
    }
    // Remove animate class so they can be re-animated next time
    const cards = document.querySelectorAll('.ai-flight-card');
    cards.forEach(card => card.classList.remove('animate-in'));
    navigateTo('home');
}


function filterDeals(category) {
    triggerHaptic('light', `Filter deals: ${category}`);
    
    document.querySelectorAll('.pop-filter-pill').forEach(pill => {
        if (category === 'all' && pill.innerText === 'All') {
            pill.classList.add('active');
        } else if (pill.innerText.toLowerCase() === category.toLowerCase()) {
            pill.classList.add('active');
        } else {
            pill.classList.remove('active');
        }
    });
    
    const cards = document.querySelectorAll('.pop-offer-card');
    cards.forEach(card => {
        if (category === 'all' || card.getAttribute('data-category') === category) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}

function toggleRecentSearches() {
    const list = document.getElementById('recentSearchesList');
    const arrow = document.getElementById('recentToggleArrow');
    const isCollapsed = list.classList.toggle('collapsed');
    arrow.innerText = isCollapsed ? 'Show' : 'Hide';
    triggerHaptic('light', isCollapsed ? 'Collapse Recent Searches' : 'Expand Recent Searches');
}

function selectRecentSearch(from, to) {
    const fromAp = airports.find(ap => ap.code === from);
    const toAp = airports.find(ap => ap.code === to);
    if (fromAp && toAp) {
        appState.selectedFrom = fromAp;
        appState.selectedTo = toAp;
        document.getElementById('valFromCode').innerText = fromAp.city;
        document.getElementById('valToCode').innerText = toAp.city;
        
        const homeContent = document.getElementById('homeContentContainer');
        if (from === 'DEL') {
            homeContent.classList.add('route-selected');
            document.getElementById('userGreeting').innerText = 'Delhi';
        } else {
            homeContent.classList.remove('route-selected');
            document.getElementById('userGreeting').innerText = 'Hi Nihar!';
        }

        updateSearchButtonState();
        triggerHaptic('success', `Recent Search Selected: ${from} to ${to}`);
        
        // Scroll to search inputs
        document.getElementById('appContent').scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// ==========================================================================
// DYNAMIC COMPANION CARD SYSTEM & STATE MACHINE
// ==========================================================================

function setFlightState(state) {
    appState.flightState = state;
    
    // Highlight correct dev cockpit buttons
    document.querySelectorAll('.dev-simulator-console button[id^="btnState"]').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const targetBtnId = {
        'upcoming_trip': 'btnStateUpcomingTrip',
        'checkin_open': 'btnStateCheckinOpen',
        'checked_in': 'btnStateCheckedIn',
        'gate_open': 'btnStateGateOpen',
        'airport_checkin': 'btnStateAirportCheckin',
        'go_to_counter': 'btnStateGoToCounter',
        'gate_update': 'btnStateGateUpdate',
        'delayed': 'btnStateDelayed',
        'cancelled': 'btnStateCancelled',
        'baggage_tracking': 'btnStateBaggage'
    }[state];
    
    if (targetBtnId) {
        document.getElementById(targetBtnId).classList.add('active');
    }

    // Render the custom content based on state
    renderFlightStateCard(state);
    
    // Update the timeline milestones
    if (typeof updateTimelineState === 'function') {
        updateTimelineState(state);
    }
}

function renderFlightStateCard(state) {
    const container = document.getElementById('companionSubcardContent');
    if (!container) return;
    
    let html = '';
    
    if (state === 'upcoming_trip') {
        html = `
            <div class="state-title-row">
                <span class="state-title" style="color: #0f172a;">Upcoming Trip</span>
                <span class="state-date" style="color: #64748b;">15 Days to go</span>
            </div>
            <p class="state-desc" style="color: #475569; font-weight: 500;">
                Online check-in opens 48hrs before departure.
            </p>
            
            <div style="margin: 20px 0; display: flex; align-items: center; justify-content: space-between; position: relative;">
                <div style="position: absolute; top: 50%; left: 16px; right: 16px; height: 2px; background: #e2e8f0; transform: translateY(-50%); z-index: 1;"></div>
                <div style="position: absolute; top: 50%; left: 16px; width: 10%; height: 2px; background: var(--xairline-blue); transform: translateY(-50%); z-index: 2;"></div>
                
                <div style="z-index: 3; display: flex; flex-direction: column; align-items: center;">
                    <div style="width: 14px; height: 14px; border-radius: 50%; background: var(--xairline-blue); box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.2);"></div>
                    <div style="font-size: 10px; font-weight: 700; color: var(--xairline-navy); margin-top: 6px; white-space: nowrap;">Booked</div>
                </div>
                
                <div style="z-index: 3; display: flex; flex-direction: column; align-items: center;">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: #e2e8f0; border: 2px solid white;"></div>
                    <div style="font-size: 10px; font-weight: 600; color: #64748b; margin-top: 6px; white-space: nowrap;">Check-in (13 Days)</div>
                </div>
                
                <div style="z-index: 3; display: flex; flex-direction: column; align-items: center;">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: #e2e8f0; border: 2px solid white;"></div>
                    <div style="font-size: 10px; font-weight: 600; color: #64748b; margin-top: 6px; white-space: nowrap;">Depart</div>
                </div>
            </div>

            <div class="action-row-buttons">
                <button class="btn-secondary-action" onclick="alert('Manage Booking clicked')" style="width: 100%; justify-content: center; background: #f8fafc; color: var(--xairline-navy); border: 1px solid #e2e8f0;">Manage Booking</button>
            </div>
        `;
        triggerHaptic('light', 'Companion State: Upcoming Trip');
        triggerDynamicIsland('Upcoming Trip', '15 days to go', 'Booked');
        
    } else if (state === 'checkin_open') {
        html = `
            <div class="state-title-row">
                <span class="state-title">Check-in Open</span>
                <span class="state-date">24 APRIL | 12:30 PM IST</span>
            </div>
            <p class="state-desc">Check-in closes in 1h 10m – act fast</p>
            <div class="action-row-buttons">
                <button class="btn-primary-action" onclick="runCheckinVerify()">Check in ➔</button>
            </div>
        `;
        triggerHaptic('light', 'Companion State: Check-in Open');
        triggerDynamicIsland('Check-in Open', 'Online check-in closes in 1h 10m', 'Check-in');
        
    } else if (state === 'baggage_tracking') {
        html = `
            <div onclick="openBaggageTracking()" style="padding: 16px; margin: -16px; cursor: pointer;">
                <div class="state-title-row" style="margin-bottom: 12px;">
                    <span class="state-title" style="color: #001b94;">Baggage Tracking</span>
                    <span class="state-date" style="color: #10b981;">In Progress</span>
                </div>
                <div class="baggage-mini-timeline" id="baggageMiniTimeline">
                    <div style="position: relative; width: 100%; display: flex; justify-content: space-between; align-items: center; padding-top: 12px; padding-bottom: 24px;">
                        <div style="position: absolute; top: 16px; left: 10px; right: 10px; height: 2px; background: #e2e8f0; z-index: 1;"></div>
                        <div style="position: absolute; top: 16px; left: 10px; width: 50%; height: 2px; background: #10b981; z-index: 2;"></div>
                        
                        <div class="bag-node active" style="z-index: 3; position: relative;">
                            <div class="dot" style="width: 10px; height: 10px; border-radius: 50%; background: #10b981; margin: 0 auto; box-shadow: 0 0 0 4px #d1fae5;"></div>
                            <div style="position: absolute; top: 16px; left: 50%; transform: translateX(-50%); font-size: 8px; font-weight: 700; color: #64748b; white-space: nowrap;">Received</div>
                        </div>
                        <div class="bag-node active" style="z-index: 3; position: relative;">
                            <div class="dot" style="width: 10px; height: 10px; border-radius: 50%; background: #10b981; margin: 0 auto; box-shadow: 0 0 0 4px #d1fae5;"></div>
                            <div style="position: absolute; top: 16px; left: 50%; transform: translateX(-50%); font-size: 8px; font-weight: 700; color: #64748b; white-space: nowrap;">Loaded</div>
                        </div>
                        <div class="bag-node current" style="z-index: 3; position: relative;">
                            <div class="dot glowing" style="width: 12px; height: 12px; border-radius: 50%; background: #0066FF; margin: -1px auto 0; box-shadow: 0 0 0 4px rgba(0, 102, 255, 0.2); animation: pulseDot 2s infinite;"></div>
                            <svg class="bag-plane-anim" viewBox="0 0 24 24" width="16" height="16" fill="currentColor" style="position: absolute; top: -14px; left: 50%; transform-origin: center; animation: orbitPlane 2s linear infinite; color: #001b94; pointer-events: none;"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg>
                            <div style="position: absolute; top: 16px; left: 50%; transform: translateX(-50%); font-size: 8px; font-weight: 800; color: #0f172a; white-space: nowrap;">Transfer</div>
                        </div>
                        <div class="bag-node" style="z-index: 3; position: relative;">
                            <div class="dot" style="width: 10px; height: 10px; border-radius: 50%; background: #cbd5e1; border: 2px solid #fff; margin: 0 auto;"></div>
                            <div style="position: absolute; top: 16px; left: 50%; transform: translateX(-50%); font-size: 8px; font-weight: 600; color: #94a3b8; white-space: nowrap;">Offloaded</div>
                        </div>
                        <div class="bag-node" style="z-index: 3; position: relative;">
                            <div class="dot" style="width: 10px; height: 10px; border-radius: 50%; background: #cbd5e1; border: 2px solid #fff; margin: 0 auto;"></div>
                            <div style="position: absolute; top: 16px; left: 50%; transform: translateX(-50%); font-size: 8px; font-weight: 600; color: #94a3b8; white-space: nowrap;">Belt A21</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        triggerHaptic('light', 'Companion State: Baggage Tracking');
        triggerDynamicIsland('Baggage Transferred', 'BOM Terminal 2', 'Baggage Tracking');
        
    } else if (state === 'checked_in') {
        html = `
            <div class="state-title-row">
                <span class="state-title">Status: Checked in</span>
                <span class="state-date">24 APRIL | 12:30 PM IST</span>
            </div>
            
            <div class="state-details-grid">
                <div class="detail-block">
                    <span class="detail-lbl">Passenger</span>
                    <span class="detail-val">Ishika Pachori</span>
                </div>
                <div class="detail-block">
                    <span class="detail-lbl">Seat</span>
                    <span class="detail-val">17F</span>
                </div>
                <div class="detail-block">
                    <span class="detail-lbl">Class</span>
                    <span class="detail-val">Economy</span>
                </div>
                <div class="barcode-thumbnail-box">
                    <div class="barcode-mini-lines"></div>
                </div>
            </div>

            <div class="action-row-buttons">
                <button class="btn-glass-action" onclick="triggerHaptic('light', 'Download Pass')">Download Pass</button>
                <button class="btn-primary-action" onclick="triggerHaptic('success', 'Boarding pass ready'); navigateTo('trips');">View Boarding Pass</button>
            </div>
        `;
        triggerHaptic('success', 'Companion State: Checked In');
        triggerDynamicIsland('Check-in Completed', 'Seat 17F • Boarding Pass Ready', 'Checked In');
        
    } else if (state === 'gate_open') {
        html = `
            <div class="state-title-row">
                <span class="state-title warning-text">Status: Gate 43 - Open</span>
                <span class="state-date">24 APRIL | 12:30 PM IST</span>
            </div>

            <div class="state-details-grid">
                <div class="detail-block">
                    <span class="detail-lbl">Passenger</span>
                    <span class="detail-val">Ishika Pachori</span>
                </div>
                <div class="detail-block">
                    <span class="detail-lbl">Seat</span>
                    <span class="detail-val">17F</span>
                </div>
                <div class="detail-block">
                    <span class="detail-lbl">Boarding Starts In</span>
                    <span class="detail-val" id="countdownTimer" style="color: var(--xairline-accent);">45m 00s</span>
                </div>
                <div class="barcode-thumbnail-box">
                    <div class="barcode-mini-lines"></div>
                </div>
            </div>

            <div class="action-row-buttons">
                <button class="btn-glass-action" onclick="triggerHaptic('light', 'Download Pass')">Download Pass</button>
            </div>
        `;
        triggerHaptic('heavy', 'Companion State: Boarding Gate 43 Open');
        triggerDynamicIsland('Boarding Started', 'Gate 43 is active • Proceed for Scan', 'Boarding');
        startBoardingTimer();
        
    } else if (state === 'airport_checkin') {
        html = `
            <div class="state-title-row">
                <span class="state-title">Check-in at Airport</span>
                <span class="state-date">24 APRIL | 12:30 PM IST</span>
            </div>
            <p class="state-desc">Web check-in is closed. Please check-in at the airport counter.</p>
            <div class="action-row-buttons">
                <button class="btn-primary-action" onclick="triggerHaptic('medium', 'Manage Booking')">Manage Booking ➔</button>
            </div>
        `;
        triggerHaptic('light', 'Companion State: Web Check-in Closed');
        triggerDynamicIsland('Web Check-in Closed', 'Proceed to airport desk for check-in', 'Airport Desk');
        
    } else if (state === 'go_to_counter') {
        html = `
            <div class="state-title-row">
                <span class="state-title">Go to Counter</span>
                <span class="state-date">24 APRIL | 12:30 PM IST</span>
            </div>
            <p class="state-desc">Online check-in is not available for this booking. Please visit the airport assistance desk.</p>
            <div class="action-row-buttons">
                <button class="btn-glass-action" onclick="triggerHaptic('light', 'View Details')">View Details ➔</button>
            </div>
        `;
        triggerHaptic('medium', 'Companion State: Go to Counter');
        triggerDynamicIsland('Online Check-in Unavailable', 'Go to airline counter for assist', 'Counter');
        
    } else if (state === 'gate_update') {
        html = `
            <div class="state-title-row">
                <span class="state-title warning-text">Gate Update: Gate 21 ➔ Gate 43</span>
                <span class="state-date">24 APRIL | 12:30 PM IST</span>
            </div>
            <p class="state-desc">Your boarding gate has changed. Please proceed directly to Gate 43.</p>
            
            <div class="action-row-buttons">
                <button class="btn-glass-action" onclick="triggerHaptic('light', 'Download Pass')">Download Pass</button>
                <button class="btn-primary-action" onclick="triggerHaptic('light', 'Confirm Gate')">OK, Understood</button>
            </div>
        `;
        triggerHaptic('heavy', 'Companion State: Gate Changed Warning');
        triggerDynamicIsland('Gate Changed', 'Gate 21 changed to Gate 43', 'Gate 43');
        
    } else if (state === 'delayed') {
        html = `
            <div class="state-title-row">
                <span class="state-title warning-text">Flight status: Delayed</span>
                <span class="state-date">25 APRIL | 12:20 PM IST</span>
            </div>
            <p class="state-desc">Flight time has changed – new departure below</p>
            
            <div class="delay-comparison-row">
                <span class="time-original">12:30 PM</span>
                <span class="time-revised-glow">➔ 02:30 PM</span>
            </div>

            <div class="action-row-buttons" style="margin-top: 6px;">
                <button class="btn-primary-action" onclick="triggerHaptic('light', 'View Pass')">View Boarding Pass ➔</button>
            </div>
        `;
        triggerHaptic('heavy', 'Companion State: Delayed Warning');
        triggerDynamicIsland('Flight Delayed', 'Delayed 2 hours • Est: 14:30', 'Delayed');
        
    } else if (state === 'cancelled') {
        html = `
            <div class="state-title-row">
                <span class="state-title error-text">Flight status: Cancelled</span>
                <span class="state-date">25 APRIL | 12:20 PM IST</span>
            </div>
            <p class="state-desc">This flight has been cancelled by the airline due to operational constraints.</p>
            <div class="action-row-buttons">
                <button class="btn-primary-action" onclick="triggerHaptic('heavy', 'Manage refund')">Manage Booking ➔</button>
            </div>
        `;
        triggerHaptic('error', 'Companion State: Flight Cancelled Severe Warning');
        triggerDynamicIsland('Flight Cancelled', '6E 2015 cancelled • Free refund/change', 'Cancelled');
    }
    
    container.innerHTML = html;
}

// Security Check-in Loading Simulation
function runCheckinVerify() {
    const container = document.getElementById('companionSubcardContent');
    if (!container) return;
    
    container.innerHTML = `
        <div class="state-title-row">
            <span class="state-title">Processing Check-in...</span>
        </div>
        <p class="state-desc">Assigning priority seat and verifying credentials...</p>
        <div style="width: 100%; height: 2px; background: rgba(0,31,84,0.06); border-radius: 2px; overflow: hidden; margin-top: 8px;">
            <div style="width: 50%; height: 100%; background: var(--xairline-blue); animation: pulse 1s infinite alternate;"></div>
        </div>
    `;
    
    triggerHaptic('medium', 'Running credentials verify');
    triggerDynamicIsland('Assigning Seat', 'Searching flight seat matrix...', 'Checking');
    
    setTimeout(() => {
        setFlightState('checked_in');
    }, 1500);
}

// Boarding Gate Active countdown timer
let timerInterval = null;
function startBoardingTimer() {
    if (timerInterval) clearInterval(timerInterval);
    
    let minutes = 45;
    let seconds = 0;
    
    timerInterval = setInterval(() => {
        if (appState.flightState !== 'gate_open') {
            clearInterval(timerInterval);
            return;
        }
        
        if (seconds === 0) {
            if (minutes === 0) {
                clearInterval(timerInterval);
                const timerNode = document.getElementById('countdownTimer');
                if (timerNode) timerNode.innerText = 'Boarding Closed';
                return;
            }
            minutes--;
            seconds = 59;
        } else {
            seconds--;
        }
        
        const mStr = minutes < 10 ? '0' + minutes : minutes;
        const sStr = seconds < 10 ? '0' + seconds : seconds;
        const timerNode = document.getElementById('countdownTimer');
        if (timerNode) {
            timerNode.innerText = `${mStr}m ${sStr}s`;
        }
    }, 1000);
}

// ==========================================================================
// DYNAMIC ISLAND MICRO-INTERACTIONS
// ==========================================================================

let islandTimeout = null;

function triggerDynamicIsland(headline, subline, badgeText) {
    const island = document.getElementById('dynamicIsland');
    const headlineNode = document.getElementById('islandHeadline');
    const sublineNode = document.getElementById('islandSubline');
    const badgeNode = document.getElementById('islandBadge');
    
    if (!island) return;

    // Clear any pending collapse timers
    if (islandTimeout) {
        clearTimeout(islandTimeout);
    }
    
    // Setup text
    if (headlineNode) headlineNode.innerText = headline;
    if (sublineNode) sublineNode.innerText = subline;
    if (badgeNode) badgeNode.innerText = badgeText;
    
    // Animate expand
    island.classList.add('expanded');
    
    // Automatically shrink after 4.5 seconds
    islandTimeout = setTimeout(() => {
        island.classList.remove('expanded');
    }, 4500);
}

function toggleIslandExpansion() {
    const island = document.getElementById('dynamicIsland');
    if (!island) return;
    
    const isExpanded = island.classList.contains('expanded');
    
    triggerHaptic('light', isExpanded ? 'Collapse Dynamic Island' : 'Expand Dynamic Island');
    
    if (isExpanded) {
        island.classList.remove('expanded');
    } else {
        island.classList.add('expanded');
    }
}

// ==========================================================================
// CAROUSEL DOTS SYNC, SIRI VOICE SEARCH, PARALLAX SCROLL & OSCILLOSCOPE
// ==========================================================================

// Flight Simulator Configuration
const cityCoordinates = {
    'DEL': { x: 185, y: 135, name: 'Delhi', airport: 'Indira Gandhi Int\'l', temp: '34°C', flights: 96 },
    'MUM': { x: 170, y: 170, name: 'Mumbai', airport: 'Chhatrapati Shivaji Int\'l', temp: '30°C', flights: 78 },
    'LON': { x: 75, y: 85, name: 'London', airport: 'Heathrow Airport', temp: '17°C', flights: 15 },
    'AMST': { x: 115, y: 75, name: 'Amsterdam', airport: 'Schiphol Airport', temp: '15°C', flights: 8 },
    'GAU': { x: 230, y: 130, name: 'Guwahati', airport: 'Lokpriya Gopinath Bordoloi', temp: '28°C', flights: 32 }
};

const flightSequence = ['DEL', 'MUM', 'GAU', 'LON', 'AMST'];
let currentCity = 'DEL';
let flightAnimationId = null;
let flightTimeoutId = null;
let isExploring = false;

// Initialize Offers Carousel as a 3D Curved Coverflow (Visible Left/Right Cards)
function init3DCurvedCoverflow(carouselId, dotsContainerId, cardWidth, cardHeight) {
    const carousel = document.getElementById(carouselId);
    const dotsContainer = document.getElementById(dotsContainerId);
    if (!carousel || !dotsContainer) return;

    const viewport = carousel.parentElement;
    const slides = carousel.querySelectorAll('.carousel-slide, .trending-slide-card');
    const dots = dotsContainer.querySelectorAll('.dot');
    const N = slides.length;
    if (N === 0) return;

    let progress = 0; // Floating scroll progress
    let startX = 0;
    let startY = 0;
    let startProgress = 0;
    let dragDistance = 0;
    let isDragging = false;
    let lastTouchTime = 0;

    // Apply viewport styles
    viewport.style.perspective = '1000px';
    viewport.style.perspectiveOrigin = '50% 50%';
    viewport.style.overflow = 'visible';
    viewport.style.position = 'relative';
    viewport.style.touchAction = 'none';
    viewport.style.height = `${cardHeight}px`;

    carousel.style.transformStyle = 'preserve-3d';
    carousel.style.position = 'relative';
    carousel.style.width = '100%';
    carousel.style.height = `${cardHeight}px`;

    // Add touch-action to slides directly to ensure smooth mobile swipes
    slides.forEach(slide => {
        slide.style.touchAction = 'none';
        slide.setAttribute('draggable', 'false');
    });

    // Prevent default drag and selection behaviors
    viewport.addEventListener('dragstart', (e) => e.preventDefault());
    viewport.addEventListener('selectstart', (e) => e.preventDefault());

    function updateLayout(animate = true) {
        // Normalize progress
        let normalizedProgress = (progress % N + N) % N;
        let activeIndex = Math.round(normalizedProgress) % N;

        slides.forEach((slide, i) => {
            slide.style.position = 'absolute';
            slide.style.left = '50%';
            slide.style.top = '50%';
            slide.style.marginLeft = `-${cardWidth / 2}px`;
            slide.style.marginTop = `-${cardHeight / 2}px`;
            slide.style.width = `${cardWidth}px`;
            slide.style.height = `${cardHeight}px`;
            slide.style.transformStyle = 'preserve-3d';
            slide.style.backfaceVisibility = 'hidden';

            if (animate) {
                slide.style.transition = 'transform 0.5s cubic-bezier(0.2, 0.85, 0.3, 1), opacity 0.5s ease, border-color 0.4s ease, box-shadow 0.4s ease';
            } else {
                slide.style.transition = 'none';
            }

            // Calculate distance in circular layout
            let dist = i - normalizedProgress;
            while (dist > N/2) dist -= N;
            while (dist < -N/2) dist += N;

            // Math transformations for visible peeking cards
            let tx = dist * (cardWidth * 0.62); // Horizontal shift
            let ty = 0;
            let tz = -Math.abs(dist) * 80; // Depth pushback
            let ry = dist * -28; // Inward angle rotation
            let scale = 1.02 - Math.abs(dist) * 0.12;
            let opacity = 1.0 - Math.abs(dist) * 0.55;
            let zIndex = Math.round(10 - Math.abs(dist) * 5);

            slide.style.zIndex = `${zIndex}`;
            slide.style.opacity = `${opacity}`;
            slide.style.transform = `perspective(1000px) translateX(${tx}px) translateY(${ty}px) translateZ(${tz}px) rotateY(${ry}deg) scale(${scale})`;

            // Add highlights to center card
            if (i === activeIndex) {
                slide.classList.add('active-highlight');
            } else {
                slide.classList.remove('active-highlight');
            }
        });

        // Sync dots
        dots.forEach((dot, i) => {
            if (i === activeIndex) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }

    function captureClick(e) {
        e.stopPropagation();
        e.preventDefault();
        viewport.removeEventListener('click', captureClick, true);
    }

    function getCoordinates(e) {
        let clientX = 0;
        let clientY = 0;
        if (e.clientX !== undefined) {
            clientX = e.clientX;
            clientY = e.clientY;
        } else if (e.touches && e.touches.length > 0) {
            clientX = e.touches[0].clientX;
            clientY = e.touches[0].clientY;
        }
        return { clientX, clientY };
    }

    function handleStart(e) {
        isDragging = true;
        const coords = getCoordinates(e);
        startX = coords.clientX;
        startY = coords.clientY;
        startProgress = progress;
        dragDistance = 0;
        updateLayout(false);
    }

    function handleMove(e) {
        if (!isDragging) return;
        const coords = getCoordinates(e);
        const diffX = coords.clientX - startX;

        if (e.cancelable) {
            e.preventDefault();
        }

        dragDistance = diffX;
        const viewportWidth = viewport.offsetWidth || 360;
        progress = startProgress - (dragDistance / viewportWidth) * 1.5;
        updateLayout(false);
    }

    function handleEnd() {
        if (!isDragging) return;
        isDragging = false;

        // Snapping progress to integer
        let targetProgress = Math.round(progress);
        progress = targetProgress;
        
        // Wrap to keep clean bounds
        progress = (progress % N + N) % N;

        updateLayout(true);
        triggerHaptic('medium', `Coverflow snap to card ${Math.round(progress) + 1}`);

        // Click prevention
        if (Math.abs(dragDistance) > 10) {
            viewport.addEventListener('click', captureClick, true);
        }
    }

    // Touch event listeners for mobile devices
    viewport.addEventListener('touchstart', (e) => {
        lastTouchTime = Date.now();
        handleStart(e);
    }, { passive: true });

    viewport.addEventListener('touchmove', (e) => {
        handleMove(e);
    }, { passive: false });

    viewport.addEventListener('touchend', () => {
        handleEnd();
    });

    viewport.addEventListener('touchcancel', () => {
        handleEnd();
    });

    // Mouse event listeners for desktop devices
    viewport.addEventListener('mousedown', (e) => {
        if (e.button !== 0) return;
        
        // Avoid double trigger on touch devices that emulate mouse events
        if (Date.now() - lastTouchTime < 800) return;

        handleStart(e);

        const mouseMoveHandler = (ev) => {
            handleMove(ev);
        };
        const mouseUpHandler = () => {
            handleEnd();
            document.removeEventListener('mousemove', mouseMoveHandler);
            document.removeEventListener('mouseup', mouseUpHandler);
        };
        document.addEventListener('mousemove', mouseMoveHandler);
        document.addEventListener('mouseup', mouseUpHandler);
    });

    // Initial load
    updateLayout(false);
}

// Initialize Trending Destinations Carousel as a 3D Swiping Stack (Apple Wallet Style)
function init3DSwipingStack(carouselId, dotsContainerId, cardWidth, cardHeight) {
    const carousel = document.getElementById(carouselId);
    const dotsContainer = document.getElementById(dotsContainerId);
    if (!carousel || !dotsContainer) return;

    const viewport = carousel.parentElement;
    const slides = carousel.querySelectorAll('.trending-slide-card, .insta-story-card');
    const dots = dotsContainer.querySelectorAll('.dot');
    const N = slides.length;
    if (N === 0) return;

    let activeIndex = 0;
    let dragX = 0;
    let dragY = 0;
    let isDragging = false;
    let startX = 0;
    let startY = 0;
    let clickPrevented = false;
    let lastTouchTime = 0;

    // Apply viewport styles
    viewport.style.perspective = '1000px';
    viewport.style.perspectiveOrigin = '50% 50%';
    viewport.style.overflow = 'visible';
    viewport.style.position = 'relative';
    viewport.style.touchAction = 'none';
    viewport.style.height = `${cardHeight}px`;

    carousel.style.transformStyle = 'preserve-3d';
    carousel.style.position = 'relative';
    carousel.style.width = '100%';
    carousel.style.height = `${cardHeight}px`;

    // Enable touch actions on stack items
    slides.forEach(slide => {
        slide.style.touchAction = 'none';
        slide.setAttribute('draggable', 'false');
    });

    // Prevent default drag and selection behaviors
    viewport.addEventListener('dragstart', (e) => e.preventDefault());
    viewport.addEventListener('selectstart', (e) => e.preventDefault());

    function updateLayout(animate = true, swipingOffIndex = -1, flyDirection = 0) {
        slides.forEach((slide, i) => {
            slide.style.position = 'absolute';
            slide.style.left = '50%';
            slide.style.top = '50%';
            slide.style.marginLeft = `-${cardWidth / 2}px`;
            slide.style.marginTop = `-${cardHeight / 2}px`;
            slide.style.width = `${cardWidth}px`;
            slide.style.height = `${cardHeight}px`;
            slide.style.transformStyle = 'preserve-3d';
            slide.style.backfaceVisibility = 'hidden';

            if (animate) {
                slide.style.transition = 'transform 0.4s cubic-bezier(0.2, 0.85, 0.3, 1), opacity 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease';
            } else {
                slide.style.transition = 'none';
            }

            // If this slide is currently flying off-screen
            if (i === swipingOffIndex) {
                slide.style.transition = 'transform 0.35s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.3s ease';
                let tx = flyDirection * 400;
                let ty = dragY * 1.5;
                let rotate = flyDirection * 45;
                slide.style.transform = `perspective(1000px) translateX(${tx}px) translateY(${ty}px) translateZ(50px) rotate(${rotate}deg) scale(0.9)`;
                slide.style.opacity = '0';
                slide.style.zIndex = '12';
                return;
            }

            // Position in stack relative to activeIndex
            let indexInStack = (i - activeIndex + N) % N;
            
            // Drag ratios
            let dragRatio = 0;
            if (isDragging) {
                let dist = Math.hypot(dragX, dragY);
                dragRatio = Math.min(1, dist / 150);
            }

            if (indexInStack === 0) {
                // Front active card
                slide.classList.add('active-highlight');
                slide.style.opacity = '1';
                slide.style.zIndex = '10';
                
                // Track finger
                let rotate = dragX / 12;
                slide.style.transform = `perspective(1000px) translateX(${dragX}px) translateY(${dragY}px) translateZ(0px) rotate(${rotate}deg) scale(1)`;
            } else {
                slide.classList.remove('active-highlight');
                
                // Cards behind shift forward and scale up as user drags front card away
                let tx = (indexInStack * 15) - (dragRatio * 15);
                let ty = (indexInStack * 10) - (dragRatio * 10);
                let tz = -(indexInStack * 50) + (dragRatio * 50);
                let rotate = (indexInStack * 2) - (dragRatio * 2);
                let scale = (1 - indexInStack * 0.07) + (dragRatio * 0.07);
                let opacity = (0.95 - indexInStack * 0.15) + (dragRatio * 0.15);
                let zIndex = 10 - indexInStack;

                slide.style.zIndex = `${zIndex}`;
                slide.style.opacity = `${opacity}`;
                slide.style.transform = `perspective(1000px) translateX(${tx}px) translateY(${ty}px) translateZ(${tz}px) rotate(${rotate}deg) scale(${scale})`;
            }
        });

        // Sync dots
        dots.forEach((dot, i) => {
            if (i === activeIndex) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }

    function captureClick(e) {
        e.stopPropagation();
        e.preventDefault();
        viewport.removeEventListener('click', captureClick, true);
    }

    function getCoordinates(e) {
        let clientX = 0;
        let clientY = 0;
        if (e.clientX !== undefined) {
            clientX = e.clientX;
            clientY = e.clientY;
        } else if (e.touches && e.touches.length > 0) {
            clientX = e.touches[0].clientX;
            clientY = e.touches[0].clientY;
        }
        return { clientX, clientY };
    }

    function handleStart(e) {
        isDragging = true;
        const coords = getCoordinates(e);
        startX = coords.clientX;
        startY = coords.clientY;
        dragX = 0;
        dragY = 0;
        clickPrevented = false;
        updateLayout(false);
    }

    function handleMove(e) {
        if (!isDragging) return;
        const coords = getCoordinates(e);
        const diffX = coords.clientX - startX;
        const diffY = coords.clientY - startY;

        if (e.cancelable) {
            e.preventDefault();
        }

        dragX = diffX;
        dragY = diffY;

        // Limit vertical drag down slightly to keep card stack visible
        if (dragY > 80) dragY = 80;

        updateLayout(false);
    }

    function handleEnd() {
        if (!isDragging) return;
        isDragging = false;

        let totalDist = Math.hypot(dragX, dragY);
        
        if (totalDist > 90) {
            // Swipe off! Determine direction
            let flyDirection = dragX >= 0 ? 1 : -1;
            let swipedIndex = activeIndex;

            // Trigger animation frame for swipe-off
            updateLayout(true, swipedIndex, flyDirection);
            triggerHaptic('heavy', `Swiped away card ${activeIndex + 1}`);

            // Increment active index after animation finishes
            setTimeout(() => {
                activeIndex = (activeIndex + 1) % N;
                dragX = 0;
                dragY = 0;
                updateLayout(true);
            }, 300);
        } else {
            // Snap back
            dragX = 0;
            dragY = 0;
            updateLayout(true);
            triggerHaptic('light', 'Card snap back');
        }

        // Click prevention
        if (totalDist > 10) {
            viewport.addEventListener('click', captureClick, true);
        }
    }

    // Touch event listeners for mobile devices
    viewport.addEventListener('touchstart', (e) => {
        lastTouchTime = Date.now();
        handleStart(e);
    }, { passive: true });

    viewport.addEventListener('touchmove', (e) => {
        handleMove(e);
    }, { passive: false });

    viewport.addEventListener('touchend', () => {
        handleEnd();
    });

    viewport.addEventListener('touchcancel', () => {
        handleEnd();
    });

    // Mouse event listeners for desktop devices
    viewport.addEventListener('mousedown', (e) => {
        if (e.button !== 0) return;
        
        // Avoid double trigger on touch devices that emulate mouse events
        if (Date.now() - lastTouchTime < 800) return;

        handleStart(e);

        const mouseMoveHandler = (ev) => {
            handleMove(ev);
        };
        const mouseUpHandler = () => {
            handleEnd();
            document.removeEventListener('mousemove', mouseMoveHandler);
            document.removeEventListener('mouseup', mouseUpHandler);
        };
        document.addEventListener('mousemove', mouseMoveHandler);
        document.addEventListener('mouseup', mouseUpHandler);
    });

    // Initial load layout
    updateLayout(false);
}

// Interactive Flight Simulator logic
function initFlightSimulator() {
    const svg = document.getElementById('globeFlightSvg');
    if (!svg) return;

    // Show plane and activate starting node
    const plane = document.getElementById('interactivePlane');
    if (plane) plane.style.display = 'block';

    const nodes = document.querySelectorAll('.airport-node');
    nodes.forEach(node => {
        if (node.id === `node-${currentCity}`) {
            node.classList.add('active');
        } else {
            node.classList.remove('active');
        }
    });

    // Auto-start immediately
    isExploring = true;
    triggerNextExplorationFlight();
}

function startGlobeExploration(event) {
    if (event) {
        event.stopPropagation();
    }
    
    isExploring = !isExploring;
    
    const btn = document.getElementById('exploreX AirlineBtn');
    const plane = document.getElementById('interactivePlane');
    
    if (isExploring) {
        triggerHaptic('medium', 'Starting globe exploration');
        if (btn) {
            btn.classList.add('active');
            btn.innerText = 'Stop Exploration';
        }
        if (plane) {
            plane.style.display = 'block';
        }
        
        // Activate the starting node (currentCity)
        const nodes = document.querySelectorAll('.airport-node');
        nodes.forEach(node => {
            if (node.id === `node-${currentCity}`) {
                node.classList.add('active');
            } else {
                node.classList.remove('active');
            }
        });
        
        // Start the loop
        triggerNextExplorationFlight();
    } else {
        triggerHaptic('light', 'Stopping globe exploration');
        if (btn) {
            btn.classList.remove('active');
            btn.innerText = 'Explore with X Airline';
        }
        
        clearTimeout(flightTimeoutId);
        cancelAnimationFrame(flightAnimationId);
        
        if (plane) {
            plane.style.display = 'none';
        }
        
        // Reset path
        const flightPath = document.getElementById('interactiveFlightPath');
        const flightPathActive = document.getElementById('interactiveFlightPathActive');
        if (flightPath) flightPath.setAttribute('d', '');
        if (flightPathActive) flightPathActive.setAttribute('d', '');
        
        // Deactivate all nodes and pulses
        const nodes = document.querySelectorAll('.airport-node');
        nodes.forEach(node => node.classList.remove('active'));
        
        const pulses = document.querySelectorAll('.airport-pulse');
        pulses.forEach(pulse => pulse.classList.remove('animating'));
        
        // Reset HUD
        const hudTitle = document.getElementById('hudDestinationName');
        const hudStats = document.getElementById('hudDestinationStats');
        if (hudTitle) hudTitle.innerText = 'Explore with X Airline';
        if (hudStats) hudStats.innerText = 'Click the button above to begin journey';
        
        const pulseLight = document.querySelector('.hud-pulse-light');
        if (pulseLight) {
            pulseLight.classList.remove('flying');
            pulseLight.classList.remove('landed');
        }
    }
}

function triggerNextExplorationFlight() {
    if (!isExploring) return;
    
    clearTimeout(flightTimeoutId);
    
    // Find next city index
    const currentIndex = flightSequence.indexOf(currentCity);
    const nextIndex = (currentIndex + 1) % flightSequence.length;
    const nextCity = flightSequence[nextIndex];
    
    // Update active nodes visual state for the flight target
    const nodes = document.querySelectorAll('.airport-node');
    nodes.forEach(node => {
        if (node.id === `node-${nextCity}`) {
            node.classList.add('active');
        } else {
            node.classList.remove('active');
        }
    });
    
    animatePlaneFlight(currentCity, nextCity, () => {
        currentCity = nextCity;
        
        // Landed! Now pause for exactly 1.5 seconds, then hop to the next city
        if (isExploring) {
            flightTimeoutId = setTimeout(() => {
                triggerNextExplorationFlight();
            }, 1500); // 1.5 seconds landing pause
        }
    });
}

function animatePlaneFlight(fromCity, toCity, onComplete) {
    const fromCoord = cityCoordinates[fromCity];
    const toCoord = cityCoordinates[toCity];
    if (!fromCoord || !toCoord) return;

    const plane = document.getElementById('interactivePlane');
    const flightPath = document.getElementById('interactiveFlightPath');
    const flightPathActive = document.getElementById('interactiveFlightPathActive');
    const pulseLight = document.querySelector('.hud-pulse-light');
    
    if (plane) plane.style.display = 'block';
    if (pulseLight) {
        pulseLight.classList.add('flying');
        pulseLight.classList.remove('landed');
    }

    const p0 = fromCoord;
    const p2 = toCoord;
    
    // Shift control point upwards to make Bezier curve arc
    const midX = (p0.x + p2.x) / 2;
    const midY = (p0.y + p2.y) / 2;
    const dist = Math.hypot(p2.x - p0.x, p2.y - p0.y);
    const arcHeight = Math.max(30, dist * 0.25);
    const p1 = { x: midX, y: midY - arcHeight };

    const pathD = `M ${p0.x} ${p0.y} Q ${p1.x} ${p1.y} ${p2.x} ${p2.y}`;
    if (flightPath) flightPath.setAttribute('d', pathD);
    if (flightPathActive) {
        flightPathActive.setAttribute('d', pathD);
        const pathLength = flightPathActive.getTotalLength();
        flightPathActive.style.strokeDasharray = pathLength;
        flightPathActive.style.strokeDashoffset = pathLength;
    }

    const duration = Math.max(1200, dist * 8); // Duration based on distance
    const startTime = performance.now();

    updateFlightHud(fromCity, toCity, 'IN_FLIGHT');

    function step(timestamp) {
        const elapsed = timestamp - startTime;
        let t = elapsed / duration;
        if (t > 1) t = 1;

        // Quadratic Bezier coordinates calculation
        const x = (1 - t) * (1 - t) * p0.x + 2 * (1 - t) * t * p1.x + t * t * p2.x;
        const y = (1 - t) * (1 - t) * p0.y + 2 * (1 - t) * t * p1.y + t * t * p2.y;

        // Tangent slope calculation for rotation angle
        const tx = 2 * (1 - t) * (p1.x - p0.x) + 2 * t * (p2.x - p1.x);
        const ty = 2 * (1 - t) * (p1.y - p0.y) + 2 * t * (p2.y - p1.y);
        const angle = Math.atan2(ty, tx) * 180 / Math.PI;

        if (plane) {
            plane.setAttribute('transform', `translate(${x}, ${y}) rotate(${angle})`);
        }

        if (flightPathActive) {
            const len = flightPathActive.getTotalLength();
            flightPathActive.style.strokeDashoffset = len * (1 - t);
        }

        if (t < 1) {
            flightAnimationId = requestAnimationFrame(step);
        } else {
            // Landing!
            if (pulseLight) {
                pulseLight.classList.remove('flying');
                pulseLight.classList.add('landed');
            }
            triggerAirportPulse(toCity);
            updateFlightHud(fromCity, toCity, 'LANDED');
            triggerHaptic('success', `Landed at ${toCity}`);
            onComplete();
        }
    }

    cancelAnimationFrame(flightAnimationId);
    flightAnimationId = requestAnimationFrame(step);
}

function triggerAirportPulse(cityCode) {
    const pulseCircle = document.getElementById(`pulse-${cityCode}`);
    if (pulseCircle) {
        pulseCircle.classList.remove('animating');
        // Trigger reflow to restart animation
        void pulseCircle.offsetWidth;
        pulseCircle.classList.add('animating');
    }
}

function updateFlightHud(fromCity, toCity, status) {
    const dest = cityCoordinates[toCity];
    const callout = document.getElementById('globeDestCallout');
    const calloutName = document.getElementById('destCalloutName');
    const calloutCode = document.getElementById('destCalloutCode');

    if (!dest || !callout) return;

    if (status === 'IN_FLIGHT') {
        // Hide callout while flying
        callout.classList.remove('visible');
    } else {
        // LANDED — show city callout
        if (calloutName) calloutName.textContent = dest.name;
        if (calloutCode) calloutCode.textContent = toCity;
        callout.classList.add('visible');
        // Auto-hide after 2.5 seconds
        setTimeout(() => callout.classList.remove('visible'), 2500);
    }
}

// Parallax cloud offset on scroll
function setupParallaxScroll() {
    const appContent = document.getElementById('appContent');
    if (!appContent) return;
    
    appContent.addEventListener('scroll', () => {
        const scrollTop = appContent.scrollTop;
        const clouds = document.querySelectorAll('.cloud-layer');
        
        clouds.forEach((cloud, idx) => {
            const speedFactor = (idx + 1) * 0.08;
            const offset = scrollTop * speedFactor;
            cloud.style.transform = `translateY(${offset}px) scale(${idx === 0 ? 1.35 : idx === 1 ? 0.95 : 1.15})`;
        });
    });
}

// Haptic Volume & Atmosphere control triggers from Cockpit
function changeCloudSpeed(val) {
    const lbl = document.getElementById('lblCloudSpeed');
    if (lbl) lbl.innerText = `${val}s`;
    
    document.querySelectorAll('.cloud-layer').forEach(cloud => {
        if (cloud.classList.contains('cloud-slow')) {
            cloud.style.animationDuration = `${val * 1.75}s`;
        } else if (cloud.classList.contains('cloud-medium')) {
            cloud.style.animationDuration = `${val * 1.4}s`;
        } else if (cloud.classList.contains('cloud-fast')) {
            cloud.style.animationDuration = `${val * 0.9}s`;
        }
    });
    triggerHaptic('light', `Cloud drift speed set to ${val}s`);
}

function changeHapticVolume(val) {
    const lbl = document.getElementById('lblHapticVol');
    if (lbl) lbl.innerText = `${val}%`;
    
    const sndTap = document.getElementById('sndTap');
    const sndConfirm = document.getElementById('sndConfirm');
    const sndAlert = document.getElementById('sndAlert');
    
    const multiplier = val / 100;
    if (sndTap) sndTap.volume = multiplier * 0.5;
    if (sndConfirm) sndConfirm.volume = multiplier * 0.7;
    if (sndAlert) sndAlert.volume = multiplier * 0.8;
    
    triggerHaptic('light', `Haptic system volume: ${val}%`);
}

// Real-time canvas-based haptic oscilloscope visualizer
let canvas = null;
let ctx = null;
let wavePoints = [];

function initHapticWaveform() {
    canvas = document.getElementById('hapticWaveformCanvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');
    animateWaveform();
}

function triggerWaveformEffect(type) {
    if (!canvas || !ctx) return;
    
    let count = 0;
    let amplitude = 0;
    let speed = 0;
    
    if (type === 'light') {
        count = 12;
        amplitude = 8;
        speed = 0.12;
    } else if (type === 'medium') {
        count = 20;
        amplitude = 15;
        speed = 0.22;
    } else if (type === 'heavy') {
        count = 30;
        amplitude = 22;
        speed = 0.32;
    } else if (type === 'success') {
        count = 35;
        amplitude = 18;
        speed = 0.18;
    } else if (type === 'error') {
        count = 45;
        amplitude = 25;
        speed = 0.38;
    }
    
    for (let i = 0; i < count; i++) {
        wavePoints.push({
            x: 0,
            y: canvas.height / 2,
            targetY: (Math.random() - 0.5) * amplitude * 2,
            phase: Math.random() * Math.PI,
            speed: speed * (0.8 + Math.random() * 0.4),
            age: 0,
            maxAge: 70 + Math.random() * 30,
            amplitude: amplitude
        });
    }
}

function animateWaveform() {
    if (!canvas || !ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw Oscilloscope background grid lines (cyber-tech pilot dashboard style)
    ctx.strokeStyle = 'rgba(139, 92, 246, 0.08)';
    ctx.lineWidth = 0.5;
    
    // Vertical grid lines
    for (let x = 0; x < canvas.width; x += 20) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    
    // Horizontal grid lines
    for (let y = 0; y < canvas.height; y += 10) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
    
    // Center Line
    ctx.strokeStyle = 'rgba(139, 92, 246, 0.2)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, canvas.height / 2);
    ctx.lineTo(canvas.width, canvas.height / 2);
    ctx.stroke();
    
    // Update and draw wave points
    if (wavePoints.length > 0) {
        ctx.strokeStyle = '#8b5cf6';
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        
        wavePoints.forEach(p => {
            p.age++;
            p.x += p.speed * 4.5;
            
            const lifeRatio = 1 - (p.age / p.maxAge);
            const currentAmp = p.amplitude * lifeRatio * Math.sin(p.age * 0.18 + p.phase);
            p.y = (canvas.height / 2) + currentAmp;
        });
        
        // Remove dead points
        wavePoints = wavePoints.filter(p => p.age < p.maxAge && p.x < canvas.width);
        
        // Plot continuous path
        for (let i = 0; i < canvas.width; i += 2) {
            let ySum = 0;
            let activeContributions = 0;
            
            wavePoints.forEach(p => {
                const dist = Math.abs(p.x - i);
                if (dist < 30) {
                    const weight = (30 - dist) / 30;
                    ySum += p.y * weight;
                    activeContributions += weight;
                }
            });
            
            const yVal = activeContributions > 0 ? (ySum / activeContributions) : (canvas.height / 2);
            if (i === 0) {
                ctx.moveTo(i, yVal);
            } else {
                ctx.lineTo(i, yVal);
            }
        }
        ctx.stroke();
    }
    
    requestAnimationFrame(animateWaveform);
}

// ==========================================================================
// SIRI VOICE ASSISTANT WAVELENGTH GENERATOR
// ==========================================================================

let siriCanvas = null;
let siriCtx = null;
let siriAnimationId = null;
let siriActive = false;

function startVoiceSearch(event) {
    if (event) event.stopPropagation();
    
    triggerHaptic('heavy', 'Siri Voice Search Activated');
    
    const overlay = document.getElementById('siriVoiceOverlay');
    if (!overlay) return;
    
    overlay.classList.add('active');
    siriActive = true;
    
    siriCanvas = document.getElementById('siriVoiceCanvas');
    if (siriCanvas) {
        siriCtx = siriCanvas.getContext('2d');
        animateSiriWaves();
    }
    
    // Simulate voice recognition process for 3.5 seconds
    setTimeout(() => {
        // Automatically select destination: Dubai (DXB)
        const dubai = airports.find(ap => ap.code === 'DXB');
        if (dubai) {
            selectAirportFromVoice(dubai);
        }
        closeVoiceSearch();
    }, 3500);
}

function closeVoiceSearch() {
    const overlay = document.getElementById('siriVoiceOverlay');
    if (overlay) overlay.classList.remove('active');
    siriActive = false;
    if (siriAnimationId) cancelAnimationFrame(siriAnimationId);
}

function animateSiriWaves() {
    if (!siriActive || !siriCanvas || !siriCtx) return;
    siriCtx.clearRect(0, 0, siriCanvas.width, siriCanvas.height);
    
    const height = siriCanvas.height;
    const time = Date.now() * 0.008;
    
    // Draw 3 colorful assistant soundwaves
    drawSiriWave(time, height / 2, 22, '#06b6d4', 0.04, 0);       // Cyan
    drawSiriWave(time * 1.2, height / 2, 16, '#ec4899', 0.05, Math.PI / 3); // Magenta
    drawSiriWave(time * 0.8, height / 2, 12, '#eab308', 0.03, Math.PI / 1.5); // Gold
    
    siriAnimationId = requestAnimationFrame(animateSiriWaves);
}

function drawSiriWave(time, centerY, maxAmp, color, freq, phaseOffset) {
    if (!siriCanvas || !siriCtx) return;
    
    siriCtx.strokeStyle = color;
    siriCtx.lineWidth = 2.5;
    siriCtx.beginPath();
    
    for (let x = 0; x < siriCanvas.width; x++) {
        // Bell envelope to pinch the wave at endpoints
        const envelope = Math.sin((x / siriCanvas.width) * Math.PI);
        const y = centerY + Math.sin(x * freq + time + phaseOffset) * maxAmp * envelope;
        
        if (x === 0) {
            siriCtx.moveTo(x, y);
        } else {
            siriCtx.lineTo(x, y);
        }
    }
    
    siriCtx.stroke();
}

function selectAirportFromVoice(airport) {
    appState.selectedTo = airport;
    const toValNode = document.getElementById('valToCode');
    if (toValNode) toValNode.innerText = airport.city;
    
    triggerHaptic('success', `Voice recognized: Flying to ${airport.city}`);
    updateSearchButtonState();
}

// ==========================================================================
// DATE & TRAVELERS PICKER DRAWERS
// ==========================================================================


function openFlightSearchDrawer() {
    triggerHaptic('medium', 'Open search drawer');
    closeAllDrawers();
    
    const backdrop = document.getElementById('bottomSheetBackdrop');
    const drawer = document.getElementById('flightSearchDrawer');
    const searchWidget = document.getElementById('searchWidgetSection');
    const drawerContent = document.getElementById('flightSearchDrawerContent');
    
    if (backdrop && drawer && searchWidget && drawerContent) {
        drawerContent.appendChild(searchWidget);
        searchWidget.style.paddingBottom = "0px";
        backdrop.classList.add('visible');
        drawer.classList.add('visible');
    }
}

function closeAllDrawers() {
    const backdrop = document.getElementById('bottomSheetBackdrop');
    const drawers = document.querySelectorAll('.bottom-sheet-drawer');
    
    
    const originalContainer = document.getElementById('homeContentContainer');
    const searchWidget = document.getElementById('searchWidgetSection');
    const categoryTabs = document.getElementById('categoryTabsSection');
    if (originalContainer && searchWidget && searchWidget.parentElement && searchWidget.parentElement.id === 'flightSearchDrawerContent') {
        if (categoryTabs && categoryTabs.nextSibling) {
            originalContainer.insertBefore(searchWidget, categoryTabs.nextSibling);
        } else {
            originalContainer.appendChild(searchWidget);
        }
        searchWidget.style.paddingBottom = "24px";
    }

    if (backdrop) backdrop.classList.remove('visible');
    if (drawers.length > 0) {
        drawers.forEach(dr => dr.classList.remove('visible'));
    }
    const feed = document.getElementById('addonsMainFeed');
    if (feed) feed.style.overflowY = 'auto';
    
    // Explicitly target passenger form just in case
    const paxForm = document.getElementById('paxDetailsDrawerModal');
    if (paxForm) paxForm.classList.remove('visible');
}

function openDatePicker() {
    triggerHaptic('medium', 'Open date picker');
    
    const drawers = document.querySelectorAll('.bottom-sheet-drawer');
    drawers.forEach(dr => dr.classList.remove('visible'));
    
    const backdrop = document.getElementById('bottomSheetBackdrop');
    const drawer = document.getElementById('dateSheetDrawer');
    
    if (backdrop && drawer) {
        pickerState.calendarMonth = pickerState.selectedDate.getMonth();
        pickerState.calendarYear = pickerState.selectedDate.getFullYear();
        
        renderCalendar();
        
        backdrop.classList.add('visible');
        drawer.classList.add('visible');
    }
}

function updateDateDisplay() {
    const d = pickerState.selectedDate;
    if (!d) return;
    
    const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const formatted = `${weekdays[d.getDay()]}, ${d.getDate()} ${months[d.getMonth()]}`;
    
    const valNode = document.getElementById('valDateText');
    if (valNode) valNode.innerText = formatted;
}

function renderCalendar() {
    const grid = document.getElementById('calendarGrid');
    const monthTitle = document.getElementById('calendarMonthTitle');
    if (!grid || !monthTitle) return;
    
    grid.innerHTML = '';
    
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    monthTitle.innerText = `${monthNames[pickerState.calendarMonth]} ${pickerState.calendarYear}`;
    
    const firstDayIndex = new Date(pickerState.calendarYear, pickerState.calendarMonth, 1).getDay();
    const totalDays = new Date(pickerState.calendarYear, pickerState.calendarMonth + 1, 0).getDate();
    
    const today = new Date();
    today.setHours(0,0,0,0);
    
    for (let i = 0; i < firstDayIndex; i++) {
        const cell = document.createElement('div');
        cell.className = 'calendar-day empty';
        grid.appendChild(cell);
    }
    
    for (let day = 1; day <= totalDays; day++) {
        const cell = document.createElement('div');
        cell.className = 'calendar-day';
        cell.innerText = day;
        
        const cellDate = new Date(pickerState.calendarYear, pickerState.calendarMonth, day);
        cellDate.setHours(0,0,0,0);
        
        if (cellDate < today) {
            cell.classList.add('disabled');
        } else {
            const activeDate = pickerState.selectedDate;
            if (activeDate && 
                activeDate.getDate() === day && 
                activeDate.getMonth() === pickerState.calendarMonth && 
                activeDate.getFullYear() === pickerState.calendarYear) {
                cell.classList.add('selected');
            }
            
            const currDate = new Date();
            if (currDate.getDate() === day && 
                currDate.getMonth() === pickerState.calendarMonth && 
                currDate.getFullYear() === pickerState.calendarYear) {
                cell.classList.add('today');
            }
            
            cell.onclick = () => {
                pickerState.selectedDate = new Date(pickerState.calendarYear, pickerState.calendarMonth, day);
                triggerHaptic('success', `Departure set: ${day} ${monthNames[pickerState.calendarMonth]}`);
                updateDateDisplay();
                updateSearchButtonState();
                
                const backdrop = document.getElementById('bottomSheetBackdrop');
                const drawer = document.getElementById('dateSheetDrawer');
                backdrop.classList.remove('visible');
                drawer.classList.remove('visible');
            };
        }
        
        grid.appendChild(cell);
    }
}

function changeMonth(dir) {
    triggerHaptic('light', 'Change calendar month');
    pickerState.calendarMonth += dir;
    if (pickerState.calendarMonth < 0) {
        pickerState.calendarMonth = 11;
        pickerState.calendarYear--;
    } else if (pickerState.calendarMonth > 11) {
        pickerState.calendarMonth = 0;
        pickerState.calendarYear++;
    }
    renderCalendar();
}

function openTravelersPicker() {
    triggerHaptic('medium', 'Open travelers selection');
    
    const drawers = document.querySelectorAll('.bottom-sheet-drawer');
    drawers.forEach(dr => dr.classList.remove('visible'));
    
    const backdrop = document.getElementById('bottomSheetBackdrop');
    const drawer = document.getElementById('travelersSheetDrawer');
    
    if (backdrop && drawer) {
        document.getElementById('countAdults').innerText = pickerState.travelers.adults;
        document.getElementById('countChildren').innerText = pickerState.travelers.children;
        document.getElementById('countInfants').innerText = pickerState.travelers.infants;
        
        backdrop.classList.add('visible');
        drawer.classList.add('visible');
    }
}

function adjustTravelers(type, dir) {
    const adultsNode = document.getElementById('countAdults');
    const childrenNode = document.getElementById('countChildren');
    const infantsNode = document.getElementById('countInfants');
    if (!adultsNode || !childrenNode || !infantsNode) return;
    
    const adultsVal = parseInt(adultsNode.innerText);
    const childrenVal = parseInt(childrenNode.innerText);
    const infantsVal = parseInt(infantsNode.innerText);
    
    let targetVal = 0;
    if (type === 'adults') targetVal = adultsVal + dir;
    if (type === 'children') targetVal = childrenVal + dir;
    if (type === 'infants') targetVal = infantsVal + dir;
    
    if (targetVal < 0) return;
    if (type === 'adults' && targetVal < 1) return;
    
    const totalTravelers = (type === 'adults' ? targetVal : adultsVal) + 
                          (type === 'children' ? targetVal : childrenVal) + 
                          (type === 'infants' ? targetVal : infantsVal);
    if (totalTravelers > 9) {
        triggerHaptic('error', 'Maximum 9 travelers allowed');
        return;
    }
    
    if (type === 'infants' && targetVal > adultsVal) {
        triggerHaptic('error', 'Infants cannot exceed number of Adults');
        return;
    }
    if (type === 'adults' && targetVal < infantsVal) {
        triggerHaptic('error', 'Adults must be equal or greater than Infants');
        return;
    }
    
    triggerHaptic('light', `${type} modified`);
    if (type === 'adults') adultsNode.innerText = targetVal;
    if (type === 'children') childrenNode.innerText = targetVal;
    if (type === 'infants') infantsNode.innerText = targetVal;
}

function confirmTravelers() {
    const adultsNode = document.getElementById('countAdults');
    const childrenNode = document.getElementById('countChildren');
    const infantsNode = document.getElementById('countInfants');
    if (!adultsNode || !childrenNode || !infantsNode) return;
    
    const adults = parseInt(adultsNode.innerText);
    const children = parseInt(childrenNode.innerText);
    const infants = parseInt(infantsNode.innerText);
    
    pickerState.travelers.adults = adults;
    pickerState.travelers.children = children;
    pickerState.travelers.infants = infants;
    
    triggerHaptic('success', `Travelers group set: ${adults} Adults`);
    
    const totalCount = adults + children + infants;
    let labelText = `${totalCount} Traveler${totalCount > 1 ? 's' : ''}`;
    
    const labelNode = document.getElementById('valTravelersText');
    if (labelNode) labelNode.innerText = labelText;
    
    const backdrop = document.getElementById('bottomSheetBackdrop');
    const drawer = document.getElementById('travelersSheetDrawer');
    if (backdrop && drawer) {
        backdrop.classList.remove('visible');
        drawer.classList.remove('visible');
    }
}

// Plane Takeoff Screen Transition handler
function triggerPlaneTransition(event) {
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }
    
    // Play aircraft takeoff haptic sounds
    triggerHaptic('heavy', 'Aircraft Takeoff transition triggered');
    
    const overlay = document.getElementById('planeTransitionOverlay');
    const aircraft = document.getElementById('transitionAircraft');
    if (!overlay || !aircraft) return;
    
    // Launch overlay and start flight animation
    overlay.classList.add('active');
    aircraft.classList.add('takeoff');
    
    // Mid-flight reveal: navigate to deals page in the background
    setTimeout(() => {
        navigateTo('deals');
    }, 600);
    
    // Clear overlay and classes when flight finishes
    setTimeout(() => {
        overlay.classList.remove('active');
        aircraft.classList.remove('takeoff');
    }, 1450);
}

// ==========================================================================
// LOYALTY SECTION - INTERACTIVE LOYALTY CARD ANIMATIONS
// ==========================================================================

function triggerLoyaltyPlaneAnimation() {
    const text = document.getElementById('loyaltyBalanceText');
    const flyer = document.getElementById('loyaltyPlaneFlyer');
    if (!text || !flyer) return;

    // Reset animations
    text.classList.remove('animate');
    flyer.classList.remove('animate');
    
    // Force reflow
    void text.offsetWidth;
    void flyer.offsetWidth;

    // Re-apply animations
    text.classList.add('animate');
    flyer.classList.add('animate');
}

function initPartnerWallet() {
    const cards = Array.from(document.querySelectorAll('.partner-card'));
    if (cards.length === 0) return;

    let currentIndex = 0;
    const N = cards.length;

    function updateCardPositions() {
        cards.forEach((card, i) => {
            // Calculate relative index from currentIndex
            let relIndex = (i - currentIndex + N) % N;

            if (relIndex === 0) {
                // Front card (active)
                card.style.transform = 'translateY(12px) scale(1.0)';
                card.style.opacity = '1';
                card.style.zIndex = '4';
            } else if (relIndex === 1) {
                // Middle card
                card.style.transform = 'translateY(0px) scale(0.92)';
                card.style.opacity = '0.85';
                card.style.zIndex = '3';
            } else if (relIndex === 2) {
                // Back card
                card.style.transform = 'translateY(-12px) scale(0.84)';
                card.style.opacity = '0.6';
                card.style.zIndex = '2';
            } else {
                // Hidden queue cards
                card.style.transform = 'translateY(-24px) scale(0.76)';
                card.style.opacity = '0';
                card.style.zIndex = '1';
            }
        });
    }

    // Initialize positions
    updateCardPositions();

    // Cycle cards interval
    setInterval(() => {
        // Front card animate sliding down (swipe-off effect)
        const frontCard = cards[currentIndex];
        frontCard.style.transform = 'translateY(55px) scale(0.9)';
        frontCard.style.opacity = '0';
        frontCard.style.zIndex = '5'; // Keep on top of others while exiting
        
        // Trigger light haptic on cycle
        triggerHaptic('light', 'Loyalty card brand rotated');

        setTimeout(() => {
            // Move index to next card
            currentIndex = (currentIndex + 1) % N;
            updateCardPositions();
        }, 300); // Wait for sliding down animation half-way
    }, 2800);
}

// ==========================================================================
// TRAVEL ON TAP - INTERACTIVE MAP BEACONS & FARES
// ==========================================================================

const travelOnTapData = {
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
};

let currentTapDestination = 'HJR';
let selectedTapFareIndex = 4;

function initTravelOnTap() {
    expandBoardingPass('HJR', false);
}

function expandBoardingPass(code, userClicked = true) {
    if (userClicked) {
        if (currentTapDestination === code) return;
        triggerHaptic('medium', `Boarding pass selected: ${code}`);
    }
    
    currentTapDestination = code;
    selectedTapFareIndex = 4; // default to middle item
    
    // Toggle active classes on boarding passes
    document.querySelectorAll('.boarding-pass-card').forEach(card => {
        card.classList.remove('expanded');
    });
    
    const targetCard = document.getElementById(`passCard${code}`);
    if (targetCard) {
        targetCard.classList.add('expanded');
        // keep focus seamlessly
        setTimeout(() => {
            targetCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
    }
    
    // Render the fare calendar inside this pass
    renderBoardingPassCalendar(code);
}

function renderBoardingPassCalendar(code) {
    const container = document.getElementById(`passCalendar${code}`);
    if (!container) return;
    
    container.innerHTML = '';
    const dest = travelOnTapData[code];
    if (!dest) return;
    
    dest.fares.forEach((fare, i) => {
        const chip = document.createElement('div');
        chip.className = 'pass-chip';
        if (fare.lowest) chip.classList.add('lowest-fare');
        if (i === selectedTapFareIndex) chip.classList.add('selected-fare');
        
        const originalPrice = fare.price;
        const discountedPrice = Math.floor(originalPrice * 0.9);
        const originalDisplay = `₹${originalPrice.toLocaleString('en-IN')}`;
        const discountedDisplay = `₹${discountedPrice.toLocaleString('en-IN')}`;
        
        chip.innerHTML = `
            <span class="pass-chip-date">${fare.date}</span>
            <span class="pass-chip-price" style="display: flex; flex-direction: column; align-items: center; gap: 2px;">
                <span style="text-decoration: line-through; opacity: 0.9; font-size: 8px; font-weight: 500;">${originalDisplay}</span>
                <span>${discountedDisplay}</span>
            </span>
        `;
        
        // Handle click manually to avoid triggering after drag
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

    // On initial render, scroll the 5th item into the center horizontally
    setTimeout(() => {
        if (container.children.length > 4) {
            const chip = container.children[4];
            const scrollLeftTarget = chip.offsetLeft - container.offsetWidth / 2 + chip.offsetWidth / 2;
            container.scrollTo({ left: scrollLeftTarget, behavior: 'auto' });
        }
    }, 50);
}

function selectBoardingPassDate(code, index) {
    selectedTapFareIndex = index;
    const dest = travelOnTapData[code];
    if (!dest) return;
    const fare = dest.fares[index];
    
    triggerHaptic('success', `Ticket preselected: Delhi to ${dest.name} on ${fare.date}`);
    
    // Re-render chips to update visual selected state
    renderBoardingPassCalendar(code);
    
    // Auto-fill Search Widget parameters:
    // 1. Origin (Delhi - DEL)
    const originAp = airports.find(ap => ap.code === 'DEL');
    if (originAp) {
        appState.selectedFrom = originAp;
        document.getElementById('valFromCode').innerText = originAp.city;
        
        // Trigger DEL layout shifts (Trending destinations slides up)
        const homeContent = document.getElementById('homeContentContainer');
        if (homeContent) {
            homeContent.classList.add('route-selected');
            document.getElementById('userGreeting').innerText = 'Delhi';
        }
    }

    // 2. Destination
    const destAp = airports.find(ap => ap.code === code);
    if (destAp) {
        appState.selectedTo = destAp;
        document.getElementById('valToCode').innerText = destAp.city;
    }

    // 3. Departure Date
    const dateNum = parseInt(fare.date);
    const selectDateObj = new Date(2026, 5, dateNum); // June 2026
    
    pickerState.selectedDate = selectDateObj;
    pickerState.calendarMonth = 5;
    pickerState.calendarYear = 2026;
    updateDateDisplay();

    // 4. Update Search Button State
    updateSearchButtonState();


}

// ==========================================================================
// FLIGHT RESULTS SCREEN LOGIC
// ==========================================================================

function renderFlightResults() {
    const list = document.getElementById('flightResultsList');
    if (!list) return;
    
    
    // Update header dynamically based on selection
    if (appState.selectedFrom && appState.selectedTo) {
        const routeMain = document.getElementById('resultsRouteMain');
        const routeSub = document.getElementById('resultsRouteSub');
        if (routeMain) {
            routeMain.innerHTML = `${appState.selectedFrom.city} <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" style="margin: 0 6px;"><path d="M6.99 11L3 15l3.99 4v-3H14v-2H6.99v-3zM21 9l-3.99-4v3H10v2h7.01v3L21 9z"/></svg> ${appState.selectedTo.city}`;
        }
        if (routeSub) {
            const dateStr = document.getElementById('valDateText').innerText;
            const paxStr = document.getElementById('valTravelersText').innerText;
            routeSub.innerText = `Return • ${dateStr} • ${paxStr}`;
        }
    }

    list.innerHTML = '';
    
    // Mock Data for Flights
    const flights = [
        { id: '6E 1234', from: '05:15', to: '07:30', dur: '2h 15m', stops: 'Non-stop', price: '4,800', stretch: '28,000' },
        { id: '6E 5678', from: '06:30', to: '10:45', dur: '4h 15m', stops: '1 Stop', price: '5,500', stretch: '32,000' },
        { id: '6E 9012', from: '08:00', to: '12:15', dur: '4h 15m', stops: '1 Stop', price: '6,200', stretch: '35,000' },
        { id: '6E 3456', from: '09:45', to: '12:00', dur: '2h 15m', stops: 'Non-stop', price: '6,500', stretch: '36,000' },
        { id: '6E 7890', from: '11:30', to: '14:00', dur: '2h 30m', stops: 'Non-stop', price: '7,100', stretch: '38,000' },
        { id: '6E 1122', from: '13:00', to: '17:45', dur: '4h 45m', stops: '1 Stop', price: '5,900', stretch: '30,500' },
        { id: '6E 3344', from: '15:45', to: '18:15', dur: '2h 30m', stops: 'Non-stop', price: '6,800', stretch: '36,500' },
        { id: '6E 5566', from: '18:20', to: '20:45', dur: '2h 25m', stops: 'Non-stop', price: '6,400', stretch: '34,000' },
        { id: '6E 7788', from: '20:15', to: '22:45', dur: '2h 30m', stops: 'Non-stop', price: '5,900', stretch: '33,000' },
        { id: '6E 9900', from: '22:30', to: '00:50', dur: '2h 20m', stops: 'Non-stop', price: '5,100', stretch: '31,000' }
    ];

    const fromAp = appState.selectedFrom ? appState.selectedFrom.code : 'DEL';
    const toAp = appState.selectedTo ? appState.selectedTo.code : 'BOM';

    // 1. Generate base HTML cards
    const cardsHtml = flights.map((f, i) => {
        let ecoPriceHtml = `₹ ${f.price}`;
        let ecoColClass = "fc-price-col";
        let ecoTagHtml = "";
        
        if (isStudentMode) {
            ecoColClass = "fc-price-col student-fare-search-active";
            const originalPriceNum = parseInt(f.price.replace(',', ''));
            const discountedPriceNum = Math.floor(originalPriceNum * 0.9);
            const discountedStr = discountedPriceNum.toLocaleString('en-IN');
            
            ecoPriceHtml = `<span class="price-strikethrough">₹${f.price}</span> ₹${discountedStr}`;
            ecoTagHtml = '<span onclick="openStudentBenefitsDrawer(event)" style="font-size: 9px; background: rgba(14, 165, 233, 0.08); color: var(--xairline-blue); padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(14, 165, 233, 0.2); cursor: pointer; display: inline-flex; align-items: center; gap: 4px;">Extra benefits <svg viewBox="0 0 24 24" width="10" height="10" fill="currentColor"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 16v-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M12 8h.01" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg></span>';
        }

        let edgeBadgeHtml = "";
        let cardClass = "flight-card";

        let durationHtml = `
            <div class="fc-duration">
                <span class="fc-dur-text">${f.dur}</span>
                <div class="fc-dur-line"></div>
                <span class="fc-dur-stop" style="color: ${f.stops === 'Non-stop' ? '#10b981' : 'var(--xairline-blue)'}">${f.stops}</span>
            </div>
        `;

        if (i === 2) {
            durationHtml = `
                <div class="fc-duration">
                    <span class="fc-dur-text">4h 55m</span>
                    <div class="fc-dur-line"></div>
                    <span class="fc-dur-stop" style="color: #f59e0b; font-weight: 800; text-decoration: underline; cursor: pointer; display: block; margin-top: 4px;" onclick="event.stopPropagation(); openLayoverPopup('Same Terminal', 'Layover for 40 mins', 'Baggage checked in through', 'No change of flight', '4h 55m')">1 Stop</span>
                </div>
            `;
        } else if (i === 3) {
            durationHtml = `
                <div class="fc-duration">
                    <span class="fc-dur-text">14h 20m</span>
                    <div class="fc-dur-line"></div>
                    <span class="fc-dur-stop" style="color: #ef4444; font-weight: 800; text-decoration: underline; cursor: pointer; display: block; margin-top: 4px;" onclick="event.stopPropagation(); openLayoverPopup('Terminal change at Delhi T3', 'about 20 mins via Free shuttle', 'Baggage is not checked through', 'Change of flight', '14h 20m')">+1 Day</span>
                </div>
            `;
        }

        return `
        <div class="${cardClass}" id="flightCard-${i}">
            ${edgeBadgeHtml}
            <div class="fc-header">
                <span>${f.id}</span>
                <span style="color: var(--xairline-blue); background: rgba(0, 95, 169, 0.05); padding: 2px 6px; border-radius: 4px;">Earn up to 400 Loyalty Points</span>
            </div>
            
            <div class="fc-times-row">
                <div class="fc-time-block">
                    <div class="fc-time">${f.from}</div>
                    <div class="fc-code">${fromAp}, T1</div>
                </div>
                
                ${durationHtml}
                
                <div class="fc-time-block">
                    <div class="fc-time">${f.to}</div>
                    <div class="fc-code">${toAp}, T2</div>
                </div>
            </div>
            
            <div class="fc-pricing-row">
                <div class="${ecoColClass}" onclick="openFarePopup(event, 'Economy', '${f.price}', '${f.id}', '${f.from}', '${f.to}', 'DEL, T1', 'BOM, T2', '${f.dur}')">
                    <div class="fc-class-name eco">Economy</div>
                    <div class="fc-price-val">${ecoPriceHtml} <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></div>
                    ${ecoTagHtml}
                </div>
                <div class="fc-price-col">
                    <div class="fc-class-name">Stretch / Business</div>
                    <div class="fc-price-val" style="color: #666; font-size: 14px;">₹ ${f.stretch} <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></div>
                </div>
            </div>
            
        </div>
        `;
    }).join('');

    list.innerHTML = cardsHtml;
    list.classList.add('searching-mode');

    // 2. Standard Staggered List Entrance
    const cards = list.querySelectorAll('.flight-card');
    
    cards.forEach((card, i) => {
        card.classList.add('shimmering');
        
        // Initial state: hidden and slightly pushed down
        card.style.transform = 'translateY(30px)';
        card.style.opacity = '0';
        card.style.transition = 'all 0.4s ease-out';
        
        // Staggered slide in
        setTimeout(() => {
            card.style.transform = 'translateY(0)';
            card.style.opacity = '1';
            if (i < 5) triggerHaptic('light', `Card entry ${i}`);
        }, 50 + (i * 100)); // 100ms delay between each card
    });

    // Live Search Simulation: Shuffle cards and update prices
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
        });

        triggerHaptic('success', 'Search complete');
        
        if (typeof isStudentMode !== 'undefined' && isStudentMode) {
            showToast('Student discount applied for all flights');
        }

        // 4. Inject Recommended Card
        setTimeout(() => {
            injectRecommendedCard(fromAp, toAp);
        }, 400); // Wait for the spread animation to settle

    }, 3000); // 3 seconds of background searching
}

function injectRecommendedCard(fromAp, toAp) {
    const list = document.getElementById('flightResultsList');
    if (!list) return;
    
    let oldP = "5,800";
    let ecoPriceHtml = `₹ ${oldP}`;
    let ecoColClass = "fc-price-col";
    let ecoTagHtml = "";
    
    if (isStudentMode) {
        ecoColClass = "fc-price-col student-fare-search-active";
        const originalPriceNum = parseInt(oldP.replace(',', ''));
        const discountedPriceNum = Math.floor(originalPriceNum * 0.9);
        const discountedStr = discountedPriceNum.toLocaleString('en-IN');
        
        ecoPriceHtml = `<span class="price-strikethrough">₹${oldP}</span> ₹${discountedStr}`;
        ecoTagHtml = '<span onclick="openStudentBenefitsDrawer(event)" style="font-size: 9px; background: rgba(14, 165, 233, 0.08); color: var(--xairline-blue); padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(14, 165, 233, 0.2); cursor: pointer; display: inline-flex; align-items: center; gap: 4px;">Extra benefits <svg viewBox="0 0 24 24" width="10" height="10" fill="currentColor"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 16v-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M12 8h.01" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg></span>';
    }

    const recCard = document.createElement('div');
    recCard.className = 'flight-card recommended';
    recCard.innerHTML = `
        <div class="recommended-badge">⭐ Recommended Morning Flight</div>
        <div class="fc-header" style="margin-top: 8px;">
            <span>6E 8888</span>
            <span style="color: var(--xairline-blue); background: rgba(0, 95, 169, 0.05); padding: 2px 6px; border-radius: 4px;">Earn up to 400 Loyalty Points</span>
        </div>
        
        <div class="fc-times-row">
            <div class="fc-time-block">
                <div class="fc-time">09:00</div>
                <div class="fc-code">${fromAp}, T1</div>
            </div>
            
            <div class="fc-duration">
                <span class="fc-dur-text">2h 10m</span>
                <div class="fc-dur-line"></div>
                <span class="fc-dur-stop" style="color: #10b981;">Non-stop</span>
            </div>
            
            <div class="fc-time-block">
                <div class="fc-time">11:10</div>
                <div class="fc-code">${toAp}, T2</div>
            </div>
        </div>
        
        <div class="fc-pricing-row">
            <div class="${ecoColClass}" onclick="openFarePopup(event, 'Economy', '${oldP}', '6E 8888', '09:00', '11:10', 'DEL, T1', 'BOM, T2', '2h 10m')">
                <div class="fc-class-name eco">Economy</div>
                <div class="fc-price-val">${ecoPriceHtml} <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></div>
                ${ecoTagHtml}
            </div>
            <div class="fc-price-col" onclick="openFarePopup(event, 'Stretch', '34,000', '6E 8888', '09:00', '11:10', 'DEL, T1', 'BOM, T2', '2h 10m')">
                <div class="fc-class-name">Stretch / Business</div>
                <div class="fc-price-val" style="color: #666; font-size: 14px;">₹ 34,000 <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></div>
            </div>
            
        </div>
    `;

    // Insert at the second position
    if (list.children.length > 1) {
        list.insertBefore(recCard, list.children[1]);
    } else {
        list.appendChild(recCard);
    }
}

// ==========================================================================
// HOMEPAGE TRIP COMPANION LOGIC
// ==========================================================================

function toggleSearchWidget() {
    triggerHaptic('light', 'Toggle Search Widget');
    const expanded = document.getElementById('searchWidgetExpandedContent');
    const toggleBtn = document.getElementById('searchAccordionToggle');
    
    if (expanded.classList.contains('collapsed')) {
        expanded.classList.remove('collapsed');
        toggleBtn.classList.remove('collapsed');
    } else {
        expanded.classList.add('collapsed');
        toggleBtn.classList.add('collapsed');
    }
}

function triggerHomepageCompanion() {
    triggerHaptic('medium', 'Trip Companion Triggered');
    
    // Switch to home if not already there
    if (appState.currentScreen !== 'home') {
        navigateTo('home');
    }
    
    const placeholder = document.getElementById('tripCompanionPlaceholder');
    const inlinePlane = document.getElementById('inlinePlaneIcon');
    const wrapper = document.getElementById('homeFlightStateWrapper');
    const expanded = document.getElementById('searchWidgetExpandedContent');
    const toggleBtn = document.getElementById('searchAccordionToggle');
    const devBtn = document.getElementById('devNavTrips');

    // Make Dev Button active visually
    document.querySelectorAll('.dev-simulator-console .dev-btn-stack button').forEach(btn => {
        if (!btn.id.startsWith('btnState')) {
            btn.classList.remove('active');
        }
    });
    if (devBtn) devBtn.classList.add('active');
    
    // Hide the search widget entirely when trip companion is loaded
    const searchWidget = document.getElementById('searchWidgetSection');
    if (searchWidget) searchWidget.style.display = 'none';
    
    // Expand the placeholder gap for the plane to fly in
    placeholder.style.height = '100px';
    placeholder.style.marginBottom = '16px';
    
    triggerHaptic('light', 'Plane Incoming');
    
    // Animate the inline plane from left to right inside the gap
    setTimeout(() => {
        inlinePlane.style.left = '120%';
        triggerHaptic('heavy', 'Plane Flyover');
    }, 50); // slight delay to allow layout to calculate
    
    // After plane finishes flying, swap placeholder for actual card
    setTimeout(() => {
        placeholder.style.height = '0';
        placeholder.style.marginBottom = '0';
        
        wrapper.style.display = 'flex';
        
        // Reset the plane position for next time without transition
        inlinePlane.style.transition = 'none';
        inlinePlane.style.left = '-50px';
        setTimeout(() => {
            inlinePlane.style.transition = 'left 1s cubic-bezier(0.4, 0, 0.2, 1)';
        }, 50);
        
        // Initialize flight companion specific state logic if needed
        renderCompanionState();
        
    }, 1100);
}

function fanOutDeck(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const cards = container.querySelectorAll('.stacked-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.remove('stacked-card');
            if (index % 2 === 0) triggerHaptic('light', 'Deck Fan Out');
        }, index * 90); 
    });
}


// ==========================================================================
// VIDEO SCROLL OBSERVER
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
    const videos = document.querySelectorAll('.insta-card-video');
    
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const video = entry.target;
                if (entry.isIntersecting) {
                    video.play().catch(e => console.log('Autoplay prevented', e));
                } else {
                    video.pause();
                }
            });
        }, { threshold: 0.5 }); // Play when at least 50% visible
        
        videos.forEach(video => {
            observer.observe(video);
        });
    }
});


// ==========================================================================
// LOYALTY STATE TOGGLE FLOW
// ==========================================================================
function toggleLoyaltyState() {
    const loyalCard = document.getElementById('loyalUserCard');
    const newCard = document.getElementById('newUserCard');
    
    if (loyalCard && newCard) {
        if (loyalCard.style.display !== 'none') {
            // Switch to New User Flow
            loyalCard.style.display = 'none';
            newCard.style.display = 'block';
        } else {
            // Switch to Loyal User Flow
            loyalCard.style.display = 'block';
            newCard.style.display = 'none';
        }
    }
}

function showToast(message) {
    let toast = document.getElementById('globalToast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'globalToast';
        const screen = document.querySelector('.iphone-screen');
        if (screen) {
            screen.appendChild(toast);
        } else {
            document.body.appendChild(toast);
        }
    }
    
    toast.innerText = message;
    toast.className = 'custom-toast show';
    
    setTimeout(() => {
        toast.className = 'custom-toast';
    }, 3000);
}

// ==========================================================================
// INTENT SEARCH LOGIC
// ==========================================================================

function toggleManualSearch() {
    const form = document.getElementById('manualSearchForm');
    const input = document.querySelector('.intent-text-input');
    if (form.style.display === 'none') {
        form.style.display = 'block';
        input.placeholder = "Or search manually...";
        triggerHaptic('light', 'Manual search opened');
        
        // Ensure default values are populated if empty
        if (!appState.selectedFrom) {
            appState.selectedFrom = airports.find(ap => ap.code === 'DEL');
            document.getElementById('valFromCode').innerText = appState.selectedFrom.city;
        }
    } else {
        form.style.display = 'none';
        input.placeholder = "Where to next?";
    }
}

function simulateIntent(intentText, destinationCode) {
    const input = document.getElementById('nlpSearchInput');
    if (input) input.value = intentText;
    triggerHaptic('success', 'Intent selected');
    
    // Simulate AI parsing intent
    setTimeout(() => {
        // Auto-fill some fields based on intent
        appState.selectedFrom = airports.find(ap => ap.code === 'DEL');
        appState.selectedTo = airports.find(ap => ap.code === destinationCode);
        
        if(appState.selectedTo) {
            document.getElementById('valFromCode').innerText = appState.selectedFrom.city;
            document.getElementById('valToCode').innerText = appState.selectedTo.city;
            
            // Open manual form to show the results of AI parsing
            if (window.exitNlpMode) {
                window.exitNlpMode();
            }
            
            // Auto search after a short delay
            setTimeout(() => {
                if (window.searchFlights) searchFlights();
            }, 800);
        }
    }, 600);
}

function toggleSearchMode(mode) {
    const tabManual = document.getElementById('tabManual');
    const tabNLP = document.getElementById('tabNLP');
    const viewManual = document.getElementById('manualSearchView');
    const viewNLP = document.getElementById('nlpSearchView');
    
    if (mode === 'manual') {
        tabManual.classList.add('active');
        tabNLP.classList.remove('active');
        viewManual.style.display = 'block';
        viewNLP.style.display = 'none';
        triggerHaptic('light', 'Manual Mode');
    } else {
        tabNLP.classList.add('active');
        tabManual.classList.remove('active');
        viewNLP.style.display = 'block';
        viewManual.style.display = 'none';
        triggerHaptic('light', 'NLP Mode');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('nlpSearchInput');
    const promptsSection = document.getElementById('trendingPromptsSection');
    
    if (searchInput) {
        searchInput.addEventListener('click', (e) => {
            e.stopPropagation();
            if (promptsSection) promptsSection.style.display = 'block';
        });
    }

    document.addEventListener('click', (e) => {
        if (promptsSection && !promptsSection.contains(e.target) && e.target !== searchInput) {
            promptsSection.style.display = 'none';
        }
    });
});


// Custom placeholder animation for NLP input
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('nlpSearchInput');
    const animatedText = document.getElementById('nlpAnimatedText');
    const customPlaceholder = document.getElementById('customNlpPlaceholder');
    
    if (input && animatedText && customPlaceholder) {
        const phrases = [
            "'Flights to Goa'",
            "'Trip to Delhi'",
            "'Beach destinations'",
            "'Coorg Homestays'"
        ];
        let currentIndex = 0;
        
        setInterval(() => {
            animatedText.style.opacity = 0;
            
            setTimeout(() => {
                currentIndex = (currentIndex + 1) % phrases.length;
                animatedText.innerText = phrases[currentIndex];
                animatedText.style.opacity = 1;
            }, 300);
        }, 3000); // Change every 3 seconds
        
        
    // NLP Focused Mode Logic
    if (input) {
        input.addEventListener('focus', () => {
            document.getElementById('searchWidgetSection').classList.add('nlp-focused-mode');
            const backIcon = document.getElementById('nlpBackIcon');
            if (backIcon) backIcon.style.display = 'flex';
            if (customPlaceholder) {
                customPlaceholder.style.display = 'none';
            }
        });

        input.addEventListener('input', (e) => {
            const val = e.target.value.toLowerCase();
            const trendingSection = document.getElementById('trendingPromptsSection');
            const autoSection = document.getElementById('autoSuggestionsSection');
            const isFocused = document.getElementById('searchWidgetSection').classList.contains('nlp-focused-mode');
            
            if (!isFocused) return; // Do not show anything if not in focused mode
            
            if (val.length === 0) {
                // If empty, show trending, hide auto
                if (trendingSection) trendingSection.style.display = 'block';
                if (autoSection) autoSection.style.display = 'none';
            } else if (val.includes('help me')) {
                // If they type help me, hide trending, show auto
                if (trendingSection) trendingSection.style.display = 'none';
                if (autoSection) autoSection.style.display = 'block';
            } else {
                // For now, if they type anything else, just hide both to be clean
                if (trendingSection) trendingSection.style.display = 'none';
                if (autoSection) autoSection.style.display = 'none';
            }
        });

        
        input.addEventListener('blur', () => {
            // If they click outside and input is empty but didn't click the back button, maybe restore it?
            // Actually, we'll only restore it when they click the back button to exit NLP mode completely.
            // But if we want it to come back if they don't type anything, we can do it here.
            setTimeout(() => {
                if (input.value.length === 0 && !document.getElementById('searchWidgetSection').classList.contains('nlp-focused-mode')) {
                    if (customPlaceholder) customPlaceholder.style.display = 'flex';
                }
            }, 100);
        });
    }

    window.exitNlpMode = function(e) {
        if(e) e.stopPropagation();
        document.getElementById('searchWidgetSection').classList.remove('nlp-focused-mode');
        const backIcon = document.getElementById('nlpBackIcon');
        if (backIcon) backIcon.style.display = 'none';
        if (customPlaceholder) {
            customPlaceholder.style.display = 'flex';
            customPlaceholder.style.left = '16px';
        }
        
        
        // Also hide trending prompts and auto suggestions
        const trendingSection = document.getElementById('trendingPromptsSection');
        const autoSection = document.getElementById('autoSuggestionsSection');
        if (trendingSection) trendingSection.style.display = 'none';
        if (autoSection) autoSection.style.display = 'none';

        
        // Clear input
        if (input) {
            input.value = '';
            // Trigger input event to restore custom placeholder
            input.dispatchEvent(new Event('input'));
        }
    };

        }
});


// Bank Offer Drawer
function openBankOffer(code, desc) {
    triggerHaptic('medium', 'Open Bank Offer');
    
    // Open drawer
    const backdrop = document.getElementById('bottomSheetBackdrop');
    const drawer = document.getElementById('bankOfferDrawer');
    if (backdrop && drawer) {
        backdrop.classList.add('visible');
        drawer.classList.add('visible');
    }
    
    // Scroll to the correct slide
    const container = document.getElementById('bankOfferScrollContainer');
    const slides = container.querySelectorAll('.bank-offer-slide');
    let targetIndex = 0;
    slides.forEach((slide, idx) => {
        if (slide.getAttribute('data-code') === code) {
            targetIndex = idx;
        }
    });
    
    // Timeout to allow drawer to be visible before scrolling
    setTimeout(() => {
        container.scrollTo({ left: targetIndex * container.clientWidth, behavior: 'instant' });
        updateBankOfferDots();
    }, 10);
}

function updateBankOfferDots() {
    const container = document.getElementById('bankOfferScrollContainer');
    const dotsContainer = document.getElementById('bankOfferDots');
    const countDisplay = document.getElementById('bankOfferCount');
    if (!container || !dotsContainer) return;
    
    const index = Math.round(container.scrollLeft / container.clientWidth);
    const dots = dotsContainer.querySelectorAll('.dot');
    
    dots.forEach((dot, i) => {
        if (i === index) {
            dot.style.width = '20px';
            dot.style.background = '#888';
        } else {
            dot.style.width = '6px';
            dot.style.background = '#D1D5DB';
        }
    });
    
    if (countDisplay) {
        countDisplay.innerText = `${index + 1}/5`;
    }
}

function copyBankOffer(code) {
    triggerHaptic('success', 'Copied Bank Offer');
    
    if (navigator.clipboard && code) {
        navigator.clipboard.writeText(code);
    }
    
    // Show toast
    showToast("Copied and apply at checkout");
    
    // Close drawer
    setTimeout(() => {
        closeAllDrawers();
    }, 400); // slight delay for better UX
}


window.openStudentBenefitsDrawer = function(event) {
    if (event) {
        event.stopPropagation();
    }
    const drawer = document.getElementById('studentBenefitsDrawer');
    const backdrop = document.getElementById('bottomSheetBackdrop');
    if (drawer && backdrop) {
        drawer.classList.add('visible');
        backdrop.classList.add('visible');
        if (typeof triggerHaptic === 'function') triggerHaptic('medium', 'Student Benefits Opened');
    }
};


window.fareOptions = {
    'Economy': [
        {
            id: 'lite',
            name: 'Fare Lite',
            isPopular: false,
            priceAdd: -500,
            features: [
                { icon: 'bag', text: '<strong>7 kg</strong> Cabin bag', type: 'tick' },
                { icon: 'luggage', text: 'No free Checkin bag', type: 'cross' },
                { icon: 'seat', text: 'Paid Seat Selection', type: 'cross' },
                { icon: 'cancel', text: 'Paid Cancellation', type: 'cross' }
            ]
        },
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
    const track = document.getElementById('cp-carousel');
    let html = '<div class="cp-carousel-padder"></div>';
    
    options.forEach((opt, idx) => {
        let popularHtml = '';
        if (opt.isPopular) {
            popularHtml = `<div class="cp-popular-badge ${opt.badgeClass || ''}">Popular fare</div>`;
        }
        
        let displayFeatures = JSON.parse(JSON.stringify(opt.features));
        if (typeof isStudentMode !== 'undefined' && isStudentMode && className === 'Economy') {
            displayFeatures.forEach(f => {
                if (f.icon === 'luggage') {
                    f.text = '<strong>25 kg</strong> Checkin bag <span style="color:var(--xairline-blue); font-size:9px; font-weight:700;">(Student +10kg)</span>';
                }
                if (f.icon === 'seat') {
                    f.text = '<strong>Free</strong> Standard Seat <span style="color:var(--xairline-blue); font-size:9px; font-weight:700;">(Student)</span>';
                    f.type = 'tick';
                }
            });
        }
        
        let featuresHtml = '';
        displayFeatures.forEach(f => {
            if (f.type === 'text-only') {
                featuresHtml += `<div class="cp-feature-item" style="justify-content: ${f.align || 'flex-start'}; margin-bottom: 12px; font-weight:700;">${f.text}</div>`;
            } else {
                const iconSvg = svgIcons[f.icon] || '';
                const itemClass = `cp-feature-item ${f.type === 'cross' ? 'cross' : 'highlighted'}`;
                featuresHtml += `<div class="${itemClass}">${iconSvg} <span>${f.text}</span></div>`;
            }
        });
        
        let totalFare = window.currentBaseFare + opt.priceAdd;
        let pricingHtml = '';
        let origFareAttr = '';
        
        if (typeof isStudentMode !== 'undefined' && isStudentMode && className === 'Economy') {
            const discountedFare = Math.floor(totalFare * 0.9);
            pricingHtml = `
                <div style="font-size: 10px; color: #999;">Student Fare from</div>
                <div style="font-size: 16px; font-weight: 800; color: #000;">
                    <span style="text-decoration: line-through; color: #999; font-size: 12px; font-weight: 600; margin-right: 4px;">₹${totalFare.toLocaleString('en-IN')}</span>
                    ₹ ${discountedFare.toLocaleString('en-IN')}<span style="font-size:11px; font-weight:400; color:#666;">/ Pax</span>
                </div>
            `;
            origFareAttr = `data-original-fare="${totalFare}"`;
            totalFare = discountedFare; // Set data-fare to discounted price so footer picks it up
        } else {
            pricingHtml = `
                <div style="font-size: 10px; color: #999;">Starting from</div>
                <div style="font-size: 16px; font-weight: 800; color: #000;">₹ ${totalFare.toLocaleString('en-IN')}<span style="font-size:11px; font-weight:400; color:#666;">/ Pax</span></div>
            `;
        }
        
        html += `
            <div class="cp-3d-card ${className === 'Stretch' ? 'stretch-mode' : ''}" data-fare="${totalFare}" ${origFareAttr} data-id="${opt.id}">
                <div class="cp-card-header">${opt.name}</div>
                ${popularHtml}
                <div class="cp-card-features">
                    ${featuresHtml}
                </div>
                <div class="cp-pricing-block">
                    ${pricingHtml}
                    <div style="font-size: 9px; color: var(--xairline-blue); font-weight: 700; margin-top: 8px;">Know More <svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-1px;"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg></div>
                </div>
            </div>
        `;
    });
    
    html += '<div class="cp-carousel-padder"></div>';
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
        const origFare = closestCard.getAttribute('data-original-fare');
        if (fare) {
            let footerHtml = '';
            if (origFare) {
                footerHtml = `<span style="text-decoration: line-through; color: #999; font-size: 14px; font-weight: 600; margin-right: 6px;">₹${parseInt(origFare).toLocaleString('en-IN')}</span>₹ ${parseInt(fare).toLocaleString('en-IN')}`;
            } else {
                footerHtml = '₹ ' + parseInt(fare).toLocaleString('en-IN');
            }
            document.getElementById('cp-total-fare').innerHTML = footerHtml;
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
                        <th>Lite</th>
                        <th>Saver</th>
                        <th class="compare-highlight">Flexi (Popular)</th>
                        <th>Upfront</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="feature-name">Cabin Baggage</td>
                        <td>7 kg</td>
                        <td>7 kg</td>
                        <td class="compare-highlight">7 kg</td>
                        <td>7 kg</td>
                    </tr>
                    <tr>
                        <td class="feature-name">Check-in Baggage</td>
                        <td>Paid</td>
                        <td>15 kg</td>
                        <td class="compare-highlight">15 kg</td>
                        <td>15 kg</td>
                    </tr>
                    <tr>
                        <td class="feature-name">Meals</td>
                        <td>❌</td>
                        <td>❌</td>
                        <td class="compare-highlight">✔️ Free Meal (Extra)</td>
                        <td>❌</td>
                    </tr>
                    <tr>
                        <td class="feature-name">Seat Selection</td>
                        <td>Paid</td>
                        <td>Paid</td>
                        <td class="compare-highlight">✔️ Free Standard Seat (Extra)</td>
                        <td>Paid</td>
                    </tr>
                    <tr>
                        <td class="feature-name">Date Change</td>
                        <td>Paid</td>
                        <td>Paid</td>
                        <td class="compare-highlight">✔️ Free Date Change (Extra)</td>
                        <td>Paid</td>
                    </tr>
                    <tr>
                        <td class="feature-name">Cancellation</td>
                        <td>Paid</td>
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

window.openLayoverPopup = function(terminalStr, timeStr, baggageStr, changeStr, totalStr) {
    document.getElementById('layoverPopupTerminal').innerText = terminalStr;
    document.getElementById('layoverPopupTime').innerText = timeStr;
    document.getElementById('layoverPopupBaggage').innerText = baggageStr;
    document.getElementById('layoverPopupChange').innerText = changeStr;
    document.getElementById('layoverPopupTotalTime').innerText = totalStr;

    // Adjust sub-text for baggage
    const baggageSub = document.getElementById('layoverPopupBaggageSub');
    if (baggageStr.toLowerCase().includes('not checked')) {
        baggageSub.innerText = 'Please collect and re-check your bags.';
    } else {
        baggageSub.innerText = 'No need to collect your bags at layover.';
    }

    const popup = document.getElementById('layoverInfoPopup');
    const content = document.getElementById('layoverInfoPopupContent');
    if (popup) {
        popup.style.display = 'flex';
        // Small delay to allow display: flex to apply before animating opacity
        requestAnimationFrame(() => {
            popup.style.opacity = '1';
            content.style.transform = 'scale(1)';
        });
    }
};

window.closeLayoverPopup = function() {
    const popup = document.getElementById('layoverInfoPopup');
    const content = document.getElementById('layoverInfoPopupContent');
    if (popup) {
        popup.style.opacity = '0';
        content.style.transform = 'scale(0.95)';
        setTimeout(() => {
            popup.style.display = 'none';
        }, 300);
    }
};

// Add mouse drag scrolling to the carousel for desktop testing
document.addEventListener('DOMContentLoaded', () => {
    // We need a mutation observer or delegated events because the carousel content might be injected,
    // but the container #cp-carousel itself is static in index.html!
    const slider = document.getElementById('cp-carousel');
    if (!slider) return;

    let isDown = false;
    let startX;
    let scrollLeft;

    slider.addEventListener('mousedown', (e) => {
        isDown = true;
        startX = e.pageX - slider.offsetLeft;
        scrollLeft = slider.scrollLeft;
        // Pause scroll-snap while dragging for smoother feel
        slider.style.scrollSnapType = 'none';
    });
    slider.addEventListener('mouseleave', () => {
        isDown = false;
        slider.style.scrollSnapType = 'x mandatory';
        handleCarouselScroll();
    });
    slider.addEventListener('mouseup', () => {
        isDown = false;
        slider.style.scrollSnapType = 'x mandatory';
        handleCarouselScroll();
    });
    slider.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - slider.offsetLeft;
        const walk = (x - startX) * 1.5; 
        slider.scrollLeft = scrollLeft - walk;
    });
});

// PASSENGER DETAILS LOGIC
window.goToPassengerDetails = function() {
    closeFarePopup();
    
    // Set the total fare in the passenger screen
    const fareNode = document.getElementById('cp-total-fare');
    if (fareNode) {
        document.getElementById('passenger-total-fare').innerHTML = fareNode.innerHTML;
    }
    
    // Get class
    const fareType = document.querySelector('.cp-3d-card.active-center .cp-card-header');
    if (fareType) {
        document.getElementById('passenger-fare-type').innerText = fareType.innerText;
    }

    // Instead of navigateTo('screenPassenger') which lacks a handler:
    document.querySelectorAll('.screen').forEach(scr => scr.classList.remove('active'));
    document.getElementById('screenPassenger').classList.add('active');
    if (typeof appState !== 'undefined') appState.currentScreen = 'passenger';

    // Hide bottom nav for full-screen overlay
    const bottomNav = document.querySelector('.bottom-nav');
    if (bottomNav) bottomNav.style.display = 'none';

    // Scroll passenger body to top
    const pBody = document.querySelector('.passenger-body');
    if (pBody) pBody.scrollTop = 0;
};

window.openPassengerForm = function(id, name, type, gender) {
    document.getElementById('pf-id').value = id;
    document.getElementById('pf-type').value = type;
    document.getElementById('passenger-form-title').innerText = type + " " + id + " Details";
    
    // Reset or set fields
    document.getElementById('pf-fname').value = name;
    document.getElementById('pf-lname').value = '';
    document.getElementById('pf-dob').value = '';
    document.getElementById('pf-assistance').value = '';
    
    if (gender === 'Female') selectGender('Female');
    else selectGender('Male');

    // Dynamic Next Button logic
    const saveBtn = document.getElementById('savePassengerBtn');
    if (saveBtn) {
        const emptyCardsCount = document.querySelectorAll('.passenger-card.empty').length;
        if (emptyCardsCount <= 1) {
            saveBtn.innerText = 'All Done';
        } else {
            saveBtn.innerText = 'Save & Next Passenger';
        }
    }

    const backdrop = document.getElementById('bottomSheetBackdrop');
    const sheet = document.getElementById('paxDetailsDrawerModal');
    if (backdrop) backdrop.classList.add('visible');
    if (sheet) sheet.classList.add('visible');
};

window.selectGender = function(gender) {
    const male = document.getElementById('gender-male');
    const female = document.getElementById('gender-female');
    male.classList.remove('active');
    female.classList.remove('active');
    
    // Reset styles
    male.style.border = '1px solid #cbd5e1';
    male.style.background = 'transparent';
    male.style.color = '#64748b';
    
    female.style.border = '1px solid #cbd5e1';
    female.style.background = 'transparent';
    female.style.color = '#64748b';
    
    if (gender === 'Male') {
        male.classList.add('active');
        male.style.border = '1px solid var(--xairline-blue)';
        male.style.background = 'rgba(14,165,233,0.05)';
        male.style.color = '#0f172a';
    } else {
        female.classList.add('active');
        female.style.border = '1px solid var(--xairline-blue)';
        female.style.background = 'rgba(14,165,233,0.05)';
        female.style.color = '#0f172a';
    }
};



window.openBulkAddSheet = function() {
    const backdrop = document.getElementById('bottomSheetBackdrop');
    const sheet = document.getElementById('savedPassengersSheet');
    if (backdrop) backdrop.classList.add('visible');
    if (sheet) sheet.classList.add('visible');
};

window.toggleBulkCheckbox = function(el) {
    const cb = el.querySelector('input[type="checkbox"]');
    cb.checked = !cb.checked;
};

window.applyBulkAdd = function() {
    closeAllDrawers();
    // Simulate auto-filling 3 slots based on checkboxes
    let added = 1; // start after ragini (already 1)
    
    // Quick and dirty simulation
    document.querySelectorAll('.passenger-card.empty').forEach(card => {
        if (added < 3) { // Simulate adding 2 more
            card.classList.remove('empty');
            card.classList.add('completed');
            card.style.border = '2px solid #22c55e';
            const name = added === 1 ? 'Alka Pande' : 'Rajvardhan Shah';
            const num = card.id.split('-')[2];
            const type = card.querySelector('.passenger-type').innerText;
            card.setAttribute('onclick', `openPassengerForm(${num}, '${name}', '${type}', 'Female')`);
            card.innerHTML = `
                <div style="display: flex; align-items: center; gap: 16px;">
                    <div class="passenger-avatar" style="background: rgba(34, 197, 94, 0.1); color: #22c55e;">${name.substring(0,2).toUpperCase()}</div>
                    <div style="flex: 1;">
                        <div class="passenger-name" style="color: #22c55e;">${name}</div>
                        <div class="passenger-type">${type}</div>
                    </div>
                    <div class="passenger-status" style="font-size: 10px; color: var(--xairline-blue); font-weight: 800; text-align: right; margin-left: auto;">Edit ✏️</div>
                </div>
            `;
            added++;
        }
    });
    updatePassengerCount();
};

window.toggleSavedPassengerChip = function(el, name) {
    if (el.classList.contains('active')) {
        el.classList.remove('active');
        el.querySelector('.chip-checkbox').innerHTML = '';
        el.style.background = '#fff';
        el.style.border = '1px solid #cbd5e1';
        el.querySelector('.chip-checkbox').style.background = 'transparent';
        el.querySelector('.chip-checkbox').style.border = '1px solid #cbd5e1';
        
        // Find the card that has this name and clear it
        document.querySelectorAll('.passenger-card.completed').forEach(card => {
            const cardNameEl = card.querySelector('.passenger-name');
            if (cardNameEl && cardNameEl.innerText === name) {
                card.classList.remove('completed');
                card.classList.add('empty');
                card.style.border = '1px solid #cbd5e1';
                const num = card.id.split('-')[2];
                const type = card.querySelector('.passenger-type').innerText;
                card.setAttribute('onclick', `openPassengerForm(${num}, '', '${type}', '')`);
                card.innerHTML = `
                    <div style="display: flex; align-items: center; gap: 16px;">
                        <div style="flex: 1;">
                            <div class="passenger-name">Passenger ${num}</div>
                            <div class="passenger-type">${type}</div>
                        </div>
                        <div class="passenger-add-btn" style="font-size: 10px; color: var(--xairline-blue); font-weight: 800; text-align: right; margin-left: auto;">Add details ></div>
                    </div>
                `;
            }
        });
        updatePassengerCount();
    } else {
        el.classList.add('active');
        el.querySelector('.chip-checkbox').innerHTML = '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
        el.style.background = 'rgba(14, 165, 233, 0.05)';
        el.style.border = '1px solid var(--xairline-blue)';
        el.querySelector('.chip-checkbox').style.background = 'var(--xairline-blue)';
        el.querySelector('.chip-checkbox').style.border = 'none';
        
        // Auto-fill an empty card
        const emptyCard = document.querySelector('.passenger-card.empty');
        if (emptyCard) {
            emptyCard.classList.remove('empty');
            emptyCard.classList.add('completed');
            emptyCard.style.border = '2px solid #22c55e';
            const num = emptyCard.id.split('-')[2];
            const type = emptyCard.querySelector('.passenger-type').innerText;
            emptyCard.setAttribute('onclick', `openPassengerForm(${num}, '${name}', '${type}', 'Female')`);
            emptyCard.innerHTML = `
                <div style="display: flex; align-items: center; gap: 16px;">
                    <div class="passenger-avatar" style="background: rgba(34, 197, 94, 0.1); color: #22c55e;">${name.substring(0,2).toUpperCase()}</div>
                    <div style="flex: 1;">
                        <div class="passenger-name" style="color: #22c55e;">${name}</div>
                        <div class="passenger-type">${type}</div>
                    </div>
                    <div class="passenger-status" style="font-size: 10px; color: var(--xairline-blue); font-weight: 800; text-align: right; margin-left: auto;">Edit ✏️</div>
                </div>
            `;
            updatePassengerCount();
        }
    }
};

window.savePassengerForm = function() {
    const id = parseInt(document.getElementById('pf-id').value);
    const type = document.getElementById('pf-type').value;
    const fname = document.getElementById('pf-fname').value;
    
    if (!fname) {
        alert("Please enter the First Name.");
        return;
    }

    // Update the card on the main screen
    const card = document.getElementById('passenger-card-' + id);
    if (card) {
        card.classList.remove('empty');
        card.classList.add('completed');
        card.style.border = '2px solid #22c55e';
        
        // Ensure the Edit button works by updating the onclick attribute with the new name
        card.setAttribute('onclick', `openPassengerForm(${id}, '${fname}', '${type}', 'Male')`);
        
        const assistance = document.getElementById('pf-assistance') ? document.getElementById('pf-assistance').value : '';
        const wheelchairHtml = assistance === 'Wheelchair' ? `<div style="font-size: 10px; color: #f59e0b; background: rgba(245, 158, 11, 0.1); padding: 2px 6px; border-radius: 4px; display: inline-block; margin-top: 4px; font-weight: 700;">♿ Wheelchair Requested</div>` : '';
        
        card.innerHTML = `
            <div style="display: flex; align-items: center; gap: 12px;">
                <div class="passenger-avatar" style="background: rgba(34, 197, 94, 0.1); color: #22c55e;">${fname.substring(0,2).toUpperCase()}</div>
                <div style="flex: 1;">
                    <div class="passenger-name" style="color: #22c55e;">${fname}</div>
                    <div class="passenger-type" style="margin-bottom: 2px;">${type}</div>
                    ${wheelchairHtml}
                </div>
                <div class="passenger-status" style="font-size: 10px; color: var(--xairline-blue); font-weight: 800; text-align: right; margin-left: auto;">Edit ✏️</div>
            </div>
        `;
    }

    updatePassengerCount();
    closeAllDrawers();

    // AUTO-ADVANCE: Find the next empty passenger and open it
    setTimeout(() => {
        if (appState.currentScreen !== 'passenger') return;
        
        const nextEmpty = document.querySelector('.passenger-card.empty');
        if (nextEmpty) {
            nextEmpty.click(); // Programmatically click the next empty card to open its form
        }
    }, 400); // Wait for drawer to close smoothly before opening the next
};

window.updatePassengerCount = function() {
    const completedCards = document.querySelectorAll('.passenger-card.completed').length;
    document.getElementById('passenger-added-count').innerText = completedCards;
    
    const visibleCards = Array.from(document.querySelectorAll('.passenger-card')).filter(card => card.style.display !== 'none').length;
    
    const nextBtn = document.getElementById('passenger-next-btn');
    if (completedCards >= 4) { // Enable if they complete at least 4, or all visible
        nextBtn.disabled = false;
        nextBtn.style.opacity = '1';
        nextBtn.style.background = 'var(--xairline-blue)';
        nextBtn.style.color = '#fff';
    } else {
        nextBtn.disabled = true;
        nextBtn.style.opacity = '0.5';
    }
};


// Passenger Details: Show Remaining Cards
window.showRemainingCards = function() {
    const btn = document.getElementById('addRemainingBtn');
    if (btn) btn.style.display = 'none';

    // Show cards 6, 7, 8
    for (let i = 6; i <= 8; i++) {
        const card = document.getElementById('passenger-card-' + i);
        if (card) {
            card.style.display = 'flex';
            // Reset animation to ensure stagger effect plays
            card.style.animation = 'none';
            card.offsetHeight; // trigger reflow
            card.style.animation = `staggerFadeIn 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) forwards`;
            card.style.animationDelay = `${(i - 5) * 0.15}s`;
        }
    }
    
    // Update container padding if needed
};



// ==========================================================================
// ADD-ONS: RADICAL REDESIGN LOGIC
// ==========================================================================

let addonCart = {}; // { paxIndex: { total: 0, items: [] } }
let currentAddonPax = 0;
let masterTotalFare = 6182;
let baseFare = 6182;

function initAddonsScreen() {
    window.hasAutoOpenedUpfront = false;
    const feed = document.getElementById('addonsMainFeed');
    if (feed) {
        // Removed auto-open logic
        feed.onscroll = null;
    }

    closeAllDrawers();
    
    // Setup Complimentary Perks visibility
    const mealBanner = document.getElementById('complimentaryMealBanner');
    const loungeTag = document.getElementById('addonLoungeAccessTag');
    if (mealBanner) mealBanner.style.display = appState.hasComplimentaryPerks ? 'flex' : 'none';
    if (loungeTag) loungeTag.style.display = appState.hasComplimentaryPerks ? 'flex' : 'none';

    // 1. Populate Passenger Cart Headers
    const paxContainer = document.getElementById('addonPaxCartContainer');
    if (paxContainer) {
        paxContainer.innerHTML = '';
        const completedPax = document.querySelectorAll('.passenger-card.completed');
        let paxList = [];
        
        if (completedPax.length > 0) {
            completedPax.forEach((card, idx) => {
                const nameEl = card.querySelector('.passenger-name');
                const typeEl = card.querySelector('.passenger-type');
                if (nameEl && typeEl) {
                    paxList.push({ name: nameEl.innerText, type: typeEl.innerText });
                }
            });
        } else {
            paxList = [
                { name: 'Priyal', type: 'Adult' },
                { name: 'Rajendraprasad', type: 'Infant' },
                { name: 'Abhay', type: 'Senior Citizen' }
            ];
        }

        paxList.forEach((pax, idx) => {
            if (!addonCart[idx]) {
                addonCart[idx] = { total: 0, items: [] };
            }
            const chip = document.createElement('div');
            chip.className = `compact-pax-chip ${idx === 0 ? 'active' : ''}`;
            chip.id = `addon-person-${idx}`;
            chip.onclick = () => selectAddonPax(idx, chip);
            
            // Extract initials
            let initials = pax.name.substring(0,2).toUpperCase();
            if (pax.name.includes(' ')) {
                const parts = pax.name.split(' ');
                initials = parts[0][0] + (parts[1] ? parts[1][0] : '');
            }
            
            chip.innerHTML = `
                <div class="compact-pax-avatar">${initials}</div>
                <div class="compact-pax-info">
                    <div class="compact-pax-name">${pax.name}</div>
                    <div class="compact-pax-status">₹<span class="pax-chip-total">${addonCart[idx].total}</span> &bull; <span class="pax-chip-items">${addonCart[idx].items.length}</span> items</div>
                </div>
            `;
            paxContainer.appendChild(chip);
        });
        currentAddonPax = 0;
    }

    // 2. Setup Scroll-Spy
    setupScrollSpy();

    // 3. Smart Inclusion Freebies
    const oldMealBanner = document.getElementById('meal-freebie-banner');
    const baggageBanner = document.getElementById('baggage-freebie-banner');
    
    if (oldMealBanner) oldMealBanner.style.display = 'none';
    if (baggageBanner) baggageBanner.style.display = 'none';

    // Handle Complimentary Perks
    const mealPrices = document.querySelectorAll('.glass-price');
    const mealBtns = document.querySelectorAll('.glass-add-btn');

    if (appState.hasComplimentaryPerks) {
        // Make all meals FREE
        mealPrices.forEach(priceEl => priceEl.innerText = 'FREE');
        mealBtns.forEach(btn => {
            btn.innerText = 'Add';
            // We'll dynamically override the price in toggleAddonCart if it sees "FREE"
            btn.setAttribute('data-is-free', 'true');
        });
    } else {
        // Reset pricing
        mealPrices.forEach(priceEl => {
            if (priceEl.id === 'veg-meal-price') priceEl.innerText = '₹ 370';
            // Other meals can be hardcoded or left alone if we didn't change them
        });
        mealBtns.forEach(btn => {
            btn.innerText = 'Add';
            btn.removeAttribute('data-is-free');
            btn.style.background = '';
            btn.style.borderColor = '';
        });
    }

    updateMasterTotal();
}

// Ensure initAddonsScreen is called from navigateTo
// (This was already added in the previous step's teardown/rebuild logic)

function selectAddonPax(index, chipEl) {
    currentAddonPax = index;
    document.querySelectorAll('.compact-pax-chip').forEach(c => c.classList.remove('active'));
    chipEl.classList.add('active');
    const container = chipEl.parentElement;
    if (container) {
        const scrollLeftTarget = chipEl.offsetLeft - (container.offsetWidth / 2) + (chipEl.offsetWidth / 2);
        container.scrollTo({ left: scrollLeftTarget, behavior: 'smooth' });
    }
    triggerHaptic('light', 'Switched passenger');
}

function toggleAddonCart(btn, itemName, price) {
    if (btn.innerText === 'Included') return;
    
    const isAdded = btn.classList.contains('added');
    const isFree = btn.getAttribute('data-is-free') === 'true';
    const actualPrice = isFree ? 0 : price;
    
    if (isAdded) {
        btn.classList.remove('added');
        btn.innerHTML = btn.classList.contains('neon-add-btn') ? 'Add to Cart' : 'Add';
        addonCart[currentAddonPax].total -= actualPrice;
        const index = addonCart[currentAddonPax].items.indexOf(itemName);
        if (index > -1) addonCart[currentAddonPax].items.splice(index, 1);
        triggerHaptic('medium', 'Removed');
    } else {
        btn.classList.add('added');
        btn.innerHTML = 'Added ✓';
        addonCart[currentAddonPax].total += actualPrice;
        addonCart[currentAddonPax].items.push(itemName);
        triggerHaptic('success', 'Added');
        
        // Fly animation could go here
    }
    
    // Update individual passenger chip
    const chip = document.getElementById(`pax-chip-${currentAddonPax}`);
    if (chip) {
        chip.querySelector('.pax-chip-total').innerText = addonCart[currentAddonPax].total;
        chip.querySelector('.pax-chip-items').innerText = addonCart[currentAddonPax].items.length;
    }
    
    updateMasterTotal();
}

function updateMasterTotal() {
    let addonsSum = 0;
    for (let key in addonCart) {
        addonsSum += addonCart[key].total;
    }
    masterTotalFare = baseFare + addonsSum;
    const totalEl = document.getElementById('addon-checkout-total');
    if (totalEl) totalEl.innerText = `₹ ${masterTotalFare.toLocaleString('en-IN')}`;
}

// SCROLL SPY LOGIC
function setupScrollSpy() {
    const feed = document.getElementById('addonsMainFeed');
    const sections = document.querySelectorAll('.addon-scroll-section');
    const tabs = document.querySelectorAll('.spy-tab');
    
    if (!feed || sections.length === 0) return;
    
    feed.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(sec => {
            const secTop = sec.offsetTop;
            const secHeight = sec.clientHeight;
            if (feed.scrollTop >= (secTop - 150)) {
                current = sec.getAttribute('id').replace('section-', '');
            }
        });
        
        tabs.forEach(tab => {
            tab.classList.remove('active');
            if (tab.innerText.toLowerCase().includes(current)) {
                tab.classList.add('active');
                
                // Manually calculate horizontal scroll to avoid scrollIntoView vertical jump bug
                const container = tab.parentElement;
                const scrollLeftTarget = tab.offsetLeft - (container.offsetWidth / 2) + (tab.offsetWidth / 2);
                container.scrollTo({ left: scrollLeftTarget, behavior: 'smooth' });
            }
        });
    });
}

function scrollToAddonSection(id) {
    const feed = document.getElementById('addonsMainFeed');
    const section = document.getElementById(`section-${id}`);
    if (feed && section) {
        // smooth scroll to section
        feed.scrollTo({
            top: section.offsetTop - 20,
            behavior: 'smooth'
        });
    }
}

// MEAL FILTERS
function filterMeals(type, filterBtn) {
    document.querySelectorAll('.meal-filter').forEach(btn => btn.classList.remove('active'));
    filterBtn.classList.add('active');
    triggerHaptic('light', 'Filtered meals');
    
    const meals = document.querySelectorAll('.immersive-meal-card');
    meals.forEach(meal => {
        if (type === 'all' || meal.getAttribute('data-type') === type) {
            meal.style.display = 'block';
        } else {
            meal.style.display = 'none';
        }
    });
}

// BAGGAGE STEPPER
let baggageExtra = 0;
function updateBaggage(change) {
    const valEl = document.getElementById('baggage-val');
    const costEl = document.getElementById('baggage-cost');
    
    if (!valEl || !costEl) return;
    
    let currentVal = parseInt(valEl.innerText);
    currentVal += change;
    if (currentVal < 0) currentVal = 0;
    
    // Calculate difference
    const diff = currentVal - baggageExtra;
    baggageExtra = currentVal;
    
    valEl.innerText = baggageExtra;
    
    const cost = baggageExtra * 100; // 100 rs per kg
    costEl.innerText = `₹ ${cost}`;
    
    // Update master cart directly for baggage
    addonCart[currentAddonPax].total += (diff * 100);
    if (change > 0) showToast('Added ' + change + 'kg Extra Baggage');

    
    const chip = document.getElementById(`pax-chip-${currentAddonPax}`);
    if (chip) {
        chip.querySelector('.pax-chip-total').innerText = addonCart[currentAddonPax].total;
    }
    updateMasterTotal();
    triggerHaptic('light', 'Baggage updated');
}


window.upgradeToUpfront = function() {
    triggerHaptic('medium', 'Upgrade');
    
    // Update the UI on the Addons screen
    const statusText = document.getElementById('upfront-status-text');
    if (statusText) {
        statusText.innerText = 'Upgraded to UpFront!';
        statusText.style.color = '#15803d'; // Green color for success
    }
    
    const seeBenefitsBtn = document.getElementById('upfront-see-benefits-btn');
    if (seeBenefitsBtn) {
        seeBenefitsBtn.style.display = 'none';
    }
    
    // Add to total fare
    masterTotalFare += 2499;
    const addonTotal = document.getElementById('addon-checkout-total');
    if (addonTotal) {
        addonTotal.innerText = '₹ ' + masterTotalFare.toLocaleString('en-IN');
    }
    
    // Also update passenger total fare just in case
    const paxTotal = document.getElementById('passenger-total-fare');
    if (paxTotal) {
        paxTotal.innerText = '₹ ' + masterTotalFare.toLocaleString('en-IN');
    }
    
    closeAllDrawers();
    
    setTimeout(() => {
        showToast('Successfully upgraded to UpFront for ₹2,499!');
    }, 300);
};

window.closeUpfrontDrawerAndShowBanner = function() {
    closeAllDrawers();
    const banner = document.getElementById('upfront-sticky-banner');
    if (banner) {
        banner.style.display = 'flex';
    }
};

// Partners Carousel Auto-Scroll Logic
function initPartnersCarousel() {
    const tracks = document.querySelectorAll('.partnersCarouselTrack');
    if (!tracks || tracks.length === 0) return;
    
    tracks.forEach(track => {
        setInterval(() => {
            const maxScroll = track.scrollWidth - track.clientWidth;
            
            if (track.scrollLeft >= maxScroll - 10) {
                track.style.scrollBehavior = 'auto';
                track.scrollLeft = 0;
                void track.offsetHeight;
                track.style.scrollBehavior = 'smooth';
            }
            
            const cards = track.querySelectorAll('.partner-box');
            let nextScroll = 0;
            
            for (let card of cards) {
                let cardLeft = card.offsetLeft;
                if (cardLeft > track.scrollLeft + 5) {
                    nextScroll = cardLeft;
                    break;
                }
            }
            
            if (nextScroll > 0) {
                track.scrollTo({ left: nextScroll, behavior: 'smooth' });
            }
        }, 3000);
    });
}

// Ensure it starts
document.addEventListener('DOMContentLoaded', () => {
    initPartnersCarousel();
});

window.openUpfrontDrawer = function() {
    const drawer = document.getElementById('addonBenefitsDrawer');
    const backdrop = document.getElementById('bottomSheetBackdrop');
    if (drawer && backdrop) {
        drawer.classList.add('visible');
        backdrop.classList.add('visible');
        
        const feed = document.getElementById('addonsMainFeed');
        if (feed) {
            feed.style.overflowY = 'hidden';
        }
    }
};


// ==========================================================================
// SEAT MAP LOGIC
// ==========================================================================

let seatMapState = {
    currentPaxIndex: 0,
    paxList: [],
    assignments: {}, // maps paxIndex -> { seatId: '1A', type: 'stretch', price: 750 }
};

function initSeatMapScreen() {
    // 1. Setup Passengers
    const completedPax = document.querySelectorAll('.passenger-card.completed');
    let list = [];
    if (completedPax.length > 0) {
        completedPax.forEach((card) => {
            const nameEl = card.querySelector('.passenger-name');
            const typeEl = card.querySelector('.passenger-type');
            const onclickAttr = card.getAttribute('onclick') || '';
            let gender = '';
            if (onclickAttr.includes("'Female'")) gender = 'Female';
            else if (onclickAttr.includes("'Male'")) gender = 'Male';
            
            if (nameEl && typeEl) list.push({ name: nameEl.innerText, type: typeEl.innerText, gender });
        });
    } else {
        list = [
            { name: 'Rahul Sharma', type: 'Adult', gender: 'Male' },
            { name: 'Anita Sharma', type: 'Adult', gender: 'Female' },
            { name: 'Aarav Sharma', type: 'Child', gender: 'Male' }
        ];
    }
    seatMapState.paxList = list;
    
    // 2. Render Passenger Chips
    renderSeatMapPaxChips();
    
    // 3. Render Grid
    renderSeatMapGrid();
    
    // 4. Init Bottom Bar
    updateSeatMapFooterCTA();
    
    // 5. Evaluate and display seat cohorts
    evaluateSeatCohorts();
}

function getPaxInitials(name) {
    let initials = name.substring(0,2).toUpperCase();
    if (name.includes(' ')) {
        const parts = name.split(' ');
        initials = parts[0][0] + (parts[1] ? parts[1][0] : '');
    }
    return initials;
}

function renderSeatMapPaxChips() {
    const container = document.getElementById('seatMapPaxCartContainer');
    if (!container) return;
    
    container.innerHTML = '';
    seatMapState.paxList.forEach((pax, idx) => {
        const chip = document.createElement('div');
        chip.id = `seatmap-pax-${idx}`;
        chip.style.cssText = `
            flex-shrink: 0;
            width: 120px;
            border: 2px solid ${idx === seatMapState.currentPaxIndex ? '#0066FF' : '#e2e8f0'};
            border-radius: 8px;
            padding: 6px 10px;
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            background: ${idx === seatMapState.currentPaxIndex ? '#f0fdf4' : '#fff'};
            transition: all 0.2s;
        `;
        chip.onclick = () => selectSeatMapPax(idx, chip);
        
        let imgHtml = `<div style="width: 24px; height: 24px; border-radius: 50%; background: #0f172a; color: white; display: flex; justify-content: center; align-items: center; font-size: 9px; font-weight: 800;">${getPaxInitials(pax.name)}</div>`;
        
        const assignment = seatMapState.assignments[idx];
        let statusText = '--';
        if (assignment) {
            const displayPrice = assignment.isFree ? 'Free' : `₹${assignment.price}`;
            statusText = `${assignment.seatId} <span style="color:#64748b; font-weight:600;">• ${displayPrice}</span>`;
        }
        
        chip.innerHTML = `
            ${imgHtml}
            <div>
                <div style="font-size: 11px; font-weight: 800; color: #0f172a; line-height: 1.2;">${pax.name}</div>
                <div style="font-size: 9px; font-weight: 600; color: #64748b; margin-top: 2px;">SEAT <span id="seatmap-pax-status-${idx}" style="color: ${assignment ? '#0066FF' : '#94a3b8'}; font-weight: 800; margin-left: 2px;">${statusText}</span></div>
            </div>
        `;
        container.appendChild(chip);
    });
}

function selectSeatMapPax(idx) {
    triggerHaptic('light', 'Pax Changed');
    seatMapState.currentPaxIndex = idx;
    renderSeatMapPaxChips();
}

function renderSeatMapGrid() {
    const grid = document.getElementById('seatMapGrid');
    if (!grid) return;
    
    grid.innerHTML = '';
    
    for (let r = 1; r <= 30; r++) {
        // Section Headers
        if (r === 1) {
            const banner = document.createElement('div');
            banner.style.cssText = 'text-align: center; margin-bottom: 24px; padding-top: 16px;';
            banner.innerHTML = '<span style="color: #94a3b8; font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;">Stretch seats</span>';
            grid.appendChild(banner);
        } else if (r === 4) {
            const banner = document.createElement('div');
            banner.style.cssText = 'text-align: center; margin: 24px 0 16px 0;';
            banner.innerHTML = '<span style="color: #94a3b8; font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;">Upfront seats</span>';
            grid.appendChild(banner);
        } else if (r === 6) {
            const banner = document.createElement('div');
            banner.style.cssText = 'text-align: center; margin: 24px 0 16px 0;';
            banner.innerHTML = '<span style="color: #94a3b8; font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;">Economy seats</span>';
            grid.appendChild(banner);
        }

        // Wing exit indicator
        if (r === 12 || r === 13) {
            const exitBanner = document.createElement('div');
            exitBanner.style.cssText = 'text-align: center; margin: 16px 0 8px 0;';
            exitBanner.innerHTML = '<span style="color: #ea580c; font-size: 10px; font-weight: 800; letter-spacing: 1px;">EMERGENCY EXIT ROW</span>';
            grid.appendChild(exitBanner);
        }

        const rowDiv = document.createElement('div');
        rowDiv.className = 'seat-row';
        if (r === 12 || r === 13) rowDiv.classList.add('exit-row');

        if (r <= 3) {
            rowDiv.classList.add('stretch-row');
            
            // Left Side (A, C)
            ['A', 'C'].forEach(letter => {
                rowDiv.appendChild(createSeat(r, letter));
            });
            
            // Aisle
            const aisle = document.createElement('div');
            aisle.className = 'seat-aisle';
            aisle.innerText = `ROW ${r}`;
            rowDiv.appendChild(aisle);
            
            // Right Side (D, F)
            ['D', 'F'].forEach(letter => {
                rowDiv.appendChild(createSeat(r, letter));
            });
        } else {
            if (r === 4 || r === 5) rowDiv.classList.add('upfront-row');
            
            // Left Side (A, B, C)
            ['A', 'B', 'C'].forEach(letter => {
                rowDiv.appendChild(createSeat(r, letter));
            });
            
            // Aisle
            const aisle = document.createElement('div');
            aisle.className = 'seat-aisle';
            aisle.innerText = `ROW ${r}`;
            rowDiv.appendChild(aisle);
            
            // Right Side (D, E, F)
            ['D', 'E', 'F'].forEach(letter => {
                rowDiv.appendChild(createSeat(r, letter));
            });
        }
        
        grid.appendChild(rowDiv);
    }
}

function createSeat(row, letter) {
    const seatId = `${row}${letter}`;
    const el = document.createElement('div');
    
    // Determine seat type
    let type = 'standard';
    let basePrice = 350;
    
    if (row <= 3 || row === 12 || row === 13) {
        type = 'stretch';
        basePrice = 800;
    } else if (row === 4 || row === 5) {
        type = 'upfront';
        basePrice = 750;
    }
    
    // Randomly occupy some seats (deterministic based on seatId)
    const seed = (row * 31 + letter.charCodeAt(0)) % 100;
    const isOccupied = seed < 25; // 25% occupied
    
    if (isOccupied) type = 'occupied';
    
    // Handle Free Perks
    const isFree = appState.hasComplimentaryPerks && type !== 'occupied';
    if (isFree) type = 'free';
    
    const finalPrice = isFree ? 0 : basePrice;
    
    el.className = `seat-3d seat-${type}`;
    el.id = `seat-${seatId}`;
    
    // Inner HTML
    let innerSeatHtml = `
        <div class="seat-backrest"></div>
        <div class="seat-cushion">
            <div class="seat-armrest seat-armrest-left"></div>
            <div class="seat-armrest seat-armrest-right"></div>
            <div class="seat-content">
    `;

    if (type === 'occupied') {
        innerSeatHtml += `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" style="opacity: 0.4; margin-top: 4px;"><path d="M18 6L6 18M6 6l12 12"/></svg>`;
    } else {
        innerSeatHtml += `
            <div class="seat-label">${seatId}</div>
        `;
    }

    innerSeatHtml += `
            </div>
        </div>
    `;
    
    el.innerHTML = innerSeatHtml;
    
    if (type !== 'occupied') {
        el.onclick = () => selectSeat(seatId, type, finalPrice, isFree);
    } else {
        el.onclick = () => {
            triggerHaptic('error', 'Seat Taken');
            showToast('Seat not available');
        };
    }
    
    return el;
}

function hoverSeat(seatId) {
    // Check if this seat is assigned to any pax
    let assignedPaxIdx = -1;
    for (const p in seatMapState.assignments) {
        if (seatMapState.assignments[p].seatId === seatId) {
            assignedPaxIdx = parseInt(p);
            break;
        }
    }
    
    if (assignedPaxIdx !== -1) {
        const chip = document.getElementById(`seatmap-pax-${assignedPaxIdx}`);
        const container = document.getElementById('seatMapPaxCartContainer');
        if (chip && container) {
            // Scroll container so the chip becomes the "first" visible card on the left
            container.scrollTo({
                left: chip.offsetLeft - 16, // offset to account for container padding
                behavior: 'smooth'
            });
        }
    }
}

function selectSeat(seatId, type, price, isFree) {
    const idx = seatMapState.currentPaxIndex;
    
    // Check if this seat is already selected by someone
    let alreadyAssignedTo = -1;
    for (const p in seatMapState.assignments) {
        if (seatMapState.assignments[p].seatId === seatId) {
            alreadyAssignedTo = parseInt(p);
            break;
        }
    }
    
    if (alreadyAssignedTo !== -1 && alreadyAssignedTo !== idx) {
        // Switch to the passenger who holds this seat
        selectSeatMapPax(alreadyAssignedTo);
        
        // Scroll their card into view
        const chip = document.getElementById(`seatmap-pax-${alreadyAssignedTo}`);
        const container = document.getElementById('seatMapPaxCartContainer');
        if (chip && container) {
            container.scrollTo({
                left: chip.offsetLeft - 16,
                behavior: 'smooth'
            });
        }
        return;
    }
    
    // Deselect previously selected seat for this pax
    const previous = seatMapState.assignments[idx];
    if (previous) {
        const prevEl = document.getElementById(`seat-${previous.seatId}`);
        if (prevEl) {
            prevEl.classList.remove('seat-selected');
            const avatar = prevEl.querySelector('.seat-pax-avatar');
            if (avatar) avatar.remove();
            const oldTooltip = prevEl.querySelector('.seat-price-tooltip');
            if (oldTooltip) oldTooltip.remove();
        }
    }
    
    // If clicking same seat, deselect it
    if (previous && previous.seatId === seatId) {
        delete seatMapState.assignments[idx];
        triggerHaptic('medium', 'Seat Deselected');
        const currEl = document.getElementById(`seat-${seatId}`);
        if (currEl) {
            const oldTooltip = currEl.querySelector('.seat-price-tooltip');
            if (oldTooltip) oldTooltip.remove();
        }
    } else {
        // Select new seat
        seatMapState.assignments[idx] = { seatId, type, price, isFree };
        const newEl = document.getElementById(`seat-${seatId}`);
        if (newEl) {
            newEl.classList.add('seat-selected');
            
            // Add pax avatar to seat
            const paxName = seatMapState.paxList[idx].name;
            const initials = getPaxInitials(paxName);
            const avatar = document.createElement('div');
            avatar.className = 'seat-pax-avatar';
            avatar.innerText = initials;
            newEl.appendChild(avatar);
            
            // Show beautiful floating price tooltip
            const tooltip = document.createElement('div');
            tooltip.className = 'seat-price-tooltip';
            const displayPrice = isFree ? 'Free' : `₹${price}`;
            tooltip.innerHTML = `<span style="font-size: 10px; opacity: 0.8; margin-right: 4px;">Added</span><span style="font-weight: 800; font-size: 13px;">${displayPrice}</span>`;
            
            Object.assign(tooltip.style, {
                position: 'absolute',
                bottom: '100%',
                left: '50%',
                transform: 'translateX(-50%) translateY(8px)',
                background: 'rgba(20, 20, 30, 0.95)',
                backdropFilter: 'blur(10px)',
                color: '#fff',
                padding: '6px 12px',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'baseline',
                boxShadow: '0 10px 25px rgba(0,0,0,0.3), 0 2px 8px rgba(0,0,0,0.2)',
                opacity: '0',
                transition: 'all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)',
                pointerEvents: 'none',
                zIndex: '100',
                whiteSpace: 'nowrap',
                border: '1px solid rgba(255,255,255,0.1)'
            });
            
            newEl.appendChild(tooltip);
            
            // Trigger animation
            requestAnimationFrame(() => {
                tooltip.style.opacity = '1';
                tooltip.style.transform = 'translateX(-50%) translateY(-10px)';
            });
            
            // Remove after 2.5 seconds
            setTimeout(() => {
                if (tooltip.parentElement) {
                    tooltip.style.opacity = '0';
                    tooltip.style.transform = 'translateX(-50%) translateY(-4px)';
                    setTimeout(() => tooltip.remove(), 400);
                }
            }, 2500);
        }
        triggerHaptic('success', `Selected ${seatId}`);
    }
    
    // Update UI
    renderSeatMapPaxChips();
    updateSeatMapFooterCTA();
    
    // Auto-advance to next passenger if available
    if (seatMapState.assignments[idx] && idx < seatMapState.paxList.length - 1) {
        setTimeout(() => {
            selectSeatMapPax(idx + 1);
        }, 500);
    }
}

function updateSeatMapFooterCTA() {
    // 1. Update Total Fare
    let total = 6182; // Base flight fare
    let seatTotal = 0;
    for (const p in seatMapState.assignments) {
        seatTotal += seatMapState.assignments[p].price;
    }
    // APPLY DISCOUNT
    if (seatMapState.cohortDiscount) {
        seatTotal = Math.round(seatTotal * (1 - seatMapState.cohortDiscount));
    }
    
    total += seatTotal;
    
    const priceEl = document.getElementById('seatMapSelectedSeatPrice');
    if (priceEl) priceEl.innerText = `₹${total.toLocaleString('en-IN')}`;
    
    // Note: The indicator circles were removed from the new layout to match the UpFront footer design.
}

function evaluateSeatCohorts() {
    const container = document.getElementById('seatCohortBannerContainer');
    if (!container) return;
    
    container.innerHTML = '';
    
    // Family/Group Cohort: 2 or more passengers
    if (seatMapState.paxList.length >= 2) {
        container.style.display = 'flex';
        container.innerHTML = `
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="background: linear-gradient(135deg, #001b94, #2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; font-size: 15px; font-style: italic; letter-spacing: -0.3px; white-space: nowrap;">Sit Together</div>
                <div style="display: flex; align-items: center; gap: 6px; font-size: 11px; font-weight: 700; color: #4338ca; white-space: nowrap;">
                    Rows 14-16
                    <span style="background: #eef2ff; border: 1px solid #c7d2fe; color: #3730a3; font-size: 9px; font-weight: 800; padding: 2px 6px; border-radius: 6px; display: flex; align-items: center; gap: 4px; letter-spacing: 0.2px; line-height: 1.2;">
                        <span style="color: #fbbf24; font-size: 10px; line-height: 1;">✨</span> 20% OFF
                    </span>
                </div>
            </div>
            <div onclick="autoAssignCohortSeats('family')" style="font-size: 10px; font-weight: 900; color: #4338ca; text-transform: uppercase; letter-spacing: 0.8px; cursor: pointer; display: flex; align-items: center; gap: 4px; white-space: nowrap;">
                ADD
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="#4338ca" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </div>
        `;
    }
    // Solo Female Cohort: 1 passenger who is Female
    else if (seatMapState.paxList.length === 1 && seatMapState.paxList[0].gender === 'Female') {
        container.style.display = 'flex';
        container.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="background: linear-gradient(135deg, #001b94, #2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; font-size: 15px; font-style: italic; letter-spacing: -0.3px;">Solo Female</div>
                <div style="font-size: 11px; font-weight: 700; color: #4338ca;">Sit with a female pax</div>
            </div>
            <div onclick="autoAssignCohortSeats('solo-female')" style="font-size: 10px; font-weight: 900; color: #4338ca; text-transform: uppercase; letter-spacing: 0.8px; cursor: pointer; display: flex; align-items: center; gap: 4px;">
                ADD
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="#4338ca" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </div>
        `;
    } else {
        container.style.display = 'none';
    }
}

function autoAssignCohortSeats(cohortType) {
    if (cohortType === 'family') {
        const rows = ['10', '11', '12', '14', '15'];
        let firstSeat = null;
        for (let row of rows) {
            const seats = ['C', 'D', 'E', 'F'];
            let allFree = true;
            let elements = [];
            for (let s of seats) {
                const el = document.getElementById(`seat-${row}${s}`);
                if (!el || el.classList.contains('occupied') || el.classList.contains('seat-unavailable')) {
                    allFree = false;
                    break;
                }
                elements.push(el);
            }
            if (allFree) {
                // Clear any existing assignments
                seatMapState.assignments = {};
                
                // Assign them using handleSeatClick logic directly
                elements.forEach((el, index) => {
                    seatMapState.assignments[index] = { 
                        seatId: `${row}${seats[index]}`, 
                        type: 'standard', 
                        price: 300, 
                        isFree: false 
                    };
                    
                    el.classList.add('seat-selected');
                    const initials = getPaxInitials(seatMapState.paxList[index].name);
                    const avatar = document.createElement('div');
                    avatar.className = 'seat-pax-avatar';
                    avatar.innerText = initials;
                    el.appendChild(avatar);
                });
                
                seatMapState.cohortDiscount = 0.10;
                firstSeat = elements[1]; // D seat
                break;
            }
        }
        
        if (firstSeat) {
            renderSeatMapPaxChips();
            updateSeatMapFooterCTA();
            triggerHaptic('success', 'Family Seats Assigned');
            panCameraToSeat(firstSeat);
            document.getElementById('seatCohortBannerContainer').style.display = 'none';
        } else {
            showToast('No adjacent seats found for 4 passengers');
        }
    } else if (cohortType === 'solo-female') {
        const target = document.getElementById('seat-12F');
        if (target && !target.classList.contains('occupied')) {
            seatMapState.assignments = {};
            seatMapState.assignments[0] = { seatId: '12F', type: 'standard', price: 150, isFree: false };
            
            target.classList.add('seat-selected');
            const initials = getPaxInitials(seatMapState.paxList[0].name);
            const avatar = document.createElement('div');
            avatar.className = 'seat-pax-avatar';
            avatar.innerText = initials;
            target.appendChild(avatar);
            
            const neighbor = document.getElementById('seat-12E');
            if (neighbor) {
                neighbor.classList.add('occupied');
                neighbor.style.borderColor = '#db2777'; 
                neighbor.style.background = '#fce7f3';
                
                const neighborAvatar = document.createElement('div');
                neighborAvatar.style.cssText = 'position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 16px; height: 16px; background: #db2777; border-radius: 50%; color: white; display: flex; justify-content: center; align-items: center; font-size: 8px; font-weight: bold;';
                neighborAvatar.innerText = '👩';
                neighbor.appendChild(neighborAvatar);
            }
            
            seatMapState.cohortDiscount = 0;
            renderSeatMapPaxChips();
            updateSeatMapFooterCTA();
            triggerHaptic('success', 'Seat Assigned');
            panCameraToSeat(target);
            document.getElementById('seatCohortBannerContainer').style.display = 'none';
        }
    }
}

function panCameraToSeat(seatElement) {
    if (!seatElement) return;
    
    let offsetTop = 0;
    let offsetLeft = 0;
    let el = seatElement;
    const fuselage = document.getElementById('seatMapFuselage');
    
    while (el && el !== fuselage) {
        offsetTop += el.offsetTop;
        offsetLeft += el.offsetLeft;
        el = el.offsetParent;
    }
    
    let targetY = 250 - offsetTop;
    if (targetY > 50) targetY = 50;
    if (targetY < -2000) targetY = -2000;
    
    let targetX = 165 - offsetLeft;
    if (targetX > 150) targetX = 150;
    if (targetX < -150) targetX = -150;
    
    const startX = seatMapPanState.x;
    const startY = seatMapPanState.y;
    const frames = 30;
    let frame = 0;
    
    function animate() {
        frame++;
        const progress = frame / frames;
        const ease = 1 - Math.pow(1 - progress, 3);
        
        if (seatMapPanState.is3DHorizontal) {
            // Wait, mapping back to logical coordinates might be complex here.
            // Let's just force the vertical mode coordinates for simplicity,
            // or animate the logical coordinates directly:
            seatMapPanState.x = startX + (targetX - startX) * ease;
            seatMapPanState.y = startY + (targetY - startY) * ease;
        } else {
            seatMapPanState.x = startX + (targetX - startX) * ease;
            seatMapPanState.y = startY + (targetY - startY) * ease;
        }
        
        updateSeatMapTransform();
        
        if (frame < frames) {
            requestAnimationFrame(animate);
        } else {
            seatElement.style.transition = 'transform 0.3s, box-shadow 0.3s';
            seatElement.style.transform = 'scale(1.2)';
            seatElement.style.boxShadow = '0 0 20px rgba(0, 102, 255, 0.8)';
            setTimeout(() => {
                seatElement.style.transform = '';
                seatElement.style.boxShadow = '';
            }, 600);
        }
    }
    animate();
}

function confirmSeatSelection() {
    triggerHaptic('success', 'Seats Confirmed');
    navigateTo('addons');
}

// ==========================================================================
// SEAT MAP PAN, ZOOM & ROTATE
// ==========================================================================

let seatMapPanState = {
    isDragging: false,
    startX: 0,
    startY: 0,
    x: 0,
    y: 0,
    scale: 1,
    is3DHorizontal: false
};

let floatingControlTimeout;
function setFloatingControlsVisibility(show) {
    const controls = document.getElementById('seatMapFloatingControls');
    if (!controls) return;
    if (show) {
        controls.style.transform = 'translateX(0)';
        controls.style.opacity = '1';
        controls.style.pointerEvents = 'auto';
    } else {
        controls.style.transform = 'translateX(150%)';
        controls.style.opacity = '0.3'; // Dim instead of completely hide, or just slide out
        controls.style.pointerEvents = 'none';
    }
}

function initSeatMapPanZoom() {
    const wrapper = document.getElementById('seatMapPanZoomArea');
    if (!wrapper) return;

    // Prevent interactions on the floating controls from triggering map pan/zoom
    const controls = document.getElementById('seatMapFloatingControls');
    if (controls) {
        const stopProp = (e) => e.stopPropagation();
        controls.addEventListener('mousedown', stopProp);
        controls.addEventListener('touchstart', stopProp);
        controls.addEventListener('touchmove', stopProp);
        controls.addEventListener('wheel', stopProp);
    }

    wrapper.addEventListener('touchstart', (e) => {
        clearTimeout(floatingControlTimeout);
        setFloatingControlsVisibility(false);
        if (e.touches.length === 1) {
            seatMapPanState.isDragging = true;
            seatMapPanState.startX = e.touches[0].clientX;
            seatMapPanState.startY = e.touches[0].clientY;
            seatMapPanState.logicalStartX = seatMapPanState.x;
            seatMapPanState.logicalStartY = seatMapPanState.y;
        } else if (e.touches.length === 2) {
            seatMapPanState.isDragging = false;
            const dx = e.touches[0].clientX - e.touches[1].clientX;
            const dy = e.touches[0].clientY - e.touches[1].clientY;
            seatMapPanState.initialPinchDistance = Math.sqrt(dx*dx + dy*dy);
            seatMapPanState.initialScale = seatMapPanState.scale;
        }
    }, { passive: false });

    wrapper.addEventListener('touchmove', (e) => {
        if (e.touches.length === 2) {
            e.preventDefault();
            const dx = e.touches[0].clientX - e.touches[1].clientX;
            const dy = e.touches[0].clientY - e.touches[1].clientY;
            const dist = Math.sqrt(dx*dx + dy*dy);
            if (seatMapPanState.initialPinchDistance) {
                const scaleFactor = dist / seatMapPanState.initialPinchDistance;
                seatMapPanState.scale = seatMapPanState.initialScale * scaleFactor;
                
                if (seatMapPanState.scale < 0.4) seatMapPanState.scale = 0.4;
                if (seatMapPanState.scale > 2.5) seatMapPanState.scale = 2.5;
                
                updateSeatMapTransform();
            }
            return;
        }

        if (!seatMapPanState.isDragging || e.touches.length !== 1) return;
        e.preventDefault(); 
        
        let deltaX = e.touches[0].clientX - seatMapPanState.startX;
        let deltaY = e.touches[0].clientY - seatMapPanState.startY;
        
        if (seatMapPanState.is3DHorizontal) {
            seatMapPanState.y = seatMapPanState.logicalStartY + deltaX;
            seatMapPanState.x = seatMapPanState.logicalStartX - deltaY;
        } else {
            seatMapPanState.x = seatMapPanState.logicalStartX + deltaX;
            seatMapPanState.y = seatMapPanState.logicalStartY + deltaY;
        }
        
        if (seatMapPanState.x > 150) seatMapPanState.x = 150;
        if (seatMapPanState.x < -150) seatMapPanState.x = -150;
        if (seatMapPanState.y > 50) seatMapPanState.y = 50;
        if (seatMapPanState.y < -2000) seatMapPanState.y = -2000;
        
        updateSeatMapTransform();
    }, { passive: false });

    wrapper.addEventListener('touchend', () => {
        seatMapPanState.isDragging = false;
        floatingControlTimeout = setTimeout(() => {
            setFloatingControlsVisibility(true);
        }, 400);
    });

    wrapper.addEventListener('mousedown', (e) => {
        clearTimeout(floatingControlTimeout);
        setFloatingControlsVisibility(false);
        seatMapPanState.isDragging = true;
        seatMapPanState.startX = e.clientX;
        seatMapPanState.startY = e.clientY;
        seatMapPanState.logicalStartX = seatMapPanState.x;
        seatMapPanState.logicalStartY = seatMapPanState.y;
        wrapper.style.cursor = 'grabbing';
    });

    window.addEventListener('mousemove', (e) => {
        if (!seatMapPanState.isDragging) return;
        e.preventDefault();
        
        let deltaX = e.clientX - seatMapPanState.startX;
        let deltaY = e.clientY - seatMapPanState.startY;
        
        if (seatMapPanState.is3DHorizontal) {
            seatMapPanState.y = seatMapPanState.logicalStartY + deltaX;
            seatMapPanState.x = seatMapPanState.logicalStartX - deltaY;
        } else {
            seatMapPanState.x = seatMapPanState.logicalStartX + deltaX;
            seatMapPanState.y = seatMapPanState.logicalStartY + deltaY;
        }
        
        if (seatMapPanState.x > 150) seatMapPanState.x = 150;
        if (seatMapPanState.x < -150) seatMapPanState.x = -150;
        if (seatMapPanState.y > 50) seatMapPanState.y = 50;
        if (seatMapPanState.y < -2000) seatMapPanState.y = -2000;
        
        updateSeatMapTransform();
    }, { passive: false });

    window.addEventListener('mouseup', () => {
        seatMapPanState.isDragging = false;
        wrapper.style.cursor = '';
        floatingControlTimeout = setTimeout(() => {
            setFloatingControlsVisibility(true);
        }, 400);
    });

    wrapper.addEventListener('wheel', (e) => {
        e.preventDefault();
        
        clearTimeout(floatingControlTimeout);
        setFloatingControlsVisibility(false);
        
        if (seatMapPanState.is3DHorizontal) {
            seatMapPanState.y -= (Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY);
        } else {
            seatMapPanState.y -= e.deltaY;
        }
        
        floatingControlTimeout = setTimeout(() => {
            setFloatingControlsVisibility(true);
        }, 400);
        if (seatMapPanState.y > 50) seatMapPanState.y = 50;
        if (seatMapPanState.y < -2000) seatMapPanState.y = -2000;
        
        updateSeatMapTransform();
    }, { passive: false });
}

function updateSeatMapTransform() {
    const container = document.getElementById('seatMapTransformContainer');
    const fuselage = document.getElementById('seatMapFuselage');
    if (container && fuselage) {
        if (seatMapPanState.is3DHorizontal) {
            // Always pivot from the nose (center top) to prevent dynamic height from breaking translation offsets
            fuselage.style.transformOrigin = 'center top';
            
            // In horizontal mode, the nose is fixed at X=195, Y=0 within the container.
            // Absolute X = 195 + containerX. We want Absolute X to equal y. So containerX = y - 195.
            const containerX = seatMapPanState.y - 195; 
            
            // Dynamically calculate perfect vertical center based on screen height
            const panArea = document.getElementById('seatMapPanZoomArea');
            const panHeight = panArea ? panArea.clientHeight : 500;
            const containerY = (panHeight / 2) - 20 - seatMapPanState.x;
            
            // Hardware-accelerated 3D transform for container panning
            container.style.transform = `translate3d(${containerX}px, ${containerY}px, 0) scale(${seatMapPanState.scale})`;
        } else {
            // Restore default vertical rendering
            fuselage.style.transformOrigin = 'center top';
            container.style.transform = `translate3d(${seatMapPanState.x}px, ${seatMapPanState.y}px, 0) scale(${seatMapPanState.scale})`;
        }
    }
    
    const wrapper = document.getElementById('seatMapPanZoomArea');
    if (wrapper) {
        let thumb = document.getElementById('customScrollThumb');
        let track = document.getElementById('customScrollTrack');
        if (!track) {
            track = document.createElement('div');
            track.id = 'customScrollTrack';
            thumb = document.createElement('div');
            thumb.id = 'customScrollThumb';
            track.appendChild(thumb);
            wrapper.appendChild(track);
        }
        
        // Logical Y perfectly represents progress along the plane in all modes!
        const logicalY = seatMapPanState.y;
        const progress = (50 - logicalY) / 2050;
        
        if (seatMapPanState.is3DHorizontal) {
            track.style.cssText = 'position: absolute; left: 20px; right: 20px; bottom: 10px; height: 4px; background: rgba(0,0,0,0.05); border-radius: 2px; z-index: 100; pointer-events: none;';
            thumb.style.cssText = 'position: absolute; top: 0; bottom: 0; left: 0; width: 40px; background: rgba(0,0,0,0.3); border-radius: 2px; transition: left 0.1s;';
            thumb.style.top = '';
            thumb.style.left = `calc(${progress * 100}% - ${progress * 40}px)`;
        } else {
            track.style.cssText = 'position: absolute; right: 4px; top: 10px; bottom: 10px; width: 4px; background: rgba(0,0,0,0.05); border-radius: 2px; z-index: 100; pointer-events: none;';
            thumb.style.cssText = 'position: absolute; top: 0; right: 0; width: 4px; height: 40px; background: rgba(0,0,0,0.3); border-radius: 2px; transition: top 0.1s;';
            thumb.style.left = '';
            thumb.style.top = `calc(${progress * 100}% - ${progress * 40}px)`;
        }
    }
}

function zoomSeatMap(delta) {
    seatMapPanState.scale += delta;
    if (seatMapPanState.scale < 0.4) seatMapPanState.scale = 0.4;
    if (seatMapPanState.scale > 2.5) seatMapPanState.scale = 2.5;
    updateSeatMapTransform();
}

function toggleSeatMap3DView() {
    triggerHaptic('medium', 'Toggle 3D View');
    
    const shimmer = document.getElementById('seatMapShimmer');
    if (shimmer) {
        shimmer.style.opacity = '1';
        setTimeout(() => {
            executeToggleSeatMap3DView();
            setTimeout(() => {
                shimmer.style.opacity = '0';
            }, 100);
        }, 200);
    } else {
        executeToggleSeatMap3DView();
    }
}

function executeToggleSeatMap3DView() {
    const fuselage = document.getElementById('seatMapFuselage');
    if (!fuselage) return;

    seatMapPanState.is3DHorizontal = !seatMapPanState.is3DHorizontal;
    
    if (seatMapPanState.is3DHorizontal) {
        fuselage.classList.remove('is-3d-vertical');
        fuselage.classList.add('is-3d-horizontal');
    } else {
        fuselage.classList.remove('is-3d-horizontal');
        fuselage.classList.add('is-3d-vertical');
    }
    
    // Unconditionally reset to the exact top-center position matching the original view
    seatMapPanState.x = 0;
    seatMapPanState.y = 50;
    seatMapPanState.scale = 1;
    
    updateSeatMapTransform();
}

// Hook it into initSeatMapScreen
const oldInitSeatMapScreen = initSeatMapScreen;
initSeatMapScreen = function() {
    oldInitSeatMapScreen();
    initSeatMapPanZoom();
};

// ==========================================================================
// PAYMENTS PAGE LOGIC
// ==========================================================================

function initPaymentsScreen() {
    const baseFare = 6182;
    let seatTotal = 0;
    let seatCount = 0;
    
    // Calculate seat total from seatMapState
    for (const p in seatMapState.assignments) {
        seatTotal += seatMapState.assignments[p].price;
        seatCount++;
    }
    
    // Update Seat Row
    const seatRow = document.getElementById('paymentSeatRow');
    const seatCountEl = document.getElementById('paymentSeatCount');
    const seatTotalEl = document.getElementById('paymentSeatTotal');
    
    if (seatCount > 0) {
        seatRow.style.display = 'flex';
        seatCountEl.innerText = `(${seatCount})`;
        seatTotalEl.innerText = `+₹${seatTotal.toLocaleString('en-IN')}`;
    } else {
        seatRow.style.display = 'none';
    }
    
    let subtotal = baseFare + seatTotal;
    let finalTotal = subtotal;
    let discountApplied = 0;
    
    // Check if cohort discount is active
    if (seatMapState.cohortDiscount) {
        const discountAmount = Math.round(seatTotal * seatMapState.cohortDiscount);
        discountApplied = discountAmount;
        finalTotal -= discountAmount;
        
        const discountRow = document.getElementById('paymentDiscountRow');
        const discountAmountEl = document.getElementById('paymentDiscountAmount');
        const couponCodeEl = document.getElementById('paymentCouponCode');
        const originalTotalEl = document.getElementById('paymentOriginalTotal');
        
        discountRow.style.display = 'block';
        discountAmountEl.innerText = `-₹${discountAmount.toLocaleString('en-IN')}`;
        
        // Determine what to show based on state
        if (seatMapState.paxList.length >= 2) {
             couponCodeEl.innerText = "COHORT Applied";
        } else if (seatMapState.paxList.length === 1 && seatMapState.paxList[0].gender === 'Female') {
             couponCodeEl.innerText = "SOLOWOMAN Applied";
        } else {
             couponCodeEl.innerText = "STUDENT20 Applied";
        }
        
        originalTotalEl.style.display = 'block';
        originalTotalEl.innerText = `₹${subtotal.toLocaleString('en-IN')}`;
    } else {
        document.getElementById('paymentDiscountRow').style.display = 'none';
        document.getElementById('paymentOriginalTotal').style.display = 'none';
    }
    
    // Update Grand Total
    const formattedTotal = `₹${finalTotal.toLocaleString('en-IN')}`;
    document.getElementById('paymentGrandTotal').innerText = formattedTotal;
    document.getElementById('paymentFooterTotal').innerText = formattedTotal;
}

function selectPaymentMethod(element) {
    // Deselect all
    const options = document.querySelectorAll('.payment-option');
    options.forEach(opt => opt.classList.remove('selected'));
    
    // Select clicked
    element.classList.add('selected');
    triggerHaptic('light', 'Payment Method Selected');
}

function processPayment() {
    triggerHaptic('medium', 'Payment Processing');
    const btn = document.querySelector('.payment-fare-card').parentElement.nextElementSibling.querySelector('button');
    const originalText = btn.innerHTML;
    
    btn.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin" style="animation: spin 1s linear infinite;"><path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"></path></svg> Processing...`;
    
    // Add simple spin animation to doc if not exists
    if (!document.getElementById('spinStyle')) {
        const style = document.createElement('style');
        style.id = 'spinStyle';
        style.innerHTML = `@keyframes spin { 100% { transform: rotate(360deg); } }`;
        document.head.appendChild(style);
    }
    
    setTimeout(() => {
        triggerHaptic('success', 'Payment Success');
        btn.style.background = '#10b981';
        btn.innerHTML = `<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg> Payment Successful`;
        
        setTimeout(() => {
            showToast('Booking Confirmed! ✈️');
            setTimeout(() => {
                // reset and go home
                btn.style.background = '#000';
                btn.innerHTML = originalText;
                navigateTo('home');
            }, 1500);
        }, 500);
    }, 2000);
}

// ==========================================================================
// LOYALTY 3D DOOR ANIMATION (CRED STYLE)
// ==========================================================================

function toggleLoyaltyMenu(wrapperElement) {
    if (wrapperElement) {
        if (wrapperElement.classList.contains('menu-open')) {
            wrapperElement.classList.remove('menu-open');
            triggerHaptic('light', 'Card Menu Closed');
        } else {
            wrapperElement.classList.add('menu-open');
            triggerHaptic('medium', 'Card Menu Opened');
        }
    }
}

// Swipe detection for Loyalty Cards
document.addEventListener('DOMContentLoaded', () => {
    const wrappers = document.querySelectorAll('.loyalty-3d-wrapper');
    wrappers.forEach(wrapper => {
        let startX = 0;
        let startY = 0;
        
        wrapper.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        }, {passive: true});
        
        wrapper.addEventListener('touchend', (e) => {
            if (!startX || !startY) return;
            const endX = e.changedTouches[0].clientX;
            const endY = e.changedTouches[0].clientY;
            
            const diffX = startX - endX;
            const diffY = startY - endY;
            
            if (Math.abs(diffX) > Math.abs(diffY)) {
                if (diffX > 40) { // Swipe left
                    if (!wrapper.classList.contains('menu-open')) {
                        toggleLoyaltyMenu(wrapper);
                    }
                } else if (diffX < -40) { // Swipe right
                    if (wrapper.classList.contains('menu-open')) {
                        toggleLoyaltyMenu(wrapper);
                    }
                }
            }
            
            startX = 0;
            startY = 0;
        });
    });
});

// --- Zoom Controls ---
function handleZoomIn() {
    if (typeof seatMapPanState !== 'undefined') {
        seatMapPanState.scale += 0.1;
        if (seatMapPanState.scale > 2.5) seatMapPanState.scale = 2.5;
        if (typeof updateSeatMapTransform === 'function') {
            updateSeatMapTransform();
        }
        if (typeof triggerHaptic === 'function') {
            triggerHaptic('light', 'Zoom In');
        }
    }
}

function handleZoomOut() {
    if (typeof seatMapPanState !== 'undefined') {
        seatMapPanState.scale -= 0.1;
        if (seatMapPanState.scale < 0.4) seatMapPanState.scale = 0.4;
        if (typeof updateSeatMapTransform === 'function') {
            updateSeatMapTransform();
        }
        if (typeof triggerHaptic === 'function') {
            triggerHaptic('light', 'Zoom Out');
        }
    }
}

// ==========================================
// BAGGAGE TRACKING SCREEN LOGIC
// ==========================================

function openBaggageTracking() {
    triggerHaptic('light', 'Open Baggage Tracking');
    document.getElementById('screenBaggageTracking').classList.add('active');
}

function closeBaggageTracking() {
    triggerHaptic('light', 'Close Baggage Tracking');
    document.getElementById('screenBaggageTracking').classList.remove('active');
}


// ==========================================================================
// INTERACTIVE MAP CONTROLLER (Pan, Zoom, Search)
// ==========================================================================

const mapCities = [
    { name: "London", country: "UK", x: 450, y: 150 },
    { name: "Paris", country: "France", x: 460, y: 165 },
    { name: "New York", country: "USA", x: 260, y: 190 },
    { name: "Tokyo", country: "Japan", x: 820, y: 200 },
    { name: "Dubai", country: "UAE", x: 570, y: 240 },
    { name: "Mumbai", country: "India", x: 650, y: 260 },
    { name: "Delhi", country: "India", x: 655, y: 235 },
    { name: "Singapore", country: "Singapore", x: 730, y: 340 },
    { name: "Sydney", country: "Australia", x: 850, y: 480 },
    { name: "Cape Town", country: "South Africa", x: 500, y: 470 },
    { name: "Rio de Janeiro", country: "Brazil", x: 330, y: 420 },
    { name: "Los Angeles", country: "USA", x: 140, y: 210 }
];

let mapScale = 1;
let mapTx = 0;
let mapTy = 0;
let isPanning = false;
let startPanX = 0;
let startPanY = 0;
let initialDist = 0;
let touchMode = 'none'; // none, scroll, pan, zoom

function initMapInteractions() {
    const wrapper = document.getElementById('mapWrapper');
    const transformLayer = document.getElementById('mapTransformLayer');
    const warning = document.getElementById('mapScrollWarning');
    if (!wrapper || !transformLayer) return;

    // Center map initially (assuming 950x620 SVG in a ~360x220 container)
    // We want to scale it down to fit or start zoomed into a specific area (e.g. Europe/Asia)
    mapScale = 0.6;
    mapTx = -100;
    mapTy = -50;
    updateMapTransform(false);

    wrapper.addEventListener('touchstart', (e) => {
        if (e.touches.length === 1) {
            touchMode = 'scroll';
            // Allow vertical scroll, but warn user if they try to drag horizontally
            startPanX = e.touches[0].clientX;
            startPanY = e.touches[0].clientY;
        } else if (e.touches.length === 2) {
            e.preventDefault();
            touchMode = 'zoom';
            isPanning = true;
            initialDist = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
            startPanX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
            startPanY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
            warning.style.opacity = '0';
        }
    }, { passive: false });

    wrapper.addEventListener('touchmove', (e) => {
        if (touchMode === 'scroll') {
            const dx = Math.abs(e.touches[0].clientX - startPanX);
            const dy = Math.abs(e.touches[0].clientY - startPanY);
            if (dx > 10 && dy < 30) {
                // User is trying to pan horizontally with one finger
                warning.style.opacity = '1';
                e.preventDefault();
            } else {
                warning.style.opacity = '0';
            }
        } else if (touchMode === 'zoom' && e.touches.length === 2) {
            e.preventDefault();
            
            // Handle Zoom
            const newDist = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
            const scaleChange = newDist / initialDist;
            let newScale = mapScale * scaleChange;
            newScale = Math.max(0.3, Math.min(newScale, 3)); // clamp scale
            
            // Handle Pan
            const currentX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
            const currentY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
            
            mapTx += (currentX - startPanX);
            mapTy += (currentY - startPanY);
            
            mapScale = newScale;
            initialDist = newDist;
            startPanX = currentX;
            startPanY = currentY;
            
            updateMapTransform(false);
        }
    }, { passive: false });

    wrapper.addEventListener('touchend', (e) => {
        if (e.touches.length < 2) {
            isPanning = false;
            touchMode = 'none';
        }
        warning.style.opacity = '0';
    });
    
    // Mouse fallback for desktop testing
    wrapper.addEventListener('mousedown', (e) => {
        isPanning = true;
        startPanX = e.clientX;
        startPanY = e.clientY;
        transformLayer.style.transition = 'none';
    });
    window.addEventListener('mousemove', (e) => {
        if (!isPanning) return;
        mapTx += (e.clientX - startPanX);
        mapTy += (e.clientY - startPanY);
        startPanX = e.clientX;
        startPanY = e.clientY;
        updateMapTransform(false);
    });
    window.addEventListener('mouseup', () => {
        isPanning = false;
        transformLayer.style.transition = 'transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1)';
    });
}

function updateMapTransform(animate = true) {
    const layer = document.getElementById('mapTransformLayer');
    if (layer) {
        if (animate) layer.style.transition = 'transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1)';
        else layer.style.transition = 'none';
        layer.style.transform = `translate(${mapTx}px, ${mapTy}px) scale(${mapScale})`;
    }
}

window.handleMapSearch = function(query) {
    const resultsDiv = document.getElementById('mapSearchResults');
    if (!query || query.length < 2) {
        resultsDiv.style.display = 'none';
        return;
    }
    
    const q = query.toLowerCase();
    const matches = mapCities.filter(c => c.name.toLowerCase().includes(q) || c.country.toLowerCase().includes(q));
    
    if (matches.length > 0) {
        resultsDiv.style.display = 'block';
        resultsDiv.innerHTML = matches.map(c => `
            <div style="padding: 12px 16px; border-bottom: 1px solid #f1f5f9; display: flex; align-items: center; gap: 12px; cursor: pointer;" onclick="zoomToMapCity('${c.name}')">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#0f172a" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                <div>
                    <div style="font-weight: 700; font-size: 14px; color: #0f172a;">${c.name}</div>
                    <div style="font-weight: 600; font-size: 11px; color: #64748b;">${c.country}</div>
                </div>
            </div>
        `).join('');
    } else {
        resultsDiv.style.display = 'none';
    }
}

window.zoomToMapCity = function(cityName) {
    const city = mapCities.find(c => c.name === cityName);
    if (!city) return;
    
    document.getElementById('mapSearchInput').value = cityName;
    document.getElementById('mapSearchResults').style.display = 'none';
    
    // Zoom in logic
    mapScale = 1.8;
    
    // Viewport dimensions (roughly 360x220 for mobile embedded view)
    const vw = document.getElementById('mapWrapper').offsetWidth || 360;
    const vh = document.getElementById('mapWrapper').offsetHeight || 220;
    
    // Center the targeted X,Y coordinates
    mapTx = (vw / 2) - (city.x * mapScale);
    mapTy = (vh / 2) - (city.y * mapScale);
    
    updateMapTransform(true);
    triggerHaptic('heavy', `Zoomed to ${cityName}`);
    
    // Drop Pin
    const pinsLayer = document.getElementById('mapPinsLayer');
    if (pinsLayer) {
        pinsLayer.innerHTML = `
            <div style="position: absolute; left: ${city.x}px; top: ${city.y}px; transform: translate(-50%, -100%); width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; animation: dropPin 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;">
                <svg viewBox="0 0 24 24" width="32" height="32" fill="#e84b38" stroke="#fff" stroke-width="1.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3" fill="#fff"></circle></svg>
            </div>
        `;
    }
}

// Add dropPin animation to document
const style = document.createElement('style');
style.textContent = `
    @keyframes dropPin {
        0% { transform: translate(-50%, -150%) scale(0); opacity: 0; }
        100% { transform: translate(-50%, -100%) scale(1); opacity: 1; }
    }
`;
document.head.appendChild(style);

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(initMapInteractions, 500);
});


// ==========================================================================
// UPFRONT UNLOCK FLOW (Option B)
// ==========================================================================
window.appState = window.appState || {};

function unlockUpfrontPerks(btn) {
    // 1. Show Toast
    if(typeof showToast === 'function') {
        showToast('🎉 Upgraded to X Airline Upfront!');
    }
    
    // 2. Button State Change
    if (btn) {
        btn.innerHTML = 'Upgraded <span style="font-size: 14px; margin-left: 4px;">✅</span>';
        btn.style.background = '#e0f2fe';
        btn.style.color = '#0284c7';
        btn.onclick = null;
    }
    
    // 3. Inject "Claim your Perks" section right below PNR card
    const pnrCard = document.querySelector('.pnr-main-card');
    if (!pnrCard) return;
    
    // Remove if already exists
    const existing = document.getElementById('upfrontPerksSection');
    if (existing) existing.remove();
    
    const perksHtml = `
        <div id="upfrontPerksSection" style="margin-top: 16px; margin-bottom: 24px; animation: slideDown 0.4s ease-out forwards; padding: 0 16px;">
            <div style="font-size: 13px; font-weight: 800; color: #001B94; margin-bottom: 12px; letter-spacing: 0.5px; text-transform: uppercase; display: flex; align-items: center; gap: 6px;">
                <div style="width: 8px; height: 8px; background: #3b82f6; border-radius: 50%; box-shadow: 0 0 0 3px rgba(59,130,246,0.2); animation: pulseDot 2s infinite;"></div>
                Action Required: Claim Perks
            </div>
            
            <div style="display: flex; gap: 12px; overflow-x: auto; scrollbar-width: none; padding-bottom: 8px; margin-left: -16px; padding-left: 16px; padding-right: 16px;">
                <!-- Meal Card -->
                <div onclick="navigateToAddonsAndMakeFree('meals')" style="flex: 0 0 160px; background: #fff; border-radius: 16px; padding: 14px; border: 2px solid #3b82f6; box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15); cursor: pointer; position: relative; overflow: hidden; transition: transform 0.2s;">
                    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, #3b82f6, #0ea5e9);"></div>
                    <div style="font-size: 28px; margin-bottom: 12px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));">🍲</div>
                    <div style="font-size: 15px; font-weight: 800; color: #0f172a;">Free Meal</div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 4px; line-height: 1.4;">Claim your included Upfront meal</div>
                    <div style="margin-top: 16px; font-size: 12px; font-weight: 800; color: #3b82f6; display: flex; align-items: center; justify-content: space-between;">
                        Select Now <span>➔</span>
                    </div>
                </div>

                <!-- Seat Card -->
                <div onclick="navigateToSeatmapAndMakeFree()" style="flex: 0 0 160px; background: #fff; border-radius: 16px; padding: 14px; border: 2px solid #3b82f6; box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15); cursor: pointer; position: relative; overflow: hidden; transition: transform 0.2s;">
                    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, #3b82f6, #0ea5e9);"></div>
                    <div style="font-size: 28px; margin-bottom: 12px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));">💺</div>
                    <div style="font-size: 15px; font-weight: 800; color: #0f172a;">Free Seat</div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 4px; line-height: 1.4;">Pick any premium seat for free</div>
                    <div style="margin-top: 16px; font-size: 12px; font-weight: 800; color: #3b82f6; display: flex; align-items: center; justify-content: space-between;">
                        Select Now <span>➔</span>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    pnrCard.insertAdjacentHTML('afterend', perksHtml);
    window.appState.upfrontUnlocked = true;
}

function navigateToAddonsAndMakeFree(section) {
    if(typeof triggerHaptic === 'function') triggerHaptic('medium', 'Addons');
    if(typeof navigateTo === 'function') navigateTo('addons');
    
    setTimeout(() => {
        // Scroll to meals section
        if(section === 'meals') {
            const mealSection = document.getElementById('section-meals');
            if(mealSection) mealSection.scrollIntoView({behavior: 'smooth', block: 'start'});
        }
        
        // Make meals free visually
        const mealPrices = document.querySelectorAll('#section-meals .glass-price');
        mealPrices.forEach(price => {
            if(!price.innerText.includes('FREE')) {
                price.innerHTML = '<span style="text-decoration: line-through; opacity: 0.5; font-size: 10px; margin-right: 4px;">' + price.innerText + '</span> <span style="color: #10b981; font-weight: 900;">FREE</span>';
            }
        });
        const mealAddBtns = document.querySelectorAll('#section-meals .glass-add-btn');
        mealAddBtns.forEach(btn => {
            if(btn.innerText === '+ Add') {
                btn.style.background = '#d1fae5';
                btn.style.color = '#059669';
                btn.style.border = '1px solid #10b981';
            }
        });
        
        // Add a top banner inside Addons
        const addonsHeader = document.querySelector('#screenAddons .companion-header-inner');
        if (addonsHeader && !document.getElementById('addonsUpfrontBanner')) {
            addonsHeader.insertAdjacentHTML('afterend', `
                <div id="addonsUpfrontBanner" style="background: linear-gradient(90deg, #1e3a8a, #3b82f6); color: #fff; padding: 12px 24px; font-size: 13px; font-weight: 700; display: flex; align-items: center; gap: 8px;">
                    <span>✨</span> You are browsing with Upfront. Meals are free!
                </div>
            `);
        }
        
    }, 400);
}

function navigateToSeatmapAndMakeFree() {
    if(typeof triggerHaptic === 'function') triggerHaptic('medium', 'Addons');
    if(typeof navigateTo === 'function') navigateTo('addons');
}

function renderCompanionState() {
    const recent = document.getElementById('recentSearchesSection');
    if(recent) recent.style.display = 'none';
    const cab = document.getElementById('companionCabDeals');
    if(cab) cab.style.display = 'block';
    
    const loyalty = document.getElementById('loyaltySection');
    if(loyalty) loyalty.style.display = 'none';
    const hotel = document.getElementById('companionHotelDeals');
    if(hotel) hotel.style.display = 'block';
}

// --- Personalized Booking Toggle ---
let isPersonalizedBooking = false;
window.togglePersonalizedBooking = function() {
    isPersonalizedBooking = !isPersonalizedBooking;
    const btn = document.getElementById('btnTogglePersonalized');
    const passCardHJR = document.getElementById('passCardHJR');
    const passCardPersonalized = document.getElementById('passCardPersonalized');
    
    if (isPersonalizedBooking) {
        if (btn) btn.classList.add('active');
        if (passCardHJR) passCardHJR.style.display = 'none';
        if (passCardPersonalized) passCardPersonalized.style.display = 'block';
        triggerHaptic('success', 'Personalized Booking Activated'); expandBoardingPass('Personalized');
    } else {
        if (btn) btn.classList.remove('active');
        if (passCardHJR) passCardHJR.style.display = 'block';
        if (passCardPersonalized) passCardPersonalized.style.display = 'none';
        triggerHaptic('light', 'Personalized Booking Deactivated');
    }
};

// Add Personalized Data for Calendar
if (typeof travelOnTapData !== 'undefined') {
    travelOnTapData['Personalized'] = {
        name: 'Mumbai',
        fares: [
            { date: '23 Apr', price: 5499, lowest: false },
            { date: '24 Apr', price: 4999, lowest: true },
            { date: '25 Apr', price: 5299, lowest: false },
            { date: '26 Apr', price: 6199, lowest: false }
        ]
    };
}


// ==========================================================================
// TIMELINE BOARDING PASS LOGIC
// ==========================================================================

window.flipToLeg = function(legNum) {
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
}

window.openQRModal = function() {
    if(document.getElementById('bpQrFullscreen')) document.getElementById('bpQrFullscreen').style.display = 'flex';
    triggerHaptic('medium', 'QR Modal Opened');
}

window.closeQRModal = function() {
    if(document.getElementById('bpQrFullscreen')) document.getElementById('bpQrFullscreen').style.display = 'none';
}

// Override the demo state toggles to handle the new timeline structure
window.setBPState = function(state) {
    document.getElementById('btnBPSingle').classList.remove('active');
    document.getElementById('btnBPMulti').classList.remove('active');
    document.getElementById('btnBPDone').classList.remove('active');
    
    const toggles = document.querySelectorAll('.bp-leg-toggle');
    const slider = document.getElementById('bpTimelineSlider');
    
    if (state === 'single') {
        document.getElementById('btnBPSingle').classList.add('active');
        toggles.forEach(t => t.style.display = 'none');
        
        flipToLeg(1);
    } else if (state === 'multi') {
        document.getElementById('btnBPMulti').classList.add('active');
        toggles.forEach(t => t.style.display = 'flex');
        
        flipToLeg(1);
    } else if (state === 'completed') {
        document.getElementById('btnBPDone').classList.add('active');
        toggles.forEach(t => t.style.display = 'flex');
        
        flipToLeg(2);
    }
}


// ==========================================================================
// TIMELINE LOGIC
// ==========================================================================

function toggleTimelineDrawer() {
    const drawer = document.getElementById('companionTimelineDrawer');
    const btn = document.getElementById('timelineToggleBtn');
    if (!drawer || !btn) return;
    
    if (drawer.style.height === '0px' || drawer.style.height === '') {
        const content = document.getElementById('verticalTimelineContent');
        drawer.style.height = content.offsetHeight + 'px';
        btn.classList.add('open');
        triggerHaptic('light', 'Timeline Expand');
    } else {
        drawer.style.height = '0px';
        btn.classList.remove('open');
        triggerHaptic('light', 'Timeline Collapse');
    }
}

function updateTimelineState(state) {
    const header = document.getElementById('companionTimelineHeader');
    const drawer = document.getElementById('companionTimelineDrawer');
    
    if (state === 'upcoming_trip') {
        if (header) header.style.display = 'none';
        if (drawer) drawer.style.display = 'none';
        return;
    } else {
        if (header) header.style.display = 'flex';
        if (drawer) drawer.style.display = 'block';
    }

    // 5 Milestones: 
    // 1. Check-in (checkin_open, checked_in)
    // 2. Airport (airport_checkin, go_to_counter)
    // 3. Gate (gate_open, gate_update)
    // 4. Boarding (delayed could map here, or gate)
    // 5. Departed (cancelled could map to an error state)
    
    let activeNodeIndex = 1; // 1 to 5
    
    if (['checkin_open'].includes(state)) activeNodeIndex = 1;
    else if (['checked_in', 'airport_checkin', 'go_to_counter'].includes(state)) activeNodeIndex = 2;
    else if (['gate_open', 'gate_update'].includes(state)) activeNodeIndex = 3;
    else if (['delayed', 'baggage_tracking'].includes(state)) activeNodeIndex = 4;
    else if (['cancelled'].includes(state)) activeNodeIndex = 1; // reset or handle specially
    
    // Update horizontal nodes
    for (let i = 1; i <= 5; i++) {
        const node = document.getElementById('tlNode' + i);
        if (!node) continue;
        
        node.className = 'timeline-node'; // reset
        if (i < activeNodeIndex) {
            node.classList.add('completed');
        } else if (i === activeNodeIndex) {
            node.classList.add('active');
        }
    }
    
    // Update progress bar width
    const progress = document.getElementById('timelineProgress');
    if (progress) {
        // 5 nodes means 4 segments. 
        // Index 1 = 0%, Index 2 = 25%, Index 3 = 50%, Index 4 = 75%, Index 5 = 100%
        const percentage = ((activeNodeIndex - 1) / 4) * 100;
        progress.style.width = percentage + '%';
    }
    
    // Render vertical timeline content
    renderVerticalTimeline(activeNodeIndex, state);
    
    // Auto-adjust drawer height if it's currently open
    const drawer = document.getElementById('companionTimelineDrawer');
    if (drawer && drawer.style.height !== '0px' && drawer.style.height !== '') {
        setTimeout(() => {
            const content = document.getElementById('verticalTimelineContent');
            drawer.style.height = content.offsetHeight + 'px';
        }, 50);
    }
}

function renderVerticalTimeline(activeIndex, state) {
    const container = document.getElementById('verticalTimelineContent');
    if (!container) return;
    
    // Base data
    const milestones = [
        { time: '12:30', title: 'Check-in Opened', sub: '24 April' },
        { time: '14:00', title: 'Airport Arrival', sub: 'Bag drop counter 45' },
        { time: '15:15', title: 'Gate Open', sub: 'Gate 5B, Terminal 2' },
        { time: '16:00', title: 'Boarding', sub: 'Zones 1-3' },
        { time: '16:45', title: 'Departure', sub: 'On time' }
    ];
    
    // Modify labels based on specific states
    if (state === 'delayed') {
        milestones[3].sub = 'Estimated 17:30';
        milestones[4].sub = 'Delayed';
        milestones[4].time = '18:15';
    } else if (state === 'gate_update') {
        milestones[2].sub = 'Gate changed to 12C';
    }
    
    let html = '';
    milestones.forEach((m, i) => {
        let nodeClass = 'vertical-node';
        if (i < activeIndex - 1) nodeClass += ' completed';
        else if (i === activeIndex - 1) nodeClass += ' active';
        
        html += `
            <div class="${nodeClass}">
                <div class="time-label">${m.time}</div>
                <div class="v-node-icon"></div>
                <div class="event-label">
                    <div class="event-label-title">${m.title}</div>
                    <div class="event-label-sub">${m.sub}</div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}
