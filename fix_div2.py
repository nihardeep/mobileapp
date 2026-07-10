with open('index.html', 'r') as f:
    text = f.read()

marker = """                            </div>

                        </div>

<div class="recent-searches-section" id="recentSearchesSection">"""
if marker in text:
    text = text.replace(marker, "</div>\n" + marker)
    with open('index.html', 'w') as f:
        f.write(text)
    print("Fixed div balance 2!")
else:
    print("Marker not found")
