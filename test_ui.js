const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
    const page = await browser.newPage();
    await page.setViewport({ width: 390, height: 844 });
    
    // Go to home page
    await page.goto('http://localhost:8000/index.html');
    await page.waitForTimeout(1000);
    
    // Take screenshot of Home page with deals
    await page.screenshot({ path: 'home_deals.png' });
    
    // Evaluate JS to trigger Upfront unlock
    await page.evaluate(() => {
        // Trigger upfront unlock
        if (typeof unlockUpfrontPerks === 'function') {
            unlockUpfrontPerks();
        }
    });
    
    await page.waitForTimeout(500);
    
    // Click on "Free Seat" button
    await page.evaluate(() => {
        const freeSeatBtn = Array.from(document.querySelectorAll('div')).find(el => el.innerText && el.innerText.includes('Pick any premium seat for free'));
        if (freeSeatBtn && freeSeatBtn.parentElement) {
            freeSeatBtn.parentElement.click();
        }
    });
    
    await page.waitForTimeout(1000);
    
    // Take screenshot of Addons page
    await page.screenshot({ path: 'addons_free_seat.png' });
    
    await browser.close();
})();
