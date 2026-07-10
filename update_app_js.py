with open('app.js', 'r') as f:
    js = f.read()

# 1. Update triggerHomepageCompanion to hide searchWidgetSection
target1 = """    // Collapse search widget if it's not already
    if (!expanded.classList.contains('collapsed')) {
        expanded.classList.add('collapsed');
        toggleBtn.classList.add('collapsed');
    }
    // Show toggle button so user can expand it back
    toggleBtn.style.display = 'flex';"""

replacement1 = """    // Hide the search widget entirely when trip companion is loaded
    const searchWidget = document.getElementById('searchWidgetSection');
    if (searchWidget) searchWidget.style.display = 'none';"""

js = js.replace(target1, replacement1)

# 2. Update navigateTo to also reset the companion if navigating to home, 
# but we have the early return: `if (appState.currentScreen === screenName) return;`
# So we must intercept 'home' even if we're already on it, to clear the companion.

target2 = """function navigateTo(screenName) {
    if (appState.currentScreen === screenName) return;"""

replacement2 = """function navigateTo(screenName) {
    // If navigating to home, ALWAYS reset the companion state even if already on home
    if (screenName === 'home') {
        const searchWidget = document.getElementById('searchWidgetSection');
        if (searchWidget) searchWidget.style.display = 'block';
        
        const wrapper = document.getElementById('homeFlightStateWrapper');
        if (wrapper) wrapper.style.display = 'none';
        
        // Remove active state from dev trip button
        const devTrips = document.getElementById('devNavTrips');
        if (devTrips) devTrips.classList.remove('active');
        
        // Activate dev home button
        const devHome = document.querySelector('.dev-btn-stack button[onclick="navigateTo(\\'home\\')"]');
        if (devHome) devHome.classList.add('active');
    }

    if (appState.currentScreen === screenName) return;"""

js = js.replace(target2, replacement2)

with open('app.js', 'w') as f:
    f.write(js)
