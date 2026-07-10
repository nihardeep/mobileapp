import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update the Mic Icon size
old_mic = """<div class="nlp-mic-icon" onclick="startVoiceSearch(event)" style="background: #fff; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 0 2px rgba(0,95,169,0.2), 0 0 0 6px rgba(0,95,169,0.05); color: var(--indigo-blue); cursor: pointer; transition: all 0.3s ease;">
                <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" fill="none" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">"""

new_mic = """<div class="nlp-mic-icon" onclick="startVoiceSearch(event)" style="background: #fff; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 0 1px rgba(0,95,169,0.2), 0 0 0 3px rgba(0,95,169,0.05); color: var(--indigo-blue); cursor: pointer; transition: all 0.3s ease;">
                <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" fill="none" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">"""

html = html.replace(old_mic, new_mic)

with open('index.html', 'w') as f:
    f.write(html)

# 2. Append the animation logic to app.js
animation_js = """
// Placeholder animation for NLP input
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('nlpSearchInput');
    if (input) {
        const phrases = [
            "'Flights to Goa'",
            "'Trip to Delhi'",
            "'Coorg Homestays'",
            "'Beach destinations'"
        ];
        let currentIndex = 0;
        
        setInterval(() => {
            input.style.transition = 'opacity 0.3s ease';
            input.style.opacity = 0;
            
            setTimeout(() => {
                currentIndex = (currentIndex + 1) % phrases.length;
                input.setAttribute('placeholder', `Ask 6eSkai about ${phrases[currentIndex]}`);
                input.style.opacity = 1;
            }, 300);
        }, 3000); // Change every 3 seconds
    }
});
"""

with open('app.js', 'a') as f:
    f.write(animation_js)

print("Updated mic icon size and added placeholder animation!")
