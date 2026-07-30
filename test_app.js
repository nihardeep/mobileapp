const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = fs.readFileSync('index.html', 'utf8');
const dom = new JSDOM(html, {
  runScripts: "dangerously",
  resources: "usable"
});

dom.window.addEventListener('error', (event) => {
    console.error('JSDOM ERROR:', event.error);
});
dom.window.addEventListener('unhandledrejection', (event) => {
    console.error('JSDOM PROMISE REJECTION:', event.reason);
});

setTimeout(() => {
    console.log('Finished waiting for DOMContentLoaded');
}, 1000);
