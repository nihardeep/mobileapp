import re

with open('app.js', 'r') as f:
    js = f.read()

# Fix 1: input event listener should only show prompts if in focused mode
old_input_listener = """        input.addEventListener('input', (e) => {
            const val = e.target.value.toLowerCase();
            const trendingSection = document.getElementById('trendingPromptsSection');
            const autoSection = document.getElementById('autoSuggestionsSection');
            
            if (val.length === 0) {
                // If empty, show trending, hide auto
                if (trendingSection) trendingSection.style.display = 'block';
                if (autoSection) autoSection.style.display = 'none';
            } else if (val.includes('help me')) {"""

new_input_listener = """        input.addEventListener('input', (e) => {
            const val = e.target.value.toLowerCase();
            const trendingSection = document.getElementById('trendingPromptsSection');
            const autoSection = document.getElementById('autoSuggestionsSection');
            const isFocused = document.getElementById('searchWidgetSection').classList.contains('nlp-focused-mode');
            
            if (!isFocused) return; // Do not show anything if not in focused mode
            
            if (val.length === 0) {
                // If empty, show trending, hide auto
                if (trendingSection) trendingSection.style.display = 'block';
                if (autoSection) autoSection.style.display = 'none';
            } else if (val.includes('help me')) {"""

js = js.replace(old_input_listener, new_input_listener)


# Fix 2: simulateIntent failing on manualSearchForm
old_simulate = """            // Open manual form to show the results of AI parsing
            const form = document.getElementById('manualSearchForm');
            form.style.display = 'block';
            
            // Auto search after a short delay
            setTimeout(() => {
                searchFlights();
            }, 800);"""

new_simulate = """            // Open manual form to show the results of AI parsing
            if (window.exitNlpMode) {
                window.exitNlpMode();
            }
            
            // Auto search after a short delay
            setTimeout(() => {
                if (window.searchFlights) searchFlights();
            }, 800);"""

js = js.replace(old_simulate, new_simulate)

# And fix querySelector('.nlp-placeholder') if it was failing because we are dealing with ID nlpSearchInput
old_input_query = """const input = document.querySelector('.nlp-placeholder');"""
new_input_query = """const input = document.getElementById('nlpSearchInput');"""
js = js.replace(old_input_query, new_input_query)


with open('app.js', 'w') as f:
    f.write(js)

print("Fixed app.js bugs!")
