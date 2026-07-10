with open('index.html', 'r') as f:
    html = f.read()

# I will replace exactly the sequence of 4 closing divs that are incorrectly stacked
bad_sequence = """                                        </div>
                                    </div>
                                    </div>"""

good_sequence = """                                        </div>
                                    </div>"""

html = html.replace(bad_sequence, good_sequence)

# Let's check how many were replaced
print("Replaced instances:", html.count(good_sequence) - html.count(bad_sequence))

with open('index.html', 'w') as f:
    f.write(html)
