import re

with open('app.js', 'r') as f:
    js = f.read()

old_code = """    // Scroll to search widget and flash search button to guide user
    const searchWidget = document.getElementById('searchWidgetSection');
    if (searchWidget) {
        searchWidget.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Visual flash effect on search button
        const searchBtn = document.getElementById('searchFlightsBtn');
        if (searchBtn) {
            setTimeout(() => {
                searchBtn.style.boxShadow = '0 0 20px #001b94';
                searchBtn.style.transform = 'scale(1.04)';
                setTimeout(() => {
                    searchBtn.style.boxShadow = '';
                    searchBtn.style.transform = '';
                }, 400);
            }, 600);
        }
    }"""

js = js.replace(old_code, "")

with open('app.js', 'w') as f:
    f.write(js)
