with open('index.html', 'r') as f:
    html = f.read()

bad_sequence = """                                        </div>
                                    </div>
                                    </div>"""

good_sequence = """                                        </div>
                                    </div>"""

html = html.replace(good_sequence, bad_sequence)

with open('index.html', 'w') as f:
    f.write(html)
