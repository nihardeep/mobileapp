import re

with open('app.js', 'r') as f:
    js = f.read()

# Fix the card class and badge
old_badge_logic = """        let edgeBadgeHtml = "";
        if (i === 1) {
            edgeBadgeHtml = `<div class="fc-edge-badge">
                <svg viewBox="0 0 24 24" width="10" height="10" fill="currentColor"><path d="M12 2l2.4 7.6L22 12l-7.6 2.4L12 22l-2.4-7.6L2 12l7.6-2.4L12 2z"/></svg> RECOMMENDED FARE
            </div>`;
        }

        return `
        <div class="flight-card" id="flightCard-${i}">
            ${edgeBadgeHtml}"""

new_badge_logic = """        let edgeBadgeHtml = "";
        let cardClass = "flight-card";
        if (i === 1) {
            cardClass += " recommended";
            edgeBadgeHtml = `<div class="recommended-badge">
                <svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><path d="M12 2l2.4 7.6L22 12l-7.6 2.4L12 22l-2.4-7.6L2 12l7.6-2.4L12 2z"/></svg> RECOMMENDED FARE
            </div>`;
        }

        return `
        <div class="${cardClass}" id="flightCard-${i}">
            ${edgeBadgeHtml}"""

js = js.replace(old_badge_logic, new_badge_logic)

with open('app.js', 'w') as f:
    f.write(js)

print("Updated app.js")

with open('style.css', 'r') as f:
    css = f.read()

# Update .flight-card.recommended
old_card_css = """.flight-card.recommended {
    border: 1.5px solid var(--indigo-accent);
    background: linear-gradient(to right, rgba(0, 27, 148, 0.02), #fff);
    position: relative;
    overflow: visible;
    margin-top: 16px;
}"""

new_card_css = """.flight-card.recommended {
    border: 1.5px solid rgba(212, 175, 55, 0.4);
    background: linear-gradient(to bottom, rgba(212, 175, 55, 0.05), #fff);
    box-shadow: 0 4px 16px rgba(212, 175, 55, 0.1);
    position: relative;
    overflow: visible;
    margin-top: 16px;
}"""

css = css.replace(old_card_css, new_card_css)

# Update .flight-card.recommended::before (remove the blue strip)
old_before_css = """.flight-card.recommended::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: var(--indigo-accent);
    border-top-left-radius: 14px;
    border-bottom-left-radius: 14px;
}"""

css = css.replace(old_before_css, "/* .flight-card.recommended::before removed */")

# Update .recommended-badge
old_rec_badge_css = """.recommended-badge {
    position: absolute;
    top: -12px;
    left: 16px;
    background: #fffbea;
    border: 1px solid rgba(217, 119, 6, 0.2);
    color: #d97706;
    font-size: 10px;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 4px;
    box-shadow: 0 2px 8px rgba(217, 119, 6, 0.1);
    z-index: 5;
}"""

new_rec_badge_css = """.recommended-badge {
    position: absolute;
    top: -12px;
    right: 16px;
    background: #FDF7E7;
    border: 1.5px solid rgba(212, 175, 55, 0.3);
    color: #D4AF37;
    font-size: 11px;
    font-weight: 800;
    padding: 4px 12px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    gap: 4px;
    box-shadow: 0 4px 8px rgba(212, 175, 55, 0.15);
    z-index: 5;
}"""

css = css.replace(old_rec_badge_css, new_rec_badge_css)

with open('style.css', 'w') as f:
    f.write(css)

print("Updated style.css")
