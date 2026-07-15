import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace(
""".bp-timeline-slider {
    display: flex;
    width: 200%;
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.bp-timeline-leg {
    width: 50%;
    padding: 0 20px 24px;
}""",
""".bp-timeline-slider {
    display: flex;
    width: 100%;
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.bp-timeline-leg {
    flex: 0 0 100%;
    width: 100%;
    padding: 0 20px 24px;
}"""
)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

app_js = app_js.replace("slider.style.transform = 'translateX(-50%)'", "slider.style.transform = 'translateX(-100%)'")
app_js = app_js.replace("if(slider) slider.style.width = '100%';", "")
app_js = app_js.replace("if(slider) slider.style.width = '200%';", "")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("Fixed distortion.")
