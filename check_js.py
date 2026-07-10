import re

def check_braces(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Very basic brace counting
    open_braces = content.count('{')
    close_braces = content.count('}')
    
    print(f"{filename} - Open: {open_braces}, Close: {close_braces}")

check_braces('app.js')
