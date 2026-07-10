import re

with open('app.js', 'r') as f:
    js = f.read()

# Remove the old animation block
old_anim_regex = r'// Placeholder animation for NLP input.*?// Change every 3 seconds\n    }\n}\);\n'
js = re.sub(old_anim_regex, '', js, flags=re.DOTALL)

# Add the new animation block targeting the specific span, and add input listener
new_anim_js = """
// Custom placeholder animation for NLP input
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('nlpSearchInput');
    const animatedText = document.getElementById('nlpAnimatedText');
    const customPlaceholder = document.getElementById('customNlpPlaceholder');
    
    if (input && animatedText && customPlaceholder) {
        const phrases = [
            "'Flights to Goa'",
            "'Trip to Delhi'",
            "'Beach destinations'",
            "'Coorg Homestays'"
        ];
        let currentIndex = 0;
        
        setInterval(() => {
            animatedText.style.opacity = 0;
            
            setTimeout(() => {
                currentIndex = (currentIndex + 1) % phrases.length;
                animatedText.innerText = phrases[currentIndex];
                animatedText.style.opacity = 1;
            }, 300);
        }, 3000); // Change every 3 seconds
        
        // Hide custom placeholder when typing
        input.addEventListener('input', () => {
            if (input.value.length > 0) {
                customPlaceholder.style.display = 'none';
            } else {
                customPlaceholder.style.display = 'flex';
            }
        });
    }
});
"""

js += new_anim_js

with open('app.js', 'w') as f:
    f.write(js)
print("Updated app.js animation logic!")
