import re

with open('index.html', 'r') as f:
    html = f.read()

with open('passes_fixed.html', 'r') as f:
    passes_html = f.read()

# Replace the stack
# The stack starts with <div class="boarding-passes-stack" id="boardingPassesStack">
# And ends before <!-- Explore Communities -->
# Since the HTML is currently very malformed around the end of the stack,
# we use a non-greedy regex that stops at Explore Communities.

pattern = re.compile(r'<div class="boarding-passes-stack" id="boardingPassesStack">.*?<!-- Explore Communities -->', re.DOTALL)

new_html = pattern.sub(passes_html + "\n\n                            <!-- Explore Communities -->", html)

with open('index.html', 'w') as f:
    f.write(new_html)
