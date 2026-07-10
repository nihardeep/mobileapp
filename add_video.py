with open('index.html', 'r') as f:
    html = f.read()

# Replace <div class="ai-dest-hero-img" id="aiDestHeroImg"></div>
# With a container that holds the video
new_hero = """<div class="ai-dest-hero-img" id="aiDestHeroImg">
                                <video id="aiDestHeroVideo" loop muted playsinline></video>
                            </div>"""

html = html.replace('<div class="ai-dest-hero-img" id="aiDestHeroImg"></div>', new_hero)

with open('index.html', 'w') as f:
    f.write(html)
print("Added video element")
