const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', error => console.log('PAGE ERROR:', error.message));
  page.on('requestfailed', request => console.log('REQUEST FAILED:', request.url(), request.failure().errorText));

  const fileUrl = 'file://' + path.resolve('index.html');
  await page.goto(fileUrl, { waitUntil: 'networkidle0' });
  
  console.log('Finished loading page');
  await browser.close();
})();
