with open('style.css', 'r') as f:
    css = f.read()

balance = 0
for i, line in enumerate(css.split('\n')):
    for char in line:
        if char == '{': balance += 1
        elif char == '}': balance -= 1
    if balance < 0:
        print(f"Extra closing brace at line {i+1}")
        balance = 0

if balance > 0:
    print(f"Missing {balance} closing braces!")
else:
    print("Braces are balanced.")
