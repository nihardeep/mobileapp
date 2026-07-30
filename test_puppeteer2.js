const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  
  page.on('console', msg => {
      if (msg.type() === 'error') {
          console.log('CONSOLE ERROR:', msg.text());
      }
  });
  page.on('pageerror', error => console.log('PAGE ERROR:', error.message));

  const fileUrl = 'file://' + path.resolve('index.html');
  await page.goto(fileUrl, { waitUntil: 'domcontentloaded' });
  
  // Wait a bit to allow JS to run
  await new Promise(r => setTimeout(r, 1000));
  
  console.log('Finished loading page');
  await browser.close();
})();
