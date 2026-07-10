with open('index.html', 'r') as f:
    text = f.read()

# I will just insert a </div> before "</div>\n\n                            </div>\n\n                        </div>"
# Let's find exactly the spot.
marker = """                            </div>

                        </div>

<div class="recent-searches-section" id="recentSearchesSection">"""
if marker in text:
    text = text.replace(marker, "</div>\n" + marker)
    with open('index.html', 'w') as f:
        f.write(text)
    print("Fixed div balance!")
else:
    print("Marker not found")
