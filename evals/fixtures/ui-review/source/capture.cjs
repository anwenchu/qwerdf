// Rebuild synthetic browser screenshots; requires Playwright and Chrome.
// No server, remote assets, credentials or production data are used.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { createHash } = require('node:crypto');

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.QWERDF_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true,
  });
  const output = path.resolve(__dirname, '../images');
  fs.mkdirSync(output, { recursive: true });
  const records = [];
  try {
    const cases = [
      ['mobile-form', 'mobile-form.html', 375, 812],
      ['compact-report', 'compact-report.html', 1024, 640],
      ['amount-clipped', 'amount-summary.html', 375, 640],
      ['amount-readable', 'amount-summary.html?variant=readable', 375, 640],
      ['save-error', 'save-feedback.html', 375, 640],
      ['save-error-feedback', 'save-feedback.html?variant=feedback', 375, 640],
    ];
    for (const [name, source, width, height] of cases) {
      const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1, locale: 'en-US', colorScheme: 'light' });
      const [filePath, query] = source.split('?');
      const url = pathToFileURL(path.join(__dirname, filePath));
      if (query) url.search = query;
      await page.goto(url.href);
      await page.evaluate(() => document.fonts.ready);
      let attempt;
      if (name.startsWith('save-error')) {
        await page.getByRole('button', { name: 'Save changes' }).click();
        attempt = await page.evaluate(() => window.lastAttempt);
        if (attempt?.outcome !== 'rejected' || !attempt.inputPreserved) throw new Error('Expected a rejected save with preserved input');
      }
      const file = `${name}.png`;
      const bytes = await page.screenshot({ path: path.join(output, file), animations: 'disabled' });
      records.push({ file, width, height, dpr: 1, theme: 'light', locale: 'en-US', state: attempt ? 'save-rejected' : 'default',
        data: 'synthetic static sample', version: 'fixture-v1', font: 'Arial, sans-serif',
        ...(attempt ? { attempt } : {}), sha256: createHash('sha256').update(bytes).digest('hex') });
      await page.close();
    }
    fs.writeFileSync(path.join(output, 'baseline.json'), JSON.stringify({ browser: browser.version(), images: records }, null, 2) + '\n');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error.message); process.exitCode = 1; });
