with open('style.css', 'r') as f:
    css = f.read()

# Replace padding: 16px; with padding: 8px 16px; on .passenger-card
css = css.replace(""".passenger-card {
    background: #E6EAF0;
    border-radius: 16px;
    padding: 16px;
    box-shadow: 5px 5px 10px rgba(163,177,198,0.5), -5px -5px 10px rgba(255,255,255,0.8);
    transition: all 0.3s ease;
    cursor: pointer;
}""", """.passenger-card {
    background: #E6EAF0;
    border-radius: 16px;
    padding: 8px 16px;
    box-shadow: 5px 5px 10px rgba(163,177,198,0.5), -5px -5px 10px rgba(255,255,255,0.8);
    transition: all 0.3s ease;
    cursor: pointer;
}""")

with open('style.css', 'w') as f:
    f.write(css)
