import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:5176');
  await page.waitForTimeout(2000);
  
  const container = await page.locator('.rounded-full.mb-10.overflow-hidden').first();
  const box = await container.boundingBox();
  console.log(`Container box: ${JSON.stringify(box)}`);
  
  const computedStyle = await container.evaluate((el) => {
    const s = window.getComputedStyle(el);
    return {
      height: s.height,
      border: s.border,
      display: s.display,
      flexDirection: s.flexDirection
    };
  });
  console.log(`Container style:`, computedStyle);

  const btn = await page.locator('button').first();
  const btnStyle = await btn.evaluate((el) => {
    const s = window.getComputedStyle(el);
    return {
      padding: s.padding,
      paddingTop: s.paddingTop,
      paddingBottom: s.paddingBottom,
      height: s.height,
      display: s.display,
      fontSize: s.fontSize,
      color: s.color,
      backgroundColor: s.backgroundColor,
      visibility: s.visibility,
      opacity: s.opacity
    };
  });
  console.log(`Button style:`, btnStyle);
  
  await page.screenshot({ path: 'screenshot.png' });
  await browser.close();
})();
