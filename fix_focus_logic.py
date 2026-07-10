import re

# 1. Update style.css to stop hiding the search button
with open('style.css', 'r') as f:
    css = f.read()

# Replace the block that hides the search btn
old_css_rule = """.search-widget-panel.nlp-focused-mode .route-row,
.search-widget-panel.nlp-focused-mode .search-details-row,
.search-widget-panel.nlp-focused-mode .search-btn-container {
    display: none;
}"""

new_css_rule = """.search-widget-panel.nlp-focused-mode .route-row,
.search-widget-panel.nlp-focused-mode .search-details-row {
    display: none;
}"""

css = css.replace(old_css_rule, new_css_rule)

with open('style.css', 'w') as f:
    f.write(css)


# 2. Update app.js to hide customPlaceholder on focus
with open('app.js', 'r') as f:
    js = f.read()

# Remove the old input listener
input_listener_regex = r'// Hide custom placeholder when typing.*?\}\);\s*\}\s*\}\);'
js = re.sub(input_listener_regex, '}\n});', js, flags=re.DOTALL)

# Update focus listener
old_focus_js = """    // NLP Focused Mode Logic
    if (input) {
        input.addEventListener('focus', () => {
            document.getElementById('searchWidgetSection').classList.add('nlp-focused-mode');
            const backIcon = document.getElementById('nlpBackIcon');
            if (backIcon) backIcon.style.display = 'flex';
            if (customPlaceholder) {
                // Adjust placeholder position slightly since back icon appears
                customPlaceholder.style.left = '56px';
            }
        });
    }"""

new_focus_js = """    // NLP Focused Mode Logic
    if (input) {
        input.addEventListener('focus', () => {
            document.getElementById('searchWidgetSection').classList.add('nlp-focused-mode');
            const backIcon = document.getElementById('nlpBackIcon');
            if (backIcon) backIcon.style.display = 'flex';
            if (customPlaceholder) {
                customPlaceholder.style.display = 'none';
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
    }"""

js = js.replace(old_focus_js, new_focus_js)

# Update exitNlpMode to restore customPlaceholder
old_exit = """        if (customPlaceholder) customPlaceholder.style.left = '16px';"""
new_exit = """        if (customPlaceholder) {
            customPlaceholder.style.display = 'flex';
            customPlaceholder.style.left = '16px';
        }"""
js = js.replace(old_exit, new_exit)

with open('app.js', 'w') as f:
    f.write(js)

print("Updates applied successfully!")
