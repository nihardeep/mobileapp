import re

with open('style.css', 'r') as f:
    css = f.read()

# Replace .ios-card-stack.stacked > .card with .ios-card-stack > .card.stacked-card
css = css.replace('.ios-card-stack.stacked > .flight-card:not(:first-child),\n.ios-card-stack.stacked > .ai-flight-card:not(:first-child)', '.ios-card-stack > .flight-card.stacked-card:not(:first-child),\n.ios-card-stack > .ai-flight-card.stacked-card:not(:first-child)')

css = css.replace('.ios-card-stack.stacked > .flight-card:nth-child(1),\n.ios-card-stack.stacked > .ai-flight-card:nth-child(1)', '.ios-card-stack > .flight-card.stacked-card:nth-child(1),\n.ios-card-stack > .ai-flight-card.stacked-card:nth-child(1)')

css = css.replace('.ios-card-stack.stacked > .flight-card:nth-child(2),\n.ios-card-stack.stacked > .ai-flight-card:nth-child(2)', '.ios-card-stack > .flight-card.stacked-card:nth-child(2),\n.ios-card-stack > .ai-flight-card.stacked-card:nth-child(2)')

css = css.replace('.ios-card-stack.stacked > .flight-card:nth-child(3),\n.ios-card-stack.stacked > .ai-flight-card:nth-child(3)', '.ios-card-stack > .flight-card.stacked-card:nth-child(3),\n.ios-card-stack > .ai-flight-card.stacked-card:nth-child(3)')

css = css.replace('.ios-card-stack.stacked > .flight-card:nth-child(n+4),\n.ios-card-stack.stacked > .ai-flight-card:nth-child(n+4)', '.ios-card-stack > .flight-card.stacked-card:nth-child(n+4),\n.ios-card-stack > .ai-flight-card.stacked-card:nth-child(n+4)')

# Remove the Expanded state override because we just remove the .stacked-card class to expand
css = re.sub(r'/\* Expanded/Normal State \*/.*?\}', '', css, flags=re.DOTALL)

with open('style.css', 'w') as f:
    f.write(css)

print("CSS updated for staggered staggering")
