/* PLAY & WIN GAME LOGIC */
/* ========================================== */
const GAME_TARGET_WORDS = ['FLY', 'PLANE', '6ESKY', 'INDIGO'];
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
    document.getElementById('screenGame').style.display = 'block';
    // Add active class for smooth entry if needed
    document.getElementById('screenGame').classList.add('active');
    
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
