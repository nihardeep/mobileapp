with open('style.css', 'a') as f:
    f.write("""
/* Global Font Enforcement */
* {
    font-family: var(--font-family);
}
input, button, select, textarea {
    font-family: inherit;
}
""")
