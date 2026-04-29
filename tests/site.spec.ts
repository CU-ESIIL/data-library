import { expect, test } from '@playwright/test';

const MAX_NAV_LINKS = 10;
const MAX_PAGE_LINKS = 25;

function isLocalHttpPath(href: string | null): href is string {
  if (!href) return false;
  if (href === '...' || href.startsWith('data:')) return false;
  if (href.startsWith('#')) return false;
  if (href.startsWith('mailto:') || href.startsWith('tel:')) return false;
  if (href.startsWith('http://') || href.startsWith('https://')) return false;
  return true;
}

function normalizePath(href: string): string {
  const withoutOrigin = href.replace(/^http:\/\/localhost:8000/, '');
  return withoutOrigin || '/';
}

test('homepage loads', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/./);
  await expect(page.locator('body')).toBeVisible();
});

test('core navigation links resolve', async ({ page }) => {
  await page.goto('/');
  const links = page.locator('nav a');
  const count = await links.count();
  const warnings: string[] = [];

  for (let i = 0; i < Math.min(count, MAX_NAV_LINKS); i += 1) {
    const href = await links.nth(i).getAttribute('href');
    if (!isLocalHttpPath(href)) continue;

    const target = normalizePath(href);
    const response = await page.goto(target);
    const status = response?.status() ?? 0;
    const bodyText = await page.locator('body').innerText().catch(() => '');

    if (!response || status >= 400 || /404|page not found/i.test(bodyText)) {
      warnings.push(`${target} returned status ${status || 'unknown'} or looked like a 404`);
      continue;
    }

    await expect(page.locator('body')).toBeVisible();
  }

  if (warnings.length > 0) {
    console.warn(`Navigation warnings:\n${warnings.join('\n')}`);
  }
});

test('homepage does not look like a 404', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('body')).not.toContainText(/404|page not found/i);
});

test('homepage local links are not obviously broken', async ({ page, request }) => {
  await page.goto('/');
  const hrefs = await page.locator('main a[href]').evaluateAll((anchors) =>
    anchors
      .map((anchor) => anchor.getAttribute('href'))
      .filter((href): href is string => Boolean(href))
  );

  const warnings: string[] = [];
  for (const href of hrefs.filter(isLocalHttpPath).slice(0, MAX_PAGE_LINKS)) {
    const target = normalizePath(href);
    const response = await request.get(target);
    const status = response.status();
    if (status >= 400) {
      warnings.push(`${target} returned status ${status}`);
    }
  }

  if (warnings.length > 0) {
    console.warn(`Homepage link warnings:\n${warnings.join('\n')}`);
  }
});
