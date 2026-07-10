with open('style.css', 'r') as f:
    css = f.read()

old_results_css = """#screenResults.active {
    display: flex;
    flex-direction: column;
    height: 100%;
    margin: -16px; /* Negate app-content padding so header touches edge */
    margin-bottom: -85px;
    padding-bottom: 85px;
}"""

new_results_css = """#screenResults.active {
    display: flex;
    flex-direction: column;
    height: 100%;
    margin-top: -64px; /* Pull up to cover status bar */
    margin-left: -16px;
    margin-right: -16px;
    margin-bottom: -85px;
    padding-bottom: 85px;
}"""

css = css.replace(old_results_css, new_results_css)

old_header_css = """.results-header {
    background: #fff;
    padding-top: 12px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    z-index: 10;
    position: relative;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
}"""

new_header_css = """.results-header {
    background: #fff;
    padding-top: 60px; /* Account for the status bar and notch */
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    z-index: 10;
    position: relative;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
}"""

css = css.replace(old_header_css, new_header_css)

with open('style.css', 'w') as f:
    f.write(css)

print("Adjusted flight listing header spacing!")
