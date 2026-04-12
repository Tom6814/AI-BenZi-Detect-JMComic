import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:5173');
  // wait for it to load
  await page.waitForTimeout(2000);
  
  // check what classes the button has
  const buttons = await page.locator('button').all();
  for (const b of buttons) {
    const text = await b.textContent();
    const className = await b.getAttribute('class');
    const box = await b.boundingBox();
    console.log(`Button: ${text.trim()}, class: ${className}, box: ${JSON.stringify(box)}`);
  }
  
  await browser.close();
})();
