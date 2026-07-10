const fs = require('fs');
const css = fs.readFileSync('style.css', 'utf8');

let openBraces = 0;
const lines = css.split('\n');
for (let i = 0; i < lines.length; i++) {
    for (let char of lines[i]) {
        if (char === '{') openBraces++;
        if (char === '}') openBraces--;
    }
    if (openBraces < 0) {
        console.log(`Extra closing brace at line ${i + 1}`);
        openBraces = 0;
    }
}
if (openBraces > 0) {
    console.log(`Missing ${openBraces} closing braces!`);
} else {
    console.log("Braces are balanced.");
}
