import re

with open('style.css', 'r', encoding='utf-8') as f:
    content = f.read()

old_body = """body {
    font-family: var(--font-family);
    background: #08090d; /* High-end dark control room feel */
    color: var(--text-primary);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow-x: hidden;
    padding: 20px;
}"""

new_body = """html, body {
    overflow-x: hidden;
    width: 100%;
    overscroll-behavior-x: none; /* Prevent iOS bounce/swipe */
}

body {
    font-family: var(--font-family);
    background: #08090d; /* High-end dark control room feel */
    color: var(--text-primary);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow-x: hidden;
    padding: 20px;
    box-sizing: border-box;
}

/* Ensure mobile view doesn't cause horizontal overflow */
@media (max-width: 480px) {
    .iphone-frame {
        transform: scale(0.85);
        transform-origin: top center;
        margin-bottom: -100px;
    }
    body {
        padding: 10px;
        align-items: flex-start;
    }
}"""

content = content.replace(old_body, new_body)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("CSS fixed.")
