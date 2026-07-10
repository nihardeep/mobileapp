with open('index.html', 'r') as f:
    html = f.read()
start = html.find('<div class="bluchip-card" id="loyalUserCard"')
end = html.find('<!-- STATE 2: NEW USER (Zero Balance) -->')
print(html[start:end])
