import re

# 1. UPDATE APP.JS
with open('app.js', 'r') as f:
    js = f.read()

# Remove the edge badge from search results
old_edge_badge_logic = """        let edgeBadgeHtml = "";
        if (isStudentMode) {
            edgeBadgeHtml = `<div class="student-edge-badge">✨ Free Change • 🧳 15Kg Extra</div>`;
        }"""
new_edge_badge_logic = """        let edgeBadgeHtml = "";
        // Removed edge badge from search page as requested"""
js = js.replace(old_edge_badge_logic, new_edge_badge_logic)

# Update standard cards in renderFlightResults
old_eco_logic = """        if (isStudentMode) {
            ecoColClass = "fc-price-col student-fare-active";
            const originalPriceNum = parseInt(f.price.replace(',', ''));
            const discountedPriceNum = Math.floor(originalPriceNum * 0.9);
            const discountedStr = discountedPriceNum.toLocaleString('en-IN');
            
            ecoPriceHtml = `<span class="price-strikethrough">₹${f.price}</span> ₹${discountedStr}`;
            ecoTagHtml = '<span style="font-size: 8px; background: rgba(52, 211, 153, 0.15); color: #10b981; padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(52, 211, 153, 0.3);">Extra bag + Date change</span>';
        }"""

new_eco_logic = """        if (isStudentMode) {
            ecoColClass = "fc-price-col student-fare-search-active";
            const originalPriceNum = parseInt(f.price.replace(',', ''));
            const discountedPriceNum = Math.floor(originalPriceNum * 0.9);
            const discountedStr = discountedPriceNum.toLocaleString('en-IN');
            
            ecoPriceHtml = `<span class="price-strikethrough">₹${f.price}</span> ₹${discountedStr}`;
            ecoTagHtml = '<span style="font-size: 9px; background: rgba(14, 165, 233, 0.08); color: var(--indigo-blue); padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(14, 165, 233, 0.2);">Extra benefits</span>';
        }"""
js = js.replace(old_eco_logic, new_eco_logic)

# Update Recommended Card
old_rec_logic = """    if (isStudentMode) {
        ecoColClass = "fc-price-col student-fare-active";
        const originalPriceNum = parseInt(oldP.replace(',', ''));
        const discountedPriceNum = Math.floor(originalPriceNum * 0.9);
        const discountedStr = discountedPriceNum.toLocaleString('en-IN');
        
        ecoPriceHtml = `<span class="price-strikethrough">₹${oldP}</span> ₹${discountedStr}`;
        ecoTagHtml = '<span style="font-size: 8px; background: rgba(52, 211, 153, 0.15); color: #10b981; padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(52, 211, 153, 0.3);">Extra bag + Date change</span>';
    }"""

new_rec_logic = """    if (isStudentMode) {
        ecoColClass = "fc-price-col student-fare-search-active";
        const originalPriceNum = parseInt(oldP.replace(',', ''));
        const discountedPriceNum = Math.floor(originalPriceNum * 0.9);
        const discountedStr = discountedPriceNum.toLocaleString('en-IN');
        
        ecoPriceHtml = `<span class="price-strikethrough">₹${oldP}</span> ₹${discountedStr}`;
        ecoTagHtml = '<span style="font-size: 9px; background: rgba(14, 165, 233, 0.08); color: var(--indigo-blue); padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(14, 165, 233, 0.2);">Extra benefits</span>';
    }"""
js = js.replace(old_rec_logic, new_rec_logic)

with open('app.js', 'w') as f:
    f.write(js)
print("Updated app.js colors and tags.")

# 2. UPDATE STYLE.CSS
with open('style.css', 'r') as f:
    css = f.read()

# Add the new light blue class for search results
if ".student-fare-search-active" not in css:
    new_css = """
.student-fare-search-active {
    background: rgba(14, 165, 233, 0.04) !important;
    border: 1px solid rgba(14, 165, 233, 0.2) !important;
}
"""
    css += new_css
    with open('style.css', 'w') as f:
        f.write(css)
    print("Added .student-fare-search-active to style.css")
