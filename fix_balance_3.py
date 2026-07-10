with open('index.html', 'r') as f:
    html = f.read()

target = '                                            </div>\n                                        </div>\n                                    </div>\n'
replacement = '                                            </div>\n                                        </div>\n                                    </div>\n                                </div>\n'
html = html.replace(target, replacement, 1)

with open('index.html', 'w') as f:
    f.write(html)
