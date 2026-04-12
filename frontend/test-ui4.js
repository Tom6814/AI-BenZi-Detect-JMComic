import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:5176');
  await page.waitForTimeout(2000);
  
  const container = await page.locator('.rounded-full.mb-10.overflow-hidden').first();
  const style = await container.evaluate(el => window.getComputedStyle(el).flexShrink);
  console.log(`Flex shrink:`, style);

  await browser.close();
})();
