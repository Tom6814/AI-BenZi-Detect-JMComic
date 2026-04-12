import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:5176');
  await page.waitForTimeout(2000);
  
  const container = await page.locator('.rounded-full.mb-10.overflow-hidden').first();
  const computedStyle = await container.evaluate((el) => {
    const s = window.getComputedStyle(el);
    return {
      height: s.height,
      maxHeight: s.maxHeight,
      minHeight: s.minHeight,
      lineHeight: s.lineHeight,
      fontSize: s.fontSize,
      alignItems: s.alignItems,
      boxSizing: s.boxSizing
    };
  });
  console.log(`Container style:`, computedStyle);

  const btn = await page.locator('button').first();
  const btnBox = await btn.boundingBox();
  console.log(`Btn box:`, btnBox);

  await browser.close();
})();
