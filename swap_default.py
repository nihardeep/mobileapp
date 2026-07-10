import re

with open('index.html', 'r') as f:
    html = f.read()

# Make tabNLP active, tabManual inactive
html = html.replace('<div class="search-mode-tab active" id="tabManual"', '<div class="search-mode-tab" id="tabManual"')
html = html.replace('<div class="search-mode-tab" id="tabNLP"', '<div class="search-mode-tab active" id="tabNLP"')

# Make manualSearchView hidden, nlpSearchView visible
html = html.replace('<div id="manualSearchView" class="search-view-container active-view">', '<div id="manualSearchView" class="search-view-container active-view" style="display: none;">')
html = html.replace('<div id="nlpSearchView" class="search-view-container" style="display: none;">', '<div id="nlpSearchView" class="search-view-container" style="display: block;">')

with open('index.html', 'w') as f:
    f.write(html)
print("Swapped defaults!")
