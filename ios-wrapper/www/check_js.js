const fs = require('fs');
try {
  const code = fs.readFileSync('app.js', 'utf8');
  new Function(code);
  console.log("Syntax OK");
} catch(e) {
  console.log("SYNTAX ERROR: " + e.message);
}
