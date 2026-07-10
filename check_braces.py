with open('app.js', 'r') as f:
    text = f.read()

def check(text):
    stack = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        for char in line:
            if char == '{':
                stack.append(('{', i+1))
            elif char == '}':
                if not stack or stack[-1][0] != '{':
                    print(f"Mismatched }} at line {i+1}")
                    return
                stack.pop()
    if stack:
        print(f"Unmatched {stack[-1][0]} from line {stack[-1][1]}")
    else:
        print("All braces match!")

check(text)
