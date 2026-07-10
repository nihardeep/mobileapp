import re

with open('style.css', 'r') as f:
    css = f.read()

stack_css = """
/* ==========================================================================
   IOS-STYLE CARD STACK ANIMATION
   ========================================================================== */
.ios-card-stack {
    perspective: 1000px;
}

.ios-card-stack > .flight-card,
.ios-card-stack > .ai-flight-card {
    transition: margin 0.7s cubic-bezier(0.2, 0.8, 0.2, 1), 
                transform 0.7s cubic-bezier(0.2, 0.8, 0.2, 1), 
                opacity 0.7s cubic-bezier(0.2, 0.8, 0.2, 1),
                filter 0.7s cubic-bezier(0.2, 0.8, 0.2, 1);
    transform-origin: top center;
}

/* Stacked State */
.ios-card-stack.stacked > .flight-card:not(:first-child),
.ios-card-stack.stacked > .ai-flight-card:not(:first-child) {
    margin-top: -120px;
}

.ios-card-stack.stacked > .flight-card:nth-child(1),
.ios-card-stack.stacked > .ai-flight-card:nth-child(1) {
    z-index: 10;
    transform: scale(1) translateY(0);
    opacity: 1;
}

.ios-card-stack.stacked > .flight-card:nth-child(2),
.ios-card-stack.stacked > .ai-flight-card:nth-child(2) {
    z-index: 9;
    transform: scale(0.94) translateY(0);
    filter: brightness(0.95);
    opacity: 1;
}

.ios-card-stack.stacked > .flight-card:nth-child(3),
.ios-card-stack.stacked > .ai-flight-card:nth-child(3) {
    z-index: 8;
    transform: scale(0.88) translateY(0);
    filter: brightness(0.85);
    opacity: 1;
}

/* Hide the rest behind the 3rd card */
.ios-card-stack.stacked > .flight-card:nth-child(n+4),
.ios-card-stack.stacked > .ai-flight-card:nth-child(n+4) {
    z-index: 7;
    transform: scale(0.82) translateY(0);
    margin-top: -140px; /* pull them up completely so they don't extend the stack */
    opacity: 0;
}

/* Expanded/Normal State */
.ios-card-stack:not(.stacked) > .flight-card,
.ios-card-stack:not(.stacked) > .ai-flight-card {
    z-index: 1;
    transform: scale(1) translateY(0);
    opacity: 1;
    filter: brightness(1);
    /* margin-top will default to 0 (or gap) because the :not(:first-child) selector is removed */
}
"""

if "IOS-STYLE CARD STACK ANIMATION" not in css:
    with open('style.css', 'a') as f:
        f.write("\n" + stack_css)
        print("CSS appended")
else:
    print("CSS already exists")
